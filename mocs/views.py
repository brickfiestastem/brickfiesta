from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import View, TemplateView
from mocs.models import Category, Moc, EventMoc, EventCategory
from django.shortcuts import render, redirect
from shop.utils import check_recaptcha
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class CategoriesListView(ListView):
    queryset = Category.objects.all()
    template_name = 'mocs/categories.html'


class CategoryListView(ListView):
    model = Moc
    template_name = 'mocs/category.html'
    paginate_by = 10

    def get_queryset(self):
        return EventMoc.objects.filter(category__in=EventCategory.objects.filter(category_id=self.kwargs['pk'])).distinct()



class EventListView(ListView):
    queryset = Category.objects.all()
    template_name = 'mocs/category.html'


class EventCategoriesListView(ListView):
    def get(self, request, event_id):
        obj_eventcategory = EventCategory.objects.filter(
            event__id__exact=event_id)
        return render(request,
                      'mocs/categories.html',
                      {'object_list': obj_eventcategory, })


class MocDetail(DetailView):
    model = Moc

    def get_context_data(self, **kwargs):
        context = super(MocDetail, self).get_context_data(**kwargs)
        context['moc_owner'] = (
            self.object.user.id == self.request.user.id)
        return context


@method_decorator(login_required, name='dispatch')
class MocAddView(CreateView):
    model = Moc
    fields = ('title', 'description', 'height', 'length',
              'width', 'viewable_sides', 'url_photo', 'url_flickr',
              'year_build', 'year_retired')
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
    fields = ('title', 'description', 'height', 'length',
              'width', 'viewable_sides', 'url_photo', 'url_flickr',
              'year_build', 'year_retired')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not check_recaptcha(self.request):
            form.add_error(
                None, 'You failed the human test. Try the reCAPTCHA again.')
            return super().form_invalid(form)
        return super().form_valid(form)
