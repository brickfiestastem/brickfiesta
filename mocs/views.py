from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import View, TemplateView
from mocs.models import Category, Moc, EventMoc, EventCategory
from django.shortcuts import render, redirect



class CategoriesListView(ListView):
    queryset = Category.objects.all()
    template_name = 'mocs/categories.html'


class CategoryListView(ListView):
    queryset = Category.objects.all()
    template_name = 'mocs/category.html'


class EventListView(ListView):
    queryset = Category.objects.all()
    template_name = 'mocs/category.html'


class EventCategoriesListView(ListView):
    def get(self, request, event_id):
        obj_eventcategory = EventCategory.objects.filter(event__id__exact=event_id)
        return render(request,
                      'mocs/categories.html',
                      {'object_list': obj_eventcategory, })


class MocDetail(DetailView):
    model = Moc

    def get_context_data(self, **kwargs):
        context = super(MocDetail, self).get_context_data(**kwargs)
        context['moc'] = (
                self.object.user.id == self.request.user.id)
        return context