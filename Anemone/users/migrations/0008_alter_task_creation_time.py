# Generated by Django 4.1.1 on 2022-11-16 03:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_task_creation_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='creation_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 16, 3, 53, 34, 779534, tzinfo=datetime.timezone.utc)),
        ),
    ]