# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinax_notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticesetting',
            name='medium',
            field=models.CharField(max_length=100, verbose_name='medium', choices=[('email', 'email')]),
        ),
    ]
