# Generated by Django 4.0.7 on 2022-12-04 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_bulletin_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bulletin',
            old_name='user',
            new_name='profile',
        ),
    ]