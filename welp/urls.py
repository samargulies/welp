from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

import places.views as places_views

PAGE_CACHE_DURATION = 15 * 60

urlpatterns = [
    path('', cache_page(PAGE_CACHE_DURATION)(places_views.IndexView.as_view()), name='index'),
    path('places/', include('places.urls')),
    path('admin/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),
    path('martor/', include('martor.urls')),
    path('comments/', include('django_comments.urls')),
    
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns