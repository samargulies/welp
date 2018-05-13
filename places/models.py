from django.contrib.gis.db import models
from sortedm2m.fields import SortedManyToManyField

class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    class Meta:
        abstract = True
        unique_together = ('slug', 'parent',)
        verbose_name_plural = 'categories'

    def __str__(self):
        full_path = [self.name]
        parent_cat = self.parent                          
        while parent_cat is not None:
            full_path.append(parent_cat.name)
            parent_cat = parent_cat.parent
        return '/'.join(full_path[::-1])

class ImageCategory(Category):
    pass
    
class Image(models.Model):
    image = models.ImageField(upload_to='user_images/%Y/%m/%d')
    title = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    alt = models.CharField(max_length=256, blank=True)
    attribution = models.CharField(max_length=256, blank=True)
    license = models.CharField(max_length=256, blank=True)
    categories = models.ManyToManyField('ImageCategory')
    
    def __str__(self):
        return self.title

class PlaceCategory(Category):
    pass
        
class Place(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    images = SortedManyToManyField(Image)
    location = models.PointField(null=True)
    categories = models.ManyToManyField('PlaceCategory')
    
    
    def __str__(self):
        return self.title