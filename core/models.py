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
    key = models.CharField(max_length=20, blank=True, null=True)
    accessibility = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.activity
