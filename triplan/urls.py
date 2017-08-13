from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from triplan import views

urlpatterns = [
    url(r'^$', login_required(views.HomepageView.as_view()),
        name="itinerary_list"),
    url(r'^search/(?P<search_str>[+\w{}.-]{0,40})/$', login_required(views.ItineraryListByLocationView.as_view()),
        name='itinerary_list_search'),
    url(r'^category/(?P<category_pk>[0-9]+)/$', login_required(views.ItineraryListByCategory.as_view()),
        name="itinerary_list_category"),
    url(r'^create/$', login_required(views.ItineraryCreate.as_view()),
        name="itinerary_create"),
    url(r'^(?P<pk>[0-9]+)/create/$', login_required(views.ItinerarySegmentCreate.as_view()),
        name="itinerarysegment_create"),
    url(r'^(?P<pk>[0-9]+)/$', login_required(views.ItineraryDetailView.as_view()),
        name="itinerary_detail"),
    url(r'^(?P<pk>[0-9]+)/addreview/$', login_required(views.ReviewCreate.as_view()),
        name="review_create"),
    url(r'^(?P<pk>[0-9]+)/edit/$', login_required(views.ItineraryEdit.as_view()),
        name="itinerary_edit"),
    url(r'^(?P<itinerary_pk>[0-9]+)/(?P<pk>[0-9]+)/edit/$', login_required(views.ItinerarySegmentEdit.as_view()),
        name="itinerarysegment_edit"),
    url(r'my_profile/$', login_required(views.UserProfile.as_view()),
        name="user_profile"),
]
