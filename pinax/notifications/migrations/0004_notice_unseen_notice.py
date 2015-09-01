# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20150812_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='unseen_notice',
            field=models.BooleanField(default=True, verbose_name='unseen_notice'),
            preserve_default=True,
        ),
    ]
