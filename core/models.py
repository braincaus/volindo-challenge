from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class ActivityType(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type


class Activity(models.Model):
    activity = models.CharField(max_length=100)
    type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=1)
    participants = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    date = models.DateTimeField()
    link = models.URLField(blank=True, null=True)
    key = models.CharField(max_length=20, blank=True, null=True)
    accessibility = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.activity


class Ticket(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
