from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from accounts.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.name = self.cleaned_data.get('name')
        user.save()
        return user
