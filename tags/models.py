from django.db import models
from taggit.models import GenericTaggedItemBase, TagBase


class CustomTag(TagBase):
    similar_tag = models.ManyToManyField("self", blank=True)
    featured = models.BooleanField(default=False)

class Tagged(GenericTaggedItemBase):
    tag = models.ForeignKey(
        CustomTag,
        related_name="%(app_label)s_%(class)s_items",
        on_delete=models.SET_NULL,
        null=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

class CustomAnswerTag(TagBase):
    similar_tag = models.ManyToManyField("self", blank=True)
    featured = models.BooleanField(default=False)


class AnswerTagged(GenericTaggedItemBase):
    tag = models.ForeignKey(
        CustomAnswerTag,
        related_name="%(app_label)s_%(class)s_items",
        on_delete=models.SET_NULL,
        null=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
