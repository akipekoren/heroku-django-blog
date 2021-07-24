# Generated by Django 3.1.7 on 2021-05-08 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0018_auto_20210410_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=models.CharField(max_length=300)),
        ),
        migrations.AlterField(
            model_name='post',
            name='isSuggested',
            field=models.CharField(choices=[('HighlySuggested', 'HighlySuggested'), ('Normal', 'Normal')], default=0, max_length=30),
        ),
    ]
