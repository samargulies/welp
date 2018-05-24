from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic, View
from django.contrib.postgres.search import SearchVector
from . import map_tiler
from .models import Place, Image, PlaceCategory, PlaceChain, Building

PAGINATE_BY = 20

class IndexView(generic.ListView):
    model = Place
    template_name = 'places/place_list.html'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        return Place.objects.prefetch_related('images', 'address_set')


class DetailView(generic.DetailView):
    model = Place

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nearby'] = context['place'].nearby()
        context['other_building_locations'] = context['place'].other_building_locations()
        context['other_chain_locations'] = context['place'].other_chain_locations()
        return context

    def get_queryset(self):
        return Place.objects.prefetch_related('images', 'address_set', 'categories').select_related('building', 'chain').filter(slug=self.kwargs['slug'])


class CategoryView(generic.DetailView):
    model = PlaceCategory
    template_name = 'places/place_list.html'
    context_object_name = 'category'
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Category: {}".format(context['category'].name)
        context['place_list'] = Place.objects.prefetch_related('images', 'address_set')\
                                    .filter(categories__in=[context['category']])
        return context


class SearchView(generic.ListView):
    model = Place
    template_name = 'places/place_list.html'
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Search"
        context['search'] = self.request.GET.get('s')
        return context

    def get_queryset(self):
        return Place.objects.annotate(
            search=SearchVector(
                'title', 'aliases', 'description', 'images__title', 'images__description', 'aliases',
                'chain__title', 'building__title', 'address__address'
            )).prefetch_related('images', 'address_set')\
            .filter(search=self.request.GET.get('s'))

class ChainView(generic.DetailView):
    model = PlaceChain
    template_name = 'places/place_list.html'
    context_object_name = 'chain'
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "{} Locations".format(context['chain'].title)
        context['description'] = context['chain'].description
        context['place_list'] = context['chain'].place_set.all()
        return context

class BuildingView(generic.DetailView):
    model = Building
    template_name = 'places/place_list.html'
    context_object_name = 'building'
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['building'].title
        context['description'] = context['building'].description
        context['place_list'] = context['building'].place_set.all()
        return context

class MapView(generic.TemplateView):
    template_name = 'places/map.html'

class MapTilesView(View):
    def get(self, request, *args, **kwargs):
        xyz = (int(self.kwargs['x']), int(self.kwargs['y']), int(self.kwargs['z']))
        tile = map_tiler.encode_objects_for_tile(xyz=xyz)
        return HttpResponse(tile, content_type='application/vnd.mapbox-vector-tile')
