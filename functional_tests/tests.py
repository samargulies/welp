from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()
    
    def wait_for_text_in_list(self, search_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('list-table')
                rows = table.find_elements_by_tag_name('tr')  
                self.assertIn(search_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)
        
    def test_can_start_a_list_for_one_user(self):  
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        # she is invited to enter a to-do item
        inputbox = self.browser.find_element_by_id('list-new-item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        
        # she types "buy peacock feathers"
        inputbox.send_keys('Buy peacock feathers')
        
        # when she hits enter, the page updates to show "1: buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)
        
        self.wait_for_text_in_list('1: Buy peacock feathers')
        
        # the user adds a second item
        inputbox = self.browser.find_element_by_id('list-new-item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        
        # the page updates to show both items
        self.wait_for_text_in_list('1: Buy peacock feathers')
        self.wait_for_text_in_list('2: Use peacock feathers to make a fly')
        
    def test_multiple_user_lists_at_multiple_urls(self):
        # user starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('list-new-item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_text_in_list('1: Buy peacock feathers')
        
        # user sees unique url for her list
        user_1_list_url = self.browser.current_url
        self.assertRegex(user_1_list_url, '/lists/.+')
        
        # another user starts a new list
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        # user 1's list is not there
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
        
        # the user adds an item
        inputbox = self.browser.find_element_by_id('list-new-item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_text_in_list('1: Buy milk')
        
        # user 2 gets a unique url
        user_2_list_url = self.browser.current_url
        self.assertRegex(user_2_list_url, '/lists/.+')
        self.assertNotEqual(user_1_list_url, user_2_list_url)
        
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)