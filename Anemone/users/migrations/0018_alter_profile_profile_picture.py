# Generated by Django 4.0.7 on 2022-11-30 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_profile_highestlevelreached_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='images/logo-round.jpg', null=True, upload_to='images/'),
        ),
    ]