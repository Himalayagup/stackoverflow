# Generated by Django 4.0.1 on 2022-01-11 23:15

from django.db import migrations
import taggit_selectize.managers


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_tagged'),
        ('questions', '0002_alter_questions_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='tags',
            field=taggit_selectize.managers.TaggableManager(help_text='A comma-separated list of tags.', through='tags.Tagged', to='tags.CustomTag', verbose_name='Tags'),
        ),
    ]
