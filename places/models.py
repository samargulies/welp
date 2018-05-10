from django.db import models

class Place(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()