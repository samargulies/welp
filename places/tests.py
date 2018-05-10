from django.test import TestCase
from django.urls import resolve

from .models import Place, Image

def create_image(title):
    image = Image()
    image.image = title + '.jpg'
    image.title = 'image ' + title
    image.description = 'description ' + title
    image.alt = 'alt ' + title
    image.attribution = 'attribution ' + title
    image.license = 'license ' + title
    image.save()
    
    return image

class PlaceModelTest(TestCase):
        
    def test_saving_and_getting_places(self):
        first_place = Place()
        first_place.title = 'place 1'
        first_place.description = 'description 1'
        first_place.save()
        
        second_place = Place()
        second_place.title = 'place 2'
        second_place.description = 'description 2'
        second_place.save()
        
        saved_places = Place.objects.all()
        self.assertEqual(saved_places.count(), 2)
        self.assertEqual(saved_places[0].title, first_place.title)
        self.assertEqual(saved_places[0].description, first_place.description)
        self.assertEqual(saved_places[1].title, second_place.title)
        self.assertEqual(saved_places[1].description, second_place.description)


class ImagesModelTest(TestCase):
    
    def test_adding_images_to_place(self):
        
        first_image = create_image("1")
        second_image = create_image("2")
             
        new_place = Place.objects.create(title='place', description='description')
        new_place.images.add(first_image, second_image)
        
        saved_place = Place.objects.first()
        self.assertEqual(saved_place, new_place)
        
        self.assertEqual(saved_place.images.count(), 2)
        saved_place_images = saved_place.images.all()
        self.assertEqual(saved_place_images[0].title, 'image 1')
        self.assertEqual(saved_place_images[0].attribution, 'attribution 1')
        self.assertEqual(saved_place_images[1].title, 'image 2')
        self.assertEqual(saved_place_images[1].attribution, 'attribution 2')
        
        
class HomepageTest(TestCase):
    
    def test_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'places/index.html')
        
        
class PlacePageTest(TestCase):
    
    def test_place_template(self):
        first_place = Place.objects.create(title='place 1', description='description 1')        
        response = self.client.get(f'/places/{first_place.id}/')
        self.assertTemplateUsed(response, 'places/place_detail.html')
        
    def test_correct_place_in_view(self):
        first_place = Place.objects.create(title='place 1', description='description 1')        
        response = self.client.get(f'/places/{first_place.id}/')
        self.assertContains(response, 'place 1')
        
    def test_correct_images_in_place_view(self):
        first_image = create_image("1")
        second_image = create_image("2")
             
        first_place = Place.objects.create(title='place 1', description='description 1')        
        first_place.images.add(first_image, second_image)
        
        response = self.client.get(f'/places/{first_place.id}/')
        self.assertContains(response, first_image.image.url)
        self.assertContains(response, first_image.attribution)
        self.assertContains(response, second_image.image.url)
        self.assertContains(response, second_image.attribution)
        
    
    