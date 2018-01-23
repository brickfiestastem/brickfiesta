from django.shortcuts import render
from django.views.generic import ListView
from .models import QuestionAnswer 
# Create your views here.

class QuestionAnswerView(ListView):
    model = QuestionAnswer
