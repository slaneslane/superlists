from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os
import time

MAX_WAIT = 10


# decorator function to wait:
def wait(func):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return func(*args, **kwargs)
            except (AssertionError, WebDriverException) as a:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        # Rozpoczynamy nowa sesje przegladarki.
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        # Na koniec wylaczamy sesje przegladarki aby miec pewnosc, ze zadne
        # informacje dotyczace poprzedniego uzytkownika nie zostana ujawnione, na przyklad przez cookies.
        self.browser.quit()
    
    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('Wyloguj')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
    
    def element_centered(self, element_tag, delta_=10):
        element = self.browser.find_element_by_id(element_tag)
        browser_size = self.browser.get_window_size()
        self.assertAlmostEqual(
            element.location['x'] + (element.size['width'] / 2), (browser_size['width'] / 2), delta=delta_
        )

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')
