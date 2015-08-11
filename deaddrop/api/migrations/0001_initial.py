# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Secret',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('uid', models.CharField(max_length=128)),
                ('content', models.TextField()),
                ('expiry_type', models.CharField(max_length=1, choices=[(1, 'time'), (2, 'read')])),
                ('expiry_timestamp', models.DateTimeField(blank=True)),
                ('management_key', models.CharField(max_length=128)),
            ],
        ),
    ]
