import uuid
import datetime
from random import randint

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models import CharField, Count
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import wonderwords
from wonderwords import RandomWord
# from 
# https://pypi.org/project/wonderwords/

class Household(models.Model):
    household_id = models.UUIDField(primary_key=True,
                                    default = uuid.uuid4,
                                    editable = False)

    pin = models.CharField(unique=True, max_length=6)


class Profile(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,      # On delete of user, profile is deleted
            primary_key=True,
    )
    # tasks_finished = Chore.objects.filter(user_claimed=user).annotate(tasks_finished=Count('task_status').filter(task_status='True'))
    # points = Chore.objects.filter(user_claimed=user, task_status='True').annotate(points=Sum('points'))
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="images/", default='images/logo-round.jpg')
    
    adjective = models.CharField(max_length=55, null=True, default="No")
    noun = models.CharField(max_length=55, null=True, default="Nickname")

    points = models.IntegerField(default=0, verbose_name="points")
    tasks_finished = models.IntegerField(default=0, verbose_name="tasks finished")
    household = models.ForeignKey(Household, default=None, on_delete=models.SET_NULL, null=True, related_name = "members")


    ## game aspects
    xp = models.IntegerField(default=0, verbose_name="xp")
    level = models.IntegerField(default=0)
    nextLevelThresh = models.IntegerField(default=200)
    prevLevelThresh = models.IntegerField(default=0)
    xpToNextLevel = models.IntegerField(default=200)

    highestLevelReached = models.IntegerField(default=0)

    ##lootbox/ lootbox rewards
    lootboxes = models.IntegerField(default=3, verbose_name="lootboxes")

    fortnight_xp = models.IntegerField(default=0)
    def open_lootbox(self):
        self.lootboxes -= 1
        self.save()


    def update_levelSystem(self, points):
            self.xp += points
            
            if points > 0:
                while self.xp > self.nextLevelThresh:
                    self.level += 1
                    if(self.level > self.highestLevelReached):
                        self.lootboxes += 1
                        self.highestLevelReached +=1
                    self.update_levelThresh(self.level, self.nextLevelThresh)
                
                self.update_xpToNextLevel(self.xp, self.nextLevelThresh)

            ### only update levels if level positive
            ##### 0 lowest level
            elif points <= 0:
                while self.xp <= self.prevLevelThresh and self.level > 0:
                    self.level -=1
                    self.demotion_update_levelThresh(self.level, self.prevLevelThresh)
                    
                self.update_xpToNextLevel(self.xp, self.nextLevelThresh)
                
    def demotion_update_levelThresh(self, level, prevLevelThresh):
        self.nextLevelThresh = prevLevelThresh
        self.prevLevelThresh = 100 * ((level - 1)**2 + 2)
        if self.level == 0:
            self.prevLevelThresh = 0

    def update_levelThresh(self, level, nextLevelThresh):
        self.prevLevelThresh = nextLevelThresh
        self.nextLevelThresh = 100 * ((level)**2 + 2)
    
    def update_xpToNextLevel(self, xp, nextLevelThresh):
        self.xpToNextLevel = nextLevelThresh - xp




    def modify_points(self, points, chore):  # add in views when task is marked as complete
        self.points += points
        
        ##update xp
        self.update_levelSystem(points)

        if chore.task_status:
            self.tasks_finished += 1
        else:
            self.tasks_finished -= 1
        self.save()
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Bulletin(models.Model):
    profile = models.ForeignKey(Profile, default=None, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='bulletin_user')
    title = models.CharField(max_length=100)
    bulletin_body = models.CharField(max_length=500)
    creation_time = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField()
    household = models.ForeignKey(Household, default=None, on_delete=models.CASCADE, null=True)


class Event(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    datetime = models.DateTimeField()


class Task(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    creation_time = models.DateTimeField()
    due_date = models.DateTimeField(default=None, null=True, blank=True)
    points = models.IntegerField()
    claimed = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)
    task_status = models.BooleanField(default=False)  # finished/not
    kudos = models.BooleanField(default=False)  # Is the task created by kudos system?
    expired = models.BooleanField(default=False)
    user_created = models.ForeignKey(Profile, default=None, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='task_user_created')
    user_claimed = models.ForeignKey(Profile, default=None, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='task_user_claimed')
    household = models.ForeignKey(Household, default=None, on_delete=models.CASCADE, null=True)


class TaskRecurrence(models.Model):
    #Recurrence Info
    task_to_clone = models.ForeignKey(Task, default=None, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=8)
    mo = models.BooleanField(default=False)
    tu = models.BooleanField(default=False)
    we = models.BooleanField(default=False)
    th = models.BooleanField(default=False)
    fr = models.BooleanField(default=False)
    sa = models.BooleanField(default=False)
    su = models.BooleanField(default=False)
    day_of_month = models.IntegerField(null=True, blank=True)




@receiver(pre_save, sender=Task)
def cache_previous_status(sender, instance, *args, **kwargs):
    if not instance._state.adding:
        original_status = None
        if instance.user_claimed is not None and instance.claimed is True:
            original_status = Task.objects.get(pk=instance.id).task_status

        instance.__original_status = original_status
    else:
        instance.__original_status = None


@receiver(post_save, sender=Task)
def point_updater(sender, instance, **kwargs):
    if timezone.now() > instance.creation_time + timezone.timedelta(hours=24) and instance.claimed is False:
        if instance.user_claimed is not None:
            instance.claimed = 'True'
            instance.save()
        else:
            profiles = Profile.objects.filter(household=instance.household)
            count = profiles.aggregate(count=Count('user'))['count']
            random_index = randint(0, count - 1)
            instance.user_claimed = profiles[random_index]
            instance.claimed = 'True'
            instance.points = int(instance.points / 2)
            instance.save()
    if instance.task_status != instance.__original_status and instance.user_claimed is not None and instance.__original_status is not None:
        profile = instance.user_claimed
        if instance.task_status:
            profile.modify_points(instance.points, instance)
        else:
            profile.modify_points(-instance.points, instance)
    if timezone.now() > instance.due_date and instance.expired == False:
        instance.expired = True
        instance.save()


class Lootbox(models.Model):
    owner = models.ForeignKey(Profile, default=None, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='lootbox_owner')


    adjective = models.CharField(max_length=55, null=True, blank=True)
    noun = models.CharField(max_length=55, null=True, blank=True)


    def generateNounAdjectivePair(self):
        r = RandomWord()

        self.adjective = r.word(include_parts_of_speech=["adjective"])
        self.noun = r.word(include_parts_of_speech=["nouns"])
        self.save()


#class Pin(models.Model):
#    pin = models.IntegerField(unique=True)
#    attached_group = models.ForeignKey(Household)
