from django.contrib.gis.db import models
from django.contrib.gis import admin
import nested_admin
from martor.widgets import AdminMartorWidget
from imagekit.admin import AdminThumbnail
from leaflet.admin import LeafletGeoAdminMixin

from .models import Place, Image, PlaceCategory, ImageCategory, Address

class ImageCategoryInline(nested_admin.NestedTabularInline):
    model = Image.categories.through
    extra = 0
    verbose_name = 'Category'
    verbose_name_plural = 'Categories'
   
class ImagesInline(nested_admin.NestedTabularInline):
    model = Place.images.through
    sortable_field_name = 'sort_value'
    extra = 0
    verbose_name = 'Image'
    verbose_name_plural = 'Images'
    # inlines = [
    #     ImageCategoryInline
    # ]
    exclude = ('categories',)

class AddressesInline(nested_admin.NestedTabularInline):
    model = Address
    sortable_field_name = 'sort_value'
    extra = 0
    
class PlaceCategoryInline(nested_admin.NestedTabularInline):
    model = Place.categories.through
    extra = 0
    verbose_name = 'Category'
    verbose_name_plural = 'Categories'
    
class PlaceAdmin(LeafletGeoAdminMixin, nested_admin.NestedModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    
    settings_overrides = {
       'DEFAULT_CENTER': (39.95, -75.16),
       'DEFAULT_ZOOM': 14,
       'TILES': [('', 
           'https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoic2FtYXJndWxpZXMiLCJhIjoiY2E3c2laTSJ9.v0zuT22Dw8b72E-TRFbFaQ',
           '')]
    }
    
    inlines = [
        AddressesInline,
        ImagesInline,
        PlaceCategoryInline
    ]
    exclude = ('images','categories')

class ImageAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        ImageCategoryInline
    ]
    admin_thumbnail = AdminThumbnail(image_field='image_medium')
    list_display = ('__str__', 'admin_thumbnail')
    readonly_fields = ('admin_thumbnail',)
    exclude = ('categories',)

    
admin.site.register(Place, PlaceAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ImageCategory)
admin.site.register(PlaceCategory)