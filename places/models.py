import os
from  django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from localflavor.us.models import USStateField, USZipCodeField
from sortedm2m.fields import SortedManyToManyField
from django_comments.moderation import CommentModerator, moderator
from django.urls import reverse
from autoslug import AutoSlugField
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.templatetags.thumbnail import thumbnail_url

class Category(models.Model):
	name = models.CharField(max_length=128)
	slug = AutoSlugField(populate_from='name', editable=True)
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
	image = ThumbnailerImageField(upload_to='%Y/%m/%d')
	title = models.CharField(max_length=256, blank=True)
	description = models.TextField(blank=True)
	alt = models.CharField(max_length=256, blank=True)
	attribution = models.CharField(max_length=256, blank=True)
	categories = models.ManyToManyField('ImageCategory', blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

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

	class Meta:
		ordering = ['sort_value']

	def __str__(self):
		return self.address


class PlaceChain(models.Model):
	title = models.CharField(max_length=256)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.title


class Building(models.Model):
	title = models.CharField(max_length=256)
	description = models.TextField(blank=True)

	def get_absolute_url(self):
		return reverse('places:building', args=[self.id])

	def __str__(self):
		return self.title


class Place(models.Model):
	title = models.CharField(max_length=256)
	slug = AutoSlugField(populate_from='title', editable=True, blank=True)
	description = models.TextField(blank=True)
	aliases = models.TextField(blank=True)
	images = SortedManyToManyField(Image)
	location = models.PointField(null=True, blank=True)
	categories = models.ManyToManyField('PlaceCategory', blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	chain = models.ForeignKey('PlaceChain', null=True, blank=True, on_delete=models.CASCADE)
	building = models.ForeignKey('Building', null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	class Meta:
	   ordering = ['-updated']

	def get_absolute_url(self):
		return reverse('places:detail', args=[self.slug])

	def map_properties(self):
		# for buildings, link to the building for the name and url
		# but still include the image and address from the place
		if self.building:
			properties = {
				"building_id": self.building.id,
				"url": self.building.get_absolute_url(),
				"title": self.building.title,
			}
		else:
			properties = {
				"url": self.get_absolute_url(),
				"title": self.title,
			}
		properties["id"] = self.id
		image = self.featured_image()
		if image:
			properties["image"] = thumbnail_url(image.image, 'map_thumbnail')
		if self.current_address():
			properties["address"] = self.current_address().address
		return properties

	def featured_image(self):
		return self.images.first()

	def displays_images_extended(self):
		return self.images.count() > 1

	def current_address(self):
		return self.address_set.first()

	def previous_addresses(self):
		return self.address_set.all()[1:]

	def other_chain_locations(self):
		if not self.chain:
			return
		return self.chain.place_set.exclude(pk=self.pk).all()[:5]

	def other_building_locations(self):
		if not self.building:
			return
		return self.building.place_set.exclude(pk=self.pk).all()[:5]

	# return 5 nearest places within 2km
	def nearby(self):
		if not self.location:
			return
		query = Place.objects.exclude(location__isnull=True)\
			.exclude(pk=self.pk)\
			.prefetch_related('address_set')\
			.filter(location__distance_lte=(self.location, D(km=2)))\
			.annotate(distance=Distance('location', self.location))\
			.order_by('distance')
		if self.building:
			query = query.exclude(building=self.building)
		return query[:5]

class PlaceModerator(CommentModerator):
	# email_notification = True
	auto_moderate_field = 'created'
	moderate_after = 0

# moderator.register(Place, PlaceModerator)
