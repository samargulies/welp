from django.urls import path, re_path

from . import views

app_name = 'places'
urlpatterns = [
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('map/', views.MapView.as_view(), name='map'),
    re_path(r'^map/tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+)/$', views.MapTilesView.as_view(), name='map-tiles'),
]