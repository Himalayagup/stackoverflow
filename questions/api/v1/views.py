from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status
from questions.models import Questions, Answers
from django.core import serializers
from .serializers import HomePageQuestionsSerializer, QuestionSolutionCreateSerializer, QuestionCreateSerializer
class SearchByTagsView(APIView):
    def get(self,request):
        q = self.request.GET.get('q').split(",")
        if q:
            query = Q()
            for word in q:
                query = query | Q(title__icontains=word) | Q(tags__name__icontains=word)
            results = Questions.objects.filter(query)
            output = []
            for item in results:
                if item.associated_user:
                    associated_user_id = item.associated_user.id
                else:
                    associated_user_id = None
                output.append({
                'title': item.title,
                'slug': item.slug,
                'associated_user' : associated_user_id,
                'vote': item.vote,
                'total_vote': item.total_vote_count,

                })
            query1 = Q()
            for word in q:
                query1 = query1 | Q(answer__icontains=word)
            results1 = Answers.objects.filter(query1)
            output1 = []
            for item in results1:
                if item.associated_user:
                    associated_user_id = item.associated_user.id
                else:
                    associated_user_id = None
                output1.append({
                'question': item.question.title,
                'question_slug': item.question.slug,
                'answer': item.answer,
                'vote': item.vote,
                'associated_user' : associated_user_id,
                'total_vote': item.total_vote_count,
                })
            final = {}
            final['questions'] = output
            final['answers'] = output1
            return Response(final,status=status.HTTP_200_OK)
        else:
            return Response({"Result": "None"})

class HomePageQuestionsListView(generics.ListAPIView):
    serializer_class = HomePageQuestionsSerializer

    def get_queryset(self):
        return Questions.objects.all().order_by('-total_vote_count')[:3]

class AllQuestionsListView(generics.ListAPIView):
    serializer_class = HomePageQuestionsSerializer

    def get_queryset(self):
        return Questions.objects.all()

def get_threaded_answers(id):
    answers = Answers.objects.filter(parent_answer=id)
    result = []
    if answers:
        for ans in answers:
            if ans.associated_user:
                associated_user_id = ans.associated_user.id
            else:
                associated_user_id = None
            result.append({
                'id': ans.id,
                'reply' : ans.answer,
                'votes' : ans.vote,
                'total_vote' : ans.total_vote_count,
                'associated_user' : associated_user_id
            })
    return result

class QuestionSolutionListView(APIView):
    def get(self,request,slug):
        print(self.request.user.is_authenticated)
        if Questions.objects.filter(slug=slug).exists():
            que = Questions.objects.get(slug=slug)
        else:
            output = "No Question Found for Matching Slug"
            return Response(output,status=status.HTTP_200_OK)
        answers = Answers.objects.filter(question=que).exclude(parent_answer__isnull=False)
        output = []
        for ans in answers:
            threaded_answers = get_threaded_answers(ans.id)
            if ans.associated_user:
                associated_user_id = ans.associated_user.id
            else:
                associated_user_id = None
            output.append({
                'id': ans.id,
                'reply' : ans.answer,
                'votes' : ans.vote,
                'total_vote' : ans.total_vote_count,
                'thread_reply': threaded_answers,
                'associated_user' : associated_user_id

            })
        return Response(output,status=status.HTTP_200_OK)

class QuestionSolutionCreateView(generics.CreateAPIView):
    serializer_class = QuestionSolutionCreateSerializer

    def perform_create(self, serializer):
        question_id = self.kwargs.get("question_id", None)
        if Questions.objects.filter(id=question_id).exists():
            ques = Questions.objects.get(id=question_id)
            if self.request.user and self.request.user.is_authenticated :
                solution = serializer.save(
                    associated_user=self.request.user,
                    question=ques)
            else:
                return Response({"User": "Not Logged In"})
        else:
            return Response({"Question": "Not Found"})

class QuestionSolutionThreadCreateView(generics.CreateAPIView):
    serializer_class = QuestionSolutionCreateSerializer

    def perform_create(self, serializer):
        solution_id = self.kwargs.get("solution_id", None)
        if Answers.objects.filter(id=solution_id).exists():
            ans = Answers.objects.get(id=solution_id)
            quest = Questions.objects.get(id=ans.question.id)
            if self.request.user and self.request.user.is_authenticated :
                solution = serializer.save(
                    associated_user=self.request.user,
                    parent_answer=ans,
                    question=quest)
            else:
                return Response({"User": "Not Logged In"})
        else:
            return Response({"Answer": "Not Found"})

class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionCreateSerializer

    def perform_create(self, serializer):
        if self.request.user and self.request.user.is_authenticated:
            solution = serializer.save(
                associated_user=self.request.user)
        else:
            return Response({"User": "Not Logged In"})

class QuestionUpVoteView(APIView):
    def post(self, request, *args, **kwargs):
        question_id = self.kwargs.get("question_id")
        if Questions.objects.filter(id=question_id).exists():
            if self.request.user and self.request.user.is_authenticated:
                ques = Questions.objects.get(id=question_id)
                ques.vote = ques.vote + 1
                ques.total_vote_count = ques.total_vote_count + 1
                ques.save()
                return Response({"UpVoted": "Successfully"})
            else:
                return Response({"User": "Not Logged In"})
        else:
            return Response({"Question": "Not Found"})

class QuestionDownVoteView(APIView):
    def post(self, request, *args, **kwargs):
        question_id = self.kwargs.get("question_id")
        if Questions.objects.filter(id=question_id).exists():
            if self.request.user and self.request.user.is_authenticated:
                ques = Questions.objects.get(id=question_id)
                ques.vote = ques.vote - 1
                ques.total_vote_count = ques.total_vote_count + 1
                ques.save()
                return Response({"DownVoted": "Successfully"})
            else:
                return Response({"User": "Not Logged In"})
        else:
            return Response({"Question": "Not Found"})

class AnswerUpVoteView(APIView):
    def post(self, request, *args, **kwargs):
        solution_id = self.kwargs.get("solution_id")
        if Answers.objects.filter(id=solution_id).exists():
            if self.request.user and self.request.user.is_authenticated:
                ans = Answers.objects.get(id=solution_id)
                ans.vote = ans.vote + 1
                ans.total_vote_count = ans.total_vote_count + 1
                ans.save()
                return Response({"UpVoted": "Successfully"})
            else:
                return Response({"User": "Not Logged In"})
        else:
            return Response({"Answer": "Not Found"})


class AnswerDownVoteView(APIView):
    def post(self, request, *args, **kwargs):
        solution_id = self.kwargs.get("solution_id")
        if Answers.objects.filter(id=solution_id).exists():
            if self.request.user and self.request.user.is_authenticated:
                ans = Answers.objects.get(id=solution_id)
                ans.vote = ans.vote - 1
                ans.total_vote_count = ans.total_vote_count + 1
                ans.save()
                return Response({"DownVoted": "Successfully"})
            else:
                return Response({"User": "Not Logged In"})
        else:
            return Response({"Answer": "Not Found"})
