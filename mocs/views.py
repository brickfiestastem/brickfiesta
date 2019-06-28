import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, BaseCreateView, DeleteView
from django.views.generic.list import ListView
from django.contrib import messages

from afol.models import Fan
from event.models import Event
from mocs.forms import MOCsForm, PublicVoteForm, FanVoteForm
from mocs.models import Moc, MocCategories, EventCategory, Vote, PublicVote
from shop.utils import check_recaptcha


class CategoryListView(ListView):
    model = Moc
    template_name = 'mocs/category.html'
    paginate_by = 20

    def get(self, request, event_id, category_id):
        obj_eventcategory = EventCategory.objects.filter(
            event=event_id,
            category=category_id).get()
        obj_mocs = MocCategories.objects.filter(
            category=obj_eventcategory, moc__is_public=True).distinct()
        return render(request,
                      'mocs/category.html',
                      {'object_list': obj_mocs, 'obj_event': obj_eventcategory})


class EventListView(ListView):
    queryset = Event.objects.all().order_by('-start_date')
    template_name = 'mocs/events.html'


class EventCategoriesListView(ListView):
    def get(self, request, event_id):
        obj_eventcategory = EventCategory.objects.filter(
            event__id__exact=event_id).order_by('category__title')
        return render(request,
                      'mocs/categories.html',
                      {'object_list': obj_eventcategory, 'obj_event': obj_eventcategory.first()})


class MocDetail(DetailView, BaseCreateView):
    model = Moc
    fields = '__all__'

    def get_success_url(self):
        return reverse('mocs:details', kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super(MocDetail, self).get_context_data(**kwargs)
        obj_fan = Fan.objects.filter(id=self.object.creator.id).get()
        obj_moc = self.get_object()
        obj_moccategories = MocCategories.objects.filter(
            moc=obj_moc).order_by('category__event__start_date')
        context['moc_categories'] = obj_moccategories
        context['not_retired'] = False
        context['moc_owner'] = False
        if obj_moc.year_retired and obj_moc.year_built > obj_moc.year_retired:
            context['not_retired'] = True
        if obj_fan.user == self.request.user:
            context['moc_owner'] = True
        return context


class MocPublicVote(CreateView):
    model = PublicVote
    form_class = PublicVoteForm

    def get_context_data(self, **kwargs):
        context = super(MocPublicVote, self).get_context_data(**kwargs)
        context['moc'] = Moc.objects.get(id=self.kwargs['moc'])
        context['eventcategory'] = EventCategory.objects.get(
            id=self.kwargs['eventcategory'])
        return context

    def get_initial(self):
        initial = super(MocPublicVote, self).get_initial()
        initial = initial.copy()
        str_session = self.request.session.get(
            'public_vote_id', str(uuid.uuid4()))
        self.request.session['public_vote_id'] = str_session
        initial['session'] = str_session
        initial['moc'] = Moc.objects.get(id=self.kwargs['moc'])
        initial['category'] = EventCategory.objects.get(
            id=self.kwargs['eventcategory'])
        return initial

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, "Vote Recorded!")
        return reverse('mocs:details', kwargs={'pk': self.kwargs['moc']})


@method_decorator(login_required, name='dispatch')
class MocDeleteVoteView(DeleteView):
    model = Vote

    def get_success_url(self):
        return reverse('mocs:details', kwargs={'pk': self.get_object().id})


@method_decorator(login_required, name='dispatch')
class MocFanVote(CreateView):
    model = Vote
    form_class = FanVoteForm

    def get_context_data(self, **kwargs):
        context = super(MocFanVote, self).get_context_data(**kwargs)
        context['moc'] = Moc.objects.get(id=self.kwargs['moc'])
        context['eventcategory'] = EventCategory.objects.get(
            id=self.kwargs['eventcategory'])
        return context

    def get_form_kwargs(self):
        kwargs = super(MocFanVote, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super(MocFanVote, self).get_initial()
        initial = initial.copy()
        initial['moc'] = Moc.objects.get(id=self.kwargs['moc'])
        initial['category'] = EventCategory.objects.get(
            id=self.kwargs['eventcategory'])
        return initial

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, "Vote Recorded!")
        return reverse('mocs:details', kwargs={'pk': self.kwargs['moc']})


class MocTableTent(DetailView):
    model = MocCategories
    template_name = 'mocs/moc_table_tent.html'


@method_decorator(login_required, name='dispatch')
class MocAddView(CreateView):
    model = Moc
    form_class = MOCsForm
    success_url = '/afol/mocs'

    def get_form_kwargs(self):
        kwargs = super(MocAddView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not check_recaptcha(self.request):
            form.add_error(
                None, 'You failed the human test. Try the reCAPTCHA again.')
            return super().form_invalid(form)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class MocUpdateView(UpdateView):
    model = Moc
    form_class = MOCsForm
    success_url = '/afol/mocs'

    def get_form_kwargs(self):
        kwargs = super(MocUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not check_recaptcha(self.request):
            form.add_error(
                None, 'You failed the human test. Try the reCAPTCHA again.')
            return super().form_invalid(form)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class MocUpdateCategoryView(UpdateView):
    model = MocCategories
    fields = ['category', ]
    success_url = '/afol/mocs'

    def form_valid(self, form):
        obj_eventcategory = EventCategory.objects.filter(
            event=form.instance.category.event)
        if MocCategories.objects.filter(moc=form.instance.moc, category__in=obj_eventcategory).count() > 1:
            form.add_error(
                "category", 'You cannot pick more than one category per event.')
            return super(MocUpdateCategoryView, self).form_invalid(form)
        if not check_recaptcha(self.request):
            form.add_error(
                None, 'You failed the human test. Try the reCAPTCHA again.')
            return super(MocUpdateCategoryView, self).form_invalid(form)
        return super(MocUpdateCategoryView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class MocCreateCategoryView(CreateView):
    model = MocCategories
    fields = ['category', ]
    success_url = '/afol/mocs'

    def dispatch(self, request, *args, **kwargs):
        self.moc = Moc.objects.get(pk=kwargs['pk'])
        return super(MocCreateCategoryView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.moc = self.moc
        obj_eventcategory = EventCategory.objects.filter(
            event=form.instance.category.event)
        if MocCategories.objects.filter(moc=self.moc, category__in=obj_eventcategory).exists():
            form.add_error(
                "category", 'You cannot pick more than one category per event.')
            return super(MocCreateCategoryView, self).form_invalid(form)
        if not check_recaptcha(self.request):
            form.add_error(
                None, 'You failed the human test. Try the reCAPTCHA again.')
            return super(MocCreateCategoryView, self).form_invalid(form)
        return super(MocCreateCategoryView, self).form_valid(form)
