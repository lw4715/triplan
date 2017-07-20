from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from django.urls import reverse_lazy
from django.views import generic

from triplan.models import Itinerary, ItinerarySegment


class ItineraryList(generic.ListView):
    def get_queryset(self):
        return Itinerary.objects.all().order_by("-date_added")


class ItineraryDetail(generic.DetailView):
    model = Itinerary

    def days_range(self):
        print("days_range", self.get_object().total_duration)
        return range(1, self.get_object().total_duration + 1)


class ItineraryCreate(generic.edit.CreateView):
    model = Itinerary
    fields = ["title", "preview_photo", "start_date"]
    success_url = reverse_lazy('triplan:itinerary_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        form.instance.save()
        return super(ItineraryCreate, self).form_valid(form)


class ItinerarySegmentCreate(generic.edit.CreateView):
    pass
    model = ItinerarySegment
    fields = ["photo", "location","category", "description", "day_number", "start_time", "end_time", "cost"]
    widgets = {
        "start_time": AdminTimeWidget(format='fa'),
        "end_time": AdminTimeWidget(format='fa'),
        # "start_time": forms.TimeInput(format='%H:%M %p'),
        # "end_time": forms.TimeInput(format='%H:%M %p'),
    }

    def get_context_data(self, **kwargs):
        context = super(ItinerarySegmentCreate, self).get_context_data(**kwargs)
        context['itinerary'] = Itinerary.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.itinerary = Itinerary.objects.get(id=self.kwargs['pk'])
        form.instance.save()
        return super(ItinerarySegmentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('triplan:itinerary_detail', args=[self.kwargs['pk']])


class ItineraryEdit(generic.edit.UpdateView):
    template_name = "triplan/itinerary_edit.html"
    model = Itinerary
    fields = ["title", "preview_photo", "start_date"]
    success_url = reverse_lazy('triplan:itinerary_list')


class ItinerarySegmentEdit(generic.edit.UpdateView):
    template_name = "triplan/itinerarysegment_edit.html"
    model = ItinerarySegment
    fields = ["photo", "location", "category", "description", "day_number", "start_time", "end_time", "cost"]
    widgets = {
        "start_time": forms.TimeInput(format='fa'),
        "end_time": forms.TimeInput(format='fa'),
    }

    def get_success_url(self):
        return reverse_lazy('triplan:itinerary_detail', args=[self.kwargs['itinerary_pk']])
