from django.test import TestCase

from .models import Place

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