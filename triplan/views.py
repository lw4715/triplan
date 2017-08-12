from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from triplan.models import Itinerary, ItinerarySegment, Profile, CategoryUtil


class ItineraryList(generic.ListView):
    def get_queryset(self):
        return Itinerary.objects.all().order_by("-date_added")

    def get_context_data(self, **kwargs):
        context = super(ItineraryList, self).get_context_data(**kwargs)
        context['category'] = 'All'
        context['all_categories'] = CategoryUtil.get_category_names()
        return context


class ItineraryListByCategory(generic.ListView):
    def get_queryset(self):
        return Itinerary.objects.all()\
            .filter(itinerarysegment__category=self.kwargs['category_pk'])\
            .order_by("-date_added")

    def get_context_data(self, **kwargs):
        context = super(ItineraryListByCategory, self).get_context_data(**kwargs)
        category_id = int(self.kwargs['category_pk'])
        context['category'] = CategoryUtil.get_category_names()[category_id]
        context['all_categories'] = CategoryUtil.get_category_names()
        return context


class ItineraryDetail(generic.DetailView):
    model = Itinerary

    def days_range(self):
        return range(1, self.get_object().total_duration + 1)

    def get_queryset(self):
        return Itinerary.objects.filter(Q(owner__user=self.request.user) |
                                        Q(shared_users__user=self.request.user) |
                                        Q(public_view=True)
                                        ).distinct()


def fav(request):
    print("INSIDE FAV!")
    if request.is_ajax():
        pk = request.POST.get('itinerary_id')
        itinerary = Itinerary.objects.get(id=pk)
        curr_user = request.user.profile
        print(itinerary.favourited_by.count())
        if itinerary.favourited_by.all().filter(id=curr_user.id).exists():
            itinerary.favourited_by.remove(curr_user)
            print("Removed", curr_user)
        else:
            itinerary.favourited_by.add(curr_user)
            print("Added", curr_user)
    # return render(request, "triplan/itinerary_detail.html", {'pk': pk})

# class FavouriteEdit(generic.UpdateView):
#     template_name = "triplan/fav_edit.html"
#     model = Itinerary
#     fields = ["favourted_by"]
#
#     def form_valid(self, form):


class ItineraryCreate(generic.edit.CreateView):
    model = Itinerary
    fields = ["public_view", "shared_users", "title", "preview_photo", "start_date"]
    success_url = reverse_lazy('triplan:itinerary_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        form.instance.save()
        return super(ItineraryCreate, self).form_valid(form)

    def get_form(self):
        form = super(ItineraryCreate, self).get_form()
        form.fields["shared_users"].queryset = Profile.objects.exclude(
            user=self.request.user)
        return form


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
