from django.shortcuts import render, get_object_or_404
from mocs.models import Category, Moc, EventCategory


def index(request):
    # obj_locations = Location.objects.all().order_by('postal_code')
    return render(request, 'mocs/index.html', {'sample': 'sample'})

def add(request):
    #obj_moc = get_object_or_404(Moc, id=moc_id)
    return render(request, 'mocs/details.html', {'moc': ''})

def edit(request, moc_id):
    obj_moc = get_object_or_404(Moc, id=moc_id)
    return render(request, 'mocs/details.html', {'moc': obj_moc})

def details(request, moc_id):
    obj_moc = get_object_or_404(Moc, id=moc_id)
    return render(request, 'mocs/details.html', {'moc': obj_moc})

def categories(request):
    return render(request, 'mocs/categories.html', {'sample': 'sample'})

def category(request, category_id):
    obj_category = get_object_or_404(Category, id=category_id)
    return render(request, 'mocs/category.html', {'': 'sample'})    

# Create your views here.
