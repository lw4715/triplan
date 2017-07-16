from datetime import datetime, date
import urllib

from django.contrib.auth.models import User
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
    preview_photo = models.ImageField(blank=True)

    def __str__(self):
        return self.title

    @property
    def encoded_locations(self):
        location_list = []
        for segment in self.itinerarysegment_set.all():
            location_list.append(urllib.parse.quote_plus(segment.location))
        return "%7C".join(location_list)


class ItinerarySegment(models.Model):
    itinerary = models.ForeignKey(Itinerary)
    location = models.CharField(max_length=200)
    start_time = models.TimeField(default="12:00 PM")
    end_time = models.TimeField(default="1:00 PM")
    description = models.CharField(max_length=400)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return self.itinerary.__str__() + self.description.__str__()

    @property
    def duration(self):
        # asseume duration always < 1 day
        # TODO: display in hours and minutes / smart display
        return datetime.combine(date.today(), self.end_time) - datetime.combine(date.today(), self.start_time)
