from django.contrib.gis import admin

from .models import Place, Image

class ImagesInline(admin.TabularInline):
    model = Place.images.through
    extra = 1

class PlaceAdmin(admin.OSMGeoAdmin):
    inlines = [
        ImagesInline,
    ]
    exclude = ('images',)


admin.site.register(Place, PlaceAdmin)
admin.site.register(Image)