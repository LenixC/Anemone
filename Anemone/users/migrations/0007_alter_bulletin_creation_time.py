# Generated by Django 4.1.3 on 2022-11-16 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_task_in_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]