from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic, View
from . import map_tiler

SRID_LNGLAT = 4326
SRID_SPHERICAL_MERCATOR = 3857  
  
from .models import Place, Image, PlaceCategory, PlaceChain

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
        context['title'] = "Category: {}".format(context['category'].name)
        context['place_list'] = Place.objects.filter(categories__in=[context['category']])
        return context

class ChainView(generic.DetailView):
    model = PlaceChain
    template_name = 'places/place_list.html'
    context_object_name = 'chain'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "{} Locations".format(context['chain'].title)
        context['description'] = context['chain'].description
        context['place_list'] = context['chain'].place_set.all()
        return context
        
class MapView(generic.TemplateView):
    template_name = 'places/map.html'
  
class MapTilesView(View):
    def get(self, request, *args, **kwargs):
        xyz = (int(self.kwargs['x']), int(self.kwargs['y']), int(self.kwargs['z']))
        tile = map_tiler.encode_objects_for_tile(Place, xyz=xyz)   
        return HttpResponse(tile)
        