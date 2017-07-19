from datetime import datetime, date, timedelta
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

    @property
    def total_duration(self):
        total = timedelta()
        for segment in self.itinerarysegment_set.all():
            total += segment.duration
        return self.format_delta_time(total)

    @staticmethod
    def format_delta_time(tdelta):
        res = ""
        days = tdelta.days
        hours, rem = divmod(tdelta.seconds, 3600)
        minutes, sec = divmod(rem, 60)
        if days > 0:
            res += str(days) + "days "
        if hours > 0:
            res += str(hours) + "h "
        if minutes > 0:
            res += str(minutes) + "min"
        if res == "":
            return "No trips added"
        return res


class CategoryUtil:
    category_list = ["Food", "Educational", "Outdoor", "Games", "Social", "Shopping",
                     "Casino", "Recreational", "Photo-spot", "Other"]
    icon_list     = ["cutlery", "university", "sun-o", "gamepad", "users", "shopping-bag",
                     "money", "soccer-ball-o", "camera", "lightbulb-o"]

    @staticmethod
    def get_category_choices():
        integer_list = list(range(0, len(CategoryUtil.category_list)))
        return zip(integer_list, CategoryUtil.category_list)

    @staticmethod
    def prepend_class_name(icon_name):
        return "fa fa-" + str(icon_name)

    @staticmethod
    def get_icon_class(category):
        icon_class_name_list = map(CategoryUtil.prepend_class_name, CategoryUtil.icon_list)
        return (
            dict(zip(list(range(0, len(CategoryUtil.category_list))), icon_class_name_list))
        ).get(category, "")


class ItinerarySegment(models.Model):
    itinerary = models.ForeignKey(Itinerary)
    location = models.CharField(max_length=200)
    start_time = models.TimeField(default="12:00 PM")
    end_time = models.TimeField(default="1:00 PM")
    description = models.CharField(max_length=400)
    photo = models.ImageField(blank=True)
    category = models.IntegerField(default=0, choices=CategoryUtil.get_category_choices())

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return self.itinerary.__str__() + self.description.__str__()

    @property
    def duration(self):
        # assume duration always < 1 day
        # TODO: display in hours and minutes / smart display
        return datetime.combine(date.today(), self.end_time) - datetime.combine(date.today(), self.start_time)

    @property
    def encoded_location(self):
        return urllib.parse.quote_plus(self.location)

    @property
    def category_icon_class(self):
        return CategoryUtil.get_icon_class(self.category)
