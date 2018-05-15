from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Place, Image, PlaceCategory

class IndexView(generic.ListView):
    model = Place
    template_name = 'places/place_list.html'

class DetailView(generic.DetailView):
    model = Place
    
class CategoryView(generic.DetailView):
    model = PlaceCategory
    template_name = 'places/place_list.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "{} Establishments".format(context['category'].name)
        context['place_list'] = Place.objects.filter(categories__in=[context['category']])
        return context
    