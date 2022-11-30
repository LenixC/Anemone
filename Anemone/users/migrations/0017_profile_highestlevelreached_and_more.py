# Generated by Django 4.1.2 on 2022-11-30 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_rename_fortnite_xp_profile_fortnight_xp'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='highestLevelReached',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nextLevelThresh',
            field=models.IntegerField(default=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='xpToNextLevel',
            field=models.IntegerField(default=200),
        ),
    ]