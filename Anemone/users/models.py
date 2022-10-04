from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,      # On delete of user, profile is deleted
            primary_key = True,          
    )

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Message(models.Model):
    sender = models.ForeignKey(
            Profile,
            on_delete=models.CASCADE
    )
    message_body = models.TextField()
    datetime = models.DateTimeField()

class Event(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    datetime = models.DateTimeField()

class Chore(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    due_date = models.DateTimeField()
    points = models.IntegerField()

class Household(models.Model):
    profiles = models.ManyToManyField(Profile)
    messages = models.ManyToManyField(Message)
    events = models.ManyToManyField(Event)
    chores = models.ManyToManyField(Chore)

