from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='user_images/%Y/%m/%d')
    title = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    alt = models.CharField(max_length=256, blank=True)
    attribution = models.CharField(max_length=256, blank=True)
    license = models.CharField(max_length=256, blank=True)
    
    def __str__(self):
        return self.title
        
class Place(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    images = models.ManyToManyField(Image)
    
    def __str__(self):
        return self.title