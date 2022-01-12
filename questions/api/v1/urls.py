from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("search-question/", views.SearchByTagsView.as_view(), name="search_by_tag"),
    path("top-three/", views.HomePageQuestionsListView.as_view(), name="top_three_questions"),
    path("all/", views.AllQuestionsListView.as_view(),name="all_questions"),
    path("<slug:slug>/solutions/", views.QuestionSolutionListView.as_view(), name="solutions"),
    path("<int:question_id>/solution/create/", views.QuestionSolutionCreateView.as_view(), name="solution_create"),
    path("<int:question_id>/upvote/", views.QuestionUpVoteView.as_view(), name="question_up_vote"),
    path("<int:question_id>/downvote/", views.QuestionDownVoteView.as_view(), name="question_down_vote"),
    path("<int:solution_id>/solution/thread/create/", views.QuestionSolutionThreadCreateView.as_view(), name="solution_thread_create"),
    path("create-question/", views.QuestionCreateView.as_view(), name="create_new_question"),

]
