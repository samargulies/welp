from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from . import views

PAGE_CACHE_DURATION = 15 * 60

app_name = 'places'
urlpatterns = [
    path('', cache_page(PAGE_CACHE_DURATION)(views.PlaceIndexView.as_view()), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('chains/<int:pk>/', cache_page(PAGE_CACHE_DURATION)(views.ChainView.as_view()), name='chain'),
    path('building/<int:pk>/', cache_page(PAGE_CACHE_DURATION)(views.BuildingView.as_view()), name='building'),
    path('category/<slug:slug>/', cache_page(PAGE_CACHE_DURATION)(views.CategoryView.as_view()), name='category'),
    path('map/', cache_page(PAGE_CACHE_DURATION)(views.MapView.as_view()), name='map'),
    re_path(r'^map/tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+)/$',
        cache_page(PAGE_CACHE_DURATION)(views.MapTilesView.as_view()), name='map-tiles'),
    path('<slug:slug>/', cache_page(PAGE_CACHE_DURATION)(views.DetailView.as_view()), name='detail'),
]
