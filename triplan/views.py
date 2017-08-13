import urllib

from django import forms
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.views.generic.list import MultipleObjectMixin

from triplan.models import Itinerary, ItinerarySegment, Profile, CategoryUtil, Review


class HomepageView(View):
    def get(self, request, *args, **kwargs):
        view = ItineraryList.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = LocationSearch.as_view()
        return view(request, *args, **kwargs)


class LocationSearchForm(forms.Form):
    search_str = forms.CharField()


class LocationSearch(MultipleObjectMixin, FormView):
    template_name = "triplan/itinerary_list.html"
    form_class = LocationSearchForm

    def __init__(self):
        super().__init__()
        self.object_list = []

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return super(LocationSearch, self).post(request, *args, **kwargs)

    def get_success_url(self):
        form = self.get_form()
        search_str = urllib.parse.quote_plus(form.data['search_str'])
        return reverse_lazy('triplan:itinerary_list_search', kwargs={'search_str': search_str})


class ItineraryList(generic.ListView):
    def get_context_data(self, **kwargs):
        context = super(ItineraryList, self).get_context_data(**kwargs)
        context['title'] = "Ready for your next trip " + self.request.user.username + "?"
        context['category'] = 'All'
        context['all_categories'] = CategoryUtil.get_category_names()
        context['form'] = LocationSearchForm()
        return context

    def get_queryset(self):
        return Itinerary.objects.all().order_by("-date_added")


class ItineraryListByLocationView(View):
    def get(self, request, *args, **kwargs):
        view = ItineraryListByLocation.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = LocationSearch.as_view()
        return view(request, *args, **kwargs)


class ItineraryListByLocation(generic.ListView):
    # def __init__(self):
    #     super().__init__()
    #     self.parsed_search_str = urllib.parse.unquote(self.kwargs['search_str'])

    def get_context_data(self, **kwargs):
        context = super(ItineraryListByLocation, self).get_context_data(**kwargs)
        context['category'] = 'All'
        context['all_categories'] = CategoryUtil.get_category_names()
        context['search_str'] = self.kwargs['search_str']
        context['form'] = LocationSearchForm()
        context['search_text'] = ' for "' + self.parsed_search_str + '"'
        return context

    def get_queryset(self):
        self.parsed_search_str = urllib.parse.unquote_plus(self.kwargs['search_str'])
        return Itinerary.objects.filter(title__contains=self.parsed_search_str)


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
        context['search_text'] = ' under "' + context['category'] + '" category'
        return context


class ItineraryDetailView(View):
    def get(self, request, *args, **kwargs):
        view = ItineraryDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = Favourite.as_view()
        return view(request, *args, **kwargs)


class ItineraryDetail(generic.DetailView):
    model = Itinerary

    def get_context_data(self, **kwargs):
        context = super(ItineraryDetail, self).get_context_data(**kwargs)
        itinerary = Itinerary.objects.get(id=self.kwargs['pk'])
        curr_user_id = self.request.user.id
        context['is_owner'] = itinerary.owner_id == curr_user_id
        context['form'] = FavouriteForm(initial={'fav': itinerary.favourited_by.filter(id=curr_user_id).exists()})
        return context

    def days_range(self):
        return range(1, self.get_object().total_duration + 1)

    def get_queryset(self):
        return Itinerary.objects.filter(Q(owner__user=self.request.user) |
                                        Q(shared_users__user=self.request.user) |
                                        Q(public_view=True)
                                        ).distinct()


class FavouriteForm(forms.Form):
    fav = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onclick': 'this.form.submit();'}),
                             label="I like this!")


class Favourite(SingleObjectMixin, FormView):
    template_name = 'triplan/itinerary_detail.html'
    success_url = reverse_lazy('triplan:itinerary_detail')
    model = Itinerary

    def get_form(self, **kwargs):
        return FavouriteForm(initial={'fav': Itinerary.objects.get(id=self.kwargs['pk']).favourited_by.filter(id=self.request.user.id).exists()})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super(Favourite, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        success_url = super(Favourite, self).form_valid(form)
        profile = Profile.objects.get(id=self.request.user.id)
        itinerary = Itinerary.objects.get(id=self.kwargs['pk'])
        # if form.instance.fav:
        #     itinerary.favourited_by.add(profile)
        # else:
        itinerary.favourited_by.remove(profile)
        itinerary.save()
        return success_url


class ItineraryCreate(generic.edit.CreateView):
    model = Itinerary
    fields = ['public_view', 'shared_users', 'title', 'preview_photo', 'start_date']
    success_url = reverse_lazy('triplan:itinerary_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        form.instance.save()
        return super(ItineraryCreate, self).form_valid(form)

    def get_form(self):
        form = super(ItineraryCreate, self).get_form()
        form.fields['shared_users'].queryset = Profile.objects.exclude(
            user=self.request.user)
        return form


class ItinerarySegmentCreate(generic.edit.CreateView):
    model = ItinerarySegment
    fields = ['photo', 'location', 'category', 'description', 'day_number', 'start_time', 'end_time', 'cost']
    widgets = {
        # "start_time": AdminTimeWidget(format='fa'),
        # "end_time": AdminTimeWidget(format='fa'),
        'start_time': forms.TimeInput(format='%H:%M %p'),
        'end_time': forms.TimeInput(format='%H:%M %p'),
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
    fields = ['title', 'preview_photo', 'start_date']
    success_url = reverse_lazy('triplan:itinerary_list')


class ItinerarySegmentEdit(generic.edit.UpdateView):
    template_name = 'triplan/itinerarysegment_edit.html'
    model = ItinerarySegment
    fields = ['photo', 'location', 'category', 'description', 'day_number', 'start_time', 'end_time', 'cost']
    widgets = {
        'start_time': forms.TimeInput(format='fa'),
        'end_time': forms.TimeInput(format='fa'),
    }

    def get_success_url(self):
        return reverse_lazy('triplan:itinerary_detail', args=[self.kwargs['itinerary_pk']])


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class ReviewCreate(generic.edit.CreateView):
    template_name = 'triplan/review_form.html'
    form = ReviewForm()
    fields = form.fields
    model = Review

    def get_context_data(self, **kwargs):
        context = super(ReviewCreate, self).get_context_data()
        context['itinerary'] = Itinerary.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.itinerary = Itinerary.objects.get(id=self.kwargs['pk'])
        form.instance.reviewer = self.request.user.profile
        form.instance.save()
        return super(ReviewCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('triplan:itinerary_detail', args=[self.kwargs['pk']])


class UserProfile(generic.list.ListView):
    template_name = 'triplan/itinerary_list.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['title'] = "Hi " + self.request.user.username + ", here are the itineraries owned by you"
        context['category'] = 'All'
        context['all_categories'] = CategoryUtil.get_category_names()
        context['form'] = LocationSearchForm()
        return context

    def get_queryset(self):
        return Itinerary.objects.all().filter(owner_id=self.request.user.id).order_by("-date_added")