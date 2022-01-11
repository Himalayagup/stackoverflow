from django.contrib import admin
from .models import Questions, Answers
from .forms import AnswersAdminForm
# Register your models here.
admin.site.register(Questions)
@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    form=AnswersAdminForm
