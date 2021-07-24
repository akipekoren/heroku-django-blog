# Generated by Django 3.1.7 on 2021-04-10 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myblog', '0016_auto_20210402_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='isSuggested',
            field=models.CharField(choices=[('HighlySuggested', 'HighlySuggested'), ('Normal', 'Normal')], default=1, max_length=30),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comment_users', to='auth.user'),
            preserve_default=False,
        ),
    ]