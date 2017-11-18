from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
 
from lists.views import home_page

class HomePageTest(TestCase):
 
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'Nowy element listy'})
        self.assertIn('Nowy element listy', response.content.decode())
