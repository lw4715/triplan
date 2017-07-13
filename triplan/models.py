from numbers import Number

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.user.username


class Itinerary(models.Model):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(Profile, related_name='owner', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ItinerarySegment(models.Model):
    itinerary = models.ForeignKey(Itinerary)
    location = models.CharField(max_length=200)
    duration = models.PositiveIntegerField()
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.itinerary.__str__() + self.description.__str__()
