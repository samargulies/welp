from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic, View
from . import tiler

SRID_LNGLAT = 4326
SRID_SPHERICAL_MERCATOR = 3857  
  
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

class MapView(generic.TemplateView):
    template_name = 'places/map.html'

def point_in_tile(tile_bounds, point):
    # `mapbox-vector-tile` has a hardcoded tile extent of 4096 units.
    MVT_EXTENT = 4096

    # We need tile bounds in spherical mercator
    assert tile_bounds.srid == SRID_SPHERICAL_MERCATOR

    # And we need the line to be in a known projection so we can re-project
    assert point.srid is not None
    point.transform(SRID_SPHERICAL_MERCATOR)

    (x0, y0, x_max, y_max) = tile_bounds.extent
    x_span = x_max - x0
    y_span = y_max - y0

    return Point(int((point.x - x0) * MVT_EXTENT / x_span),
            int((point.y - y0) * MVT_EXTENT / y_span))
          
class MapTilesView(View):
    
    def get(self, request, *args, **kwargs):
        xyz = (int(self.kwargs['x']), int(self.kwargs['y']), int(self.kwargs['z']))
        tile = tiler.encode_objects_for_tile(Place, xyz=xyz, properties=['id', 'title'])   
        return HttpResponse(tile)
        