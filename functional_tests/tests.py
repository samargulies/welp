import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.gis.geos import Point

from places.models import Place, Image

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    
    def setup_db(self):
        first_image = Image()
        first_image.image = 'test1.jpg'
        first_image.title = 'image 1'
        first_image.description = 'caption 1'
        first_image.alt = 'alt 1'
        first_image.attribution = 'attribution 1'
        first_image.license = 'license 1'
        first_image.save()
        
        first_place = Place.objects.create(title="place 1", 
            description="description 1", 
            location=Point(-34.0001, -108.1234))
        first_place.images.add(first_image)
        
        Place.objects.create(title="place 2", description="description 2")
    
    def setUp(self):
        self.setup_db()
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()
    
    def wait_for_text(self, css_selector, search_text):
        start_time = time.time()
        while True:
            try:
                elements = self.browser.find_elements_by_css_selector(css_selector)
                self.assertIn(search_text, [element.text for element in elements])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)
    
    def test_can_browse_places(self):
        # rachel visits the homepage
        self.browser.get(self.live_server_url)
        self.assertIn('Welp', self.browser.title)
        
        # she sees a list of places
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('place 1', page_text)
        self.assertIn('place 2', page_text)
        
        # she clicks on a place to view more details
        self.browser.find_element_by_css_selector('.place a').click()
        self.wait_for_text('.place__description', 'description 1')
        self.assertIn('place 1', self.browser.title)
        
        place_detail_url = self.browser.current_url
        self.assertRegex(place_detail_url, '/places/\d+')
        
        # she views images
        page_images = self.browser.find_elements_by_tag_name('img')
        self.assertIn(True, 
            ['test1.jpg' in image.get_attribute('src') for image in page_images], 
            "img src for image not found on page")
        
        # she sees the attribution of the images
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('attribution 1', page_text)
        
        # she sees the location of the place
        self.assertIn('-34.0001, -108.1234', page_text)
        
        # she views more metadata for the place
        
        # she sees nearby places
        
        # she sees other related places
        
        self.assertEqual('Finish writing tests', False)
        
    def test_can_add_place(self):
        self.assertEqual('Write admin tests', False)
        