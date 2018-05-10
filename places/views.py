from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Place

class IndexView(generic.ListView):
    model = Place
    template_name = 'places/index.html'

class DetailView(generic.DetailView):
    model = Place