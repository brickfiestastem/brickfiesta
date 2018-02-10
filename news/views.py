from django.views.generic import ListView
from .models import QuestionAnswer


class QuestionAnswerView(ListView):
    model = QuestionAnswer
