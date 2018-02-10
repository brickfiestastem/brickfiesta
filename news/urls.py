from django.urls import path
from .views import QuestionAnswerView
from .models import Article
from django.views.generic.dates import ArchiveIndexView
# TODO: Implement feed and Year Archive View
# from django.views.generic.dates import YearArchiveView

app_name = 'news'

urlpatterns = [
    path('', ArchiveIndexView.as_view(model=Article,
                                      date_field='created', paginate_by=5), name='index'),
    path('faq/', QuestionAnswerView.as_view(), name='questions'),
]

'''
path('<int:year>/', YearArchiveView.as_view(model=Article,
                                            date_field='created',
                                            paginate_by = 5), name='year'),
'''
