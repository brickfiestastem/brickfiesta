from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import View, TemplateView
from afol.models import Fan
from mocs.models import Category, Moc, EventMoc, EventCategory
from event.models import Event
from django.shortcuts import render, redirect
from shop.utils import check_recaptcha
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from mocs.forms import MOCsForm


class CategoryListView(ListView):
    model = Moc
    template_name = 'mocs/category.html'
    paginate_by = 20

    def get(self, request, event_id, category_id):
        obj_eventcategory = EventCategory.objects.filter(
            event=event_id,
            category=category_id).get()
        obj_mocs = EventMoc.objects.filter(
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


class MocDetail(DetailView):
    model = Moc

    def get_context_data(self, **kwargs):
        context = super(MocDetail, self).get_context_data(**kwargs)
        obj_fan = Fan.objects.filter(id=self.object.creator.id).get()
        if obj_fan.user == self.request.user:
            context['moc_owner'] = True
        return context


@method_decorator(login_required, name='dispatch')
class MocAddView(CreateView):
    model = Moc
    fields = ('title', 'description', 'height', 'length',
              'width', 'viewable_sides', 'url_photo', 'url_flickr',
              'year_built', 'year_retired')
    success_url = '/mocs/afol'

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not check_recaptcha(self.request):
            form.add_error(
                None, 'You failed the human test. Try the reCAPTCHA again.')
            return super().form_invalid(form)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class MocUpdateView(UpdateView):
    model = Moc
    form_class = MOCsForm
    fields = ('title', 'description', 'height', 'length',
              'width', 'viewable_sides', 'url_photo', 'url_flickr',
              'year_built', 'year_retired')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not check_recaptcha(self.request):
            form.add_error(
                None, 'You failed the human test. Try the reCAPTCHA again.')
            return super().form_invalid(form)
        return super().form_valid(form)
