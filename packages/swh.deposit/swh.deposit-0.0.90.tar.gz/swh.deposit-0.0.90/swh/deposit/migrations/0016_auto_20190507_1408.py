# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-05-07 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("deposit", "0015_depositrequest_typemigration"),
    ]

    operations = [
        migrations.AddField(
            model_name="deposit",
            name="check_task_id",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="Scheduler's associated checking task id",
            ),
        ),
        migrations.AddField(
            model_name="deposit",
            name="load_task_id",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="Scheduler's associated loading task id",
            ),
        ),
    ]
