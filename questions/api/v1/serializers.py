from questions.models import Questions, Answers
from rest_framework import serializers

from tags.api.v1.serializers import TaggitSerializer, TagListSerializerField
# from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

class HomePageQuestionsSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Questions
        fields = [
            "id",
            "title",
            "slug",
            "vote",
            "tags",
            "associated_user",
            "total_vote_count",
        ]


class QuestionSolutionCreateSerializer(TaggitSerializer,serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = [
            "id",
            "question",
            "answer",
            "vote",
            "total_vote_count",
            "parent_answer",
        ]

class QuestionCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Questions
        fields = [
            "id",
            "title",
            "slug",
            "vote",
            "tags",
            # "associated_user",
            "total_vote_count",
        ]
