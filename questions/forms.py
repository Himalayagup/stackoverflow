from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Answers


class AnswersAdminForm(forms.ModelForm):
    answer = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Answers
        fields = "__all__"
