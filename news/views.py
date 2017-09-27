from django.shortcuts import render

# Create your views here.
def index(request):
    # obj_locations = Location.objects.all().order_by('postal_code')
    return render(request, 'mocs/index.html', {'sample': 'sample'})