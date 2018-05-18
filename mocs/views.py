from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import View, TemplateView
from mocs.models import Category, Moc, EventMoc, EventCategory


class CategoryListView(ListView):
    queryset = Category.objects.all()
    template_name = 'vendor/sponsor_list.html'
