# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-19 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("deposit", "0012_deposit_status_detail"),
    ]

    operations = [
        migrations.AddField(
            model_name="depositrequest",
            name="raw_metadata",
            field=models.TextField(null=True),
        ),
    ]
