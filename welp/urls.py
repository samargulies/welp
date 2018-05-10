from django.contrib import admin
from django.urls import include, path

import places.views as places_views

urlpatterns = [
    path('', places_views.IndexView.as_view(), name='index'),
    path('places/', include('places.urls')),
    path('admin/', admin.site.urls),
]
