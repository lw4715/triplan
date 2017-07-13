from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from triplan import views

urlpatterns = [
    url(r'^$', login_required(views.ItineraryList.as_view()), name="itinerary_list"),
    url(r'^create/$', login_required(views.ItineraryCreate.as_view()), name="itinerary_create"),
    url(r'^(?P<pk>[0-9]+)/create/$', login_required(views.ItinerarySegmentCreate.as_view()), name="itinerarysegment_create"),
    url(r'^(?P<pk>[0-9]+)/$', login_required(views.ItineraryDetail.as_view()), name="itinerary_detail"),
    url(r'^(?P<itinerary_pk>[0-9]+)/(?P<pk>[0-9]+)/edit/$', login_required(views.ItineraryEdit.as_view()), name="itinerary_edit"),
]
