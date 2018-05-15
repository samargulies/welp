from django.test import TestCase
from django.urls import resolve
from django.contrib.gis.geos import Point
from django.core.files import File

from .models import Place, Image, PlaceCategory, ImageCategory, Address

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
        first_place.location = Point(-34.0001, 20.9999)
        first_place.save()
        
        second_place = Place()
        second_place.title = 'place 2'
        second_place.description = 'description 2'
        second_place.save()
        
        saved_places = Place.objects.all()
        self.assertEqual(saved_places.count(), 2)
        self.assertEqual(saved_places[0].title, 'place 1')
        self.assertEqual(saved_places[0].description, 'description 1')
        self.assertEqual(saved_places[0].location.x, -34.0001)
        self.assertEqual(saved_places[0].location.y, 20.9999)
        self.assertEqual(saved_places[1].title, 'place 2')
        self.assertEqual(saved_places[1].description, 'description 2')
        self.assertEqual(saved_places[1].location, None)

    def test_getting_nearby_places(self):
        places = []
        for lng in [20, 20.0001, 20.001, 20.01, 20.1, 21]:
            places.append(Place.objects.create(title=f'place {lng}', description='description', location=Point(-34.0001, lng)))
        
        no_location_place = Place.objects.create(title='place', description='description')
        self.assertEqual(no_location_place.nearby(), None)
    
        # only 3 of the other places are within 5km
        self.assertEqual(places[0].nearby().count(), 3)
        self.assertEqual(list(places[0].nearby()), [places[1], places[2], places[3]])
        self.assertEqual(list(places[1].nearby()), [places[0], places[2], places[3]])
        self.assertEqual(list(places[2].nearby()), [places[0], places[1], places[3]])
        self.assertEqual(list(places[3].nearby()), [places[0], places[1], places[2]])
        self.assertEqual(list(places[4].nearby()), [])
        self.assertEqual(list(places[5].nearby()), [])
        
        places.append(Place.objects.create(title='place', description='description', location=Point(-33.999, 20)))
        self.assertEqual(places[0].nearby().count(), 4)
        
        places.append(Place.objects.create(title='place', description='description', location=Point(-33.999, 19.999)))
        self.assertEqual(places[0].nearby().count(), 5)
        
        # limited to 5 results
        places.append(Place.objects.create(title='place', description='description', location=Point(-33.999, 19.999)))
        self.assertEqual(places[0].nearby().count(), 5)
        
    def test_getting_place_current_address(self):
        test_place = Place.objects.create(title='place', description='description')
        
        addresses = []
        for c in 'abcde':
            addresses.append(Address.objects.create(address=c, city='Philadelphia', state='PA', place=test_place))
        
        self.assertEqual(test_place.address_set.all().count(), 5)
        self.assertEqual(test_place.current_address(), None)
        self.assertEqual(list(test_place.previous_addresses()), list(test_place.address_set.all()))
        self.assertEqual(test_place.previous_addresses().count(), 5)
        
        addresses[1].current = True
        addresses[1].save()
        
        self.assertEqual(test_place.current_address(), addresses[1])
        self.assertEqual(test_place.previous_addresses().count(), 4)
        
        addresses[0].current = True
        addresses[0].sort_value = 1
        addresses[0].save()
        
        self.assertEqual(test_place.current_address(), addresses[1])
        self.assertEqual(test_place.previous_addresses().count(), 3)
        
        addresses[1].sort_value = 2
        addresses[1].save()
        
        self.assertEqual(test_place.current_address(), addresses[0])
        
        
    def test_images_extended(self):
        new_place = Place.objects.create(title='place', description='description')
        images = [create_image(c) for c in '12']
        new_place.images.add(images[0])
        # is false if there are is one image
        self.assertFalse(new_place.displays_images_extended())
        # is true if there are multiple images
        new_place.images.add(images[1])
        self.assertTrue(new_place.displays_images_extended())
        

class CategoriesTest(TestCase):
    
    def setUp(self):
        self.parent_image_cat = ImageCategory.objects.create(name='parent', slug='parent')
        self.child_image_cat = ImageCategory.objects.create(name='child', 
            slug='child', 
            parent=self.parent_image_cat)
        
        self.parent_place_cat = PlaceCategory.objects.create(name='parent', slug='parent')
        self.child_place_cat = PlaceCategory.objects.create(name='child', 
            slug='child', 
            parent=self.parent_place_cat)
        
        self.images = [create_image(c) for c in '12345']
        self.place = Place.objects.create(title='place', description='description')
    
    def test_image_cat_heirarchy(self):
        self.assertEqual(self.child_image_cat.parent.name, 'parent')
        self.assertEqual(list(self.parent_image_cat.children.all()), 
            [self.child_image_cat])
            
    def test_place_cat_heirarchy(self):
        self.assertEqual(self.child_place_cat.parent.name, 'parent')
        self.assertEqual(list(self.parent_place_cat.children.all()), 
            [self.child_place_cat])
    
    def test_add_child_image_cats(self):
        
        self.assertEqual("", self.images[0].classes())
            
        self.images[0].categories.add(self.child_image_cat)
        
        self.assertEqual(list(self.images[0].categories.all()), [self.child_image_cat])
        self.assertIn(self.child_image_cat.slug, self.images[0].classes())      
    
    def test_add_child_place_cats(self):
        self.place.categories.add(self.child_place_cat)
        self.assertEqual(list(self.place.categories.all()), [self.child_place_cat])
        

class ImagesModelTest(TestCase):
    
    def setUp(self):
        self.images = [create_image(c) for c in '12345']
    
    def test_adding_images_to_place(self):
             
        new_place = Place.objects.create(title='place', description='description')
        new_place.images.add(self.images[0], self.images[1])
        
        saved_place = Place.objects.first()
        self.assertEqual(saved_place, new_place)
        
        self.assertEqual(saved_place.images.count(), 2)
        saved_place_images = saved_place.images.all()
        self.assertEqual(saved_place_images[0].title, 'image 1')
        self.assertEqual(saved_place_images[0].attribution, 'attribution 1')
        self.assertEqual(saved_place_images[1].title, 'image 2')
        self.assertEqual(saved_place_images[1].attribution, 'attribution 2')  
        
    def test_image_ordering(self):

        new_place = Place.objects.create(title='place', description='description')
        new_place.images.add(self.images[0], self.images[1], self.images[2])
        
        new_place_images = new_place.images.all()
        
        self.assertEqual(list(new_place.images.all()), [
            self.images[0], 
            self.images[1], 
            self.images[2]])
            
        new_place.images.add(self.images[0])
        
        self.assertEqual(list(new_place.images.all()), [
            self.images[0], 
            self.images[1], 
            self.images[2]])
        
        new_place.images.clear()
        self.assertEqual(list(new_place.images.all()), [])
           
        
class HomepageTest(TestCase):
    
    def test_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'places/index.html')
       
        
class PlacePageTest(TestCase):
    
    def setUp(self):
        self.test_place = Place.objects.create(title='place 1', 
            description='description 1',
            location=Point(-34.0001, 20.9999))
            
        self.nearby_test_place = Place.objects.create(title='place 2', 
            description='description 2',
            location=Point(-34, 21)) 
    
    def test_place_template(self):
        response = self.client.get(f'/places/{self.test_place.id}/')
        self.assertTemplateUsed(response, 'places/place_detail.html')
        
    def test_correct_place_in_view(self):
        response = self.client.get(f'/places/{self.test_place.id}/')
        self.assertContains(response, 'place 1')
    
    def test_place_template_displays_nearby(self):
        response = self.client.get(f'/places/{self.test_place.id}/')
        self.assertContains(response, 'place 2')
    
    # disabled because it breaks the template to use fake images
    # def test_correct_images_in_place_view(self):
    #     first_image = create_image("1")
    #     second_image = create_image("2")
    #
    #     self.test_place.images.add(first_image, second_image)
    #
    #     response = self.client.get(f'/places/{self.test_place.id}/')
    #     self.assertContains(response, first_image.image.url)
    #     self.assertContains(response, first_image.attribution)
    #     self.assertContains(response, second_image.image.url)
    #     self.assertContains(response, second_image.attribution)
    #     self.assertContains(response, "-34.0001,20.9999")
        
    
    