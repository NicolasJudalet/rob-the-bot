# Generated by Django 3.0.4 on 2020-04-01 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hello", "0002_auto_20200326_1554"),
    ]

    operations = [
        migrations.AddField(
            model_name="slackuser",
            name="has_answered_skill_form_v2",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="slackuser",
            name="has_answered_skill_form_v2_last_update",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="slackuser",
            name="send_no_more_messages",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="slackuser",
            name="has_answered_skill_form",
            field=models.BooleanField(default=False),
        ),
    ]
