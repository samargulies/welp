import os
from  django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.db import models
from django.contrib.gis.measure import D
from localflavor.us.models import USStateField, USZipCodeField
from sortedm2m.fields import SortedManyToManyField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, SmartResize

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
     class Meta:
         verbose_name = 'Image Category'
         verbose_name_plural = 'Image Categories'

    
class Image(models.Model):
    image = models.ImageField(upload_to='%Y/%m/%d')
    image_thumbnail = ImageSpecField(source='image',
        processors=[SmartResize(320, 320, upscale=True)],
        format='JPEG',
        options={'quality': 85})
    image_medium = ImageSpecField(source='image',
        processors=[ResizeToFit(700, 600, upscale=False)],
        format='JPEG',
        options={'quality': 90})
    image_large = ImageSpecField(source='image',
        processors=[ResizeToFit(1400, 1100, upscale=False)],
        format='JPEG',
        options={'quality': 90})
                                      
    title = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    alt = models.CharField(max_length=256, blank=True)
    attribution = models.CharField(max_length=256, blank=True)
    license = models.CharField(max_length=256, blank=True)
    categories = models.ManyToManyField('ImageCategory', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def safe_thumbnail(self):
        try:
            if self.image_thumbnail.width:
                return self.image_thumbnail
        except:
            return
    
    def safe_medium(self):
        try:
            if self.image_medium.width:
                return self.image_medium
        except:
            return
    
    def safe_large(self):
        try:
            if self.image_large.width:
                return self.image_large
        except:
            return       
    
    # generate html classes based on the image and its categories
    def classes(self):
        classlist = []
        for category in self.categories.all():
            classlist.append(f"category-{category.slug}")
        
        return ' '.join(classlist)
        
    def __str__(self):
        return self.title or os.path.basename(self.image.name)

class PlaceCategory(Category):
    class Meta:
        verbose_name = 'Place Category'
        verbose_name_plural = 'Place Categories'

class Address(models.Model):
    address = models.CharField(max_length=64)
    address_2 = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64)
    state = USStateField(default="PA")
    zipcode = USZipCodeField(blank=True)
    place = models.ForeignKey('Place', on_delete=models.CASCADE)
    sort_value = models.SmallIntegerField(default=0)
    current = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['sort_value']
    
    def __str__(self):
        return self.address
        
class Place(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    images = SortedManyToManyField(Image)
    location = models.PointField(null=True)
    categories = models.ManyToManyField('PlaceCategory', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def featured_image(self):
        return self.images.first()
        
    def displays_images_extended(self):
        return self.images.count() > 1
    
    def current_address(self):
        return self.address_set.filter(current=True).first()
    
    def previous_addresses(self):
        return self.address_set.filter(current=False)
    
    # return 5 nearest places within 5km
    def nearby(self):
        if not self.location:
            return
        
        return Place.objects.exclude(location__isnull=True).exclude(pk=self.pk).filter(location__distance_lte=(self.location, D(km=5)))[:5]
    
    def __str__(self):
        return self.title