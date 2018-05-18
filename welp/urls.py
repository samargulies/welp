from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

import places.views as places_views

urlpatterns = [
    path('', places_views.IndexView.as_view(), name='index'),
    path('places/', include('places.urls')),
    path('admin/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),
    path('martor/', include('martor.urls')),
    path('comments/', include('django_comments.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)