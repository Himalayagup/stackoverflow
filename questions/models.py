from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from accounts.models import User
from tags.models import Tagged, AnswerTagged
from taggit_selectize.managers import TaggableManager
from .utils import unique_slug_generator_using_title

class Questions(models.Model):
    title = models.CharField("Question",max_length=255)
    slug = models.SlugField(max_length=260, unique=True, blank=True, null=True)
    associated_user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    tags = TaggableManager(through=Tagged,blank=True)
    vote = models.SmallIntegerField("Vote", default=0)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator_using_title(self)
        super().save(*args, **kwargs)

class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.TextField("Solution")
    tags = TaggableManager(through=AnswerTagged,blank=True)
    vote = models.SmallIntegerField("Vote", default=0)
    parent_answer = models.ForeignKey("self", on_delete=models.SET_NULL,blank=True,
                                    null=True,related_name="replytosolution")

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.question.title
