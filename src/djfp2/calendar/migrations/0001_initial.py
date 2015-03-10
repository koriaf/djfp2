# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='Local start datetime')),
                ('end_date', models.DateTimeField(verbose_name='Local end datetime')),
                ('title', models.CharField(max_length=1000)),
                ('color', models.CharField(max_length=40, default='#6aa4c1', blank=True)),
                ('textcolor', models.CharField(max_length=40, default='black', blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('start_date',),
            },
            bases=(models.Model,),
        ),
    ]
