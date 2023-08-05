# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-05 10:36
from __future__ import unicode_literals

from django.db import migrations, models
import swh.deposit.models


class Migration(migrations.Migration):

    dependencies = [
        ("deposit", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="depositrequest",
            name="archive",
            field=models.FileField(
                null=True, upload_to=swh.deposit.models.client_directory_path
            ),
        ),
    ]
