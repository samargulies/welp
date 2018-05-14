from django.contrib.gis import admin
import nested_admin

from .models import Place, Image, PlaceCategory, ImageCategory

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

class PlaceCategoryInline(nested_admin.NestedTabularInline):
    model = Place.categories.through
    extra = 0
    verbose_name = 'Category'
    verbose_name_plural = 'Categories'
    
class PlaceAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        ImagesInline,
        PlaceCategoryInline
    ]
    exclude = ('images','categories')

class ImageAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        ImageCategoryInline
    ]
    exclude = ('categories',)
    
admin.site.register(Place, PlaceAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ImageCategory)
admin.site.register(PlaceCategory)