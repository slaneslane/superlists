from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#for fixing the selenium 3 problem with reloading waiting page at the end of 5th chapter:
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of

import unittest

class NewVisitorTest(LiveServerTestCase):

  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    # Usatysfakcjonowana kładzie się spać.
    self.browser.quit()

  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')

    self.assertIn(row_text, [row.text for row in rows])

  @contextmanager
  def wait_for_page_load(self, timeout=30):
    old_page = self.browser.find_element_by_tag_name("html")
    yield WebDriverWait(self, timeout).until(
         staleness_of(old_page)
    )

  def test_can_start_a_list_and_retrive_it_later(self):
    # Magda dowiedziała się o nowej, wspaniałej aplikacji w postaci listy rzeczy do zrobienia.
    # Postanowiła więc przejść na stronę główną tej aplikacji.
    self.browser.get(self.live_server_url)

    # Zwróciła uwagę, że tytuł strony i nagłówek zawierają słowo 'Listy' i 'lista'.
    self.assertIn('Listy', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('lista', header_text)

    # Od razu zostaje zachęcona, aby wpisać rzecz do zrobienia.
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(inputbox.get_attribute('placeholder'), 'Wpisz rzeczy do zrobienia')

    # W polu tekstowym wpisała "Kupić pawie pióra"
    # (hobby Magdy polegające na tworzeniu ozdobnych przynęt).
    inputbox.send_keys('Kupić pawie pióra')

    # Po wciśnięciu klawisza Enter strona została uaktualniona i wyświetla
    # "1: Kupić pawie pióra" jako element listy rzeczy do zrobienia.
    inputbox.send_keys(Keys.ENTER)

    with self.wait_for_page_load(timeout=10):
        self.check_for_row_in_list_table('1: Kupić pawie pióra')

    # Na stronie nadal znajduje się pole tekstowe zachęcające do podania kolejnego zadania.
    # Magda wpisała "Użyć pawich piór do zrobienia przynęty" (Magda jest niezwykle skrupulatna).
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Użyć pawich piór do zrobienia przynęty')
    inputbox.send_keys(Keys.ENTER)

    # Strona została ponownie uaktualniona i teraz wyświetla dwa elementy na liście rzeczy do zrobienia.
    with self.wait_for_page_load(timeout=10):
        self.check_for_row_in_list_table('1: Kupić pawie pióra')
        self.check_for_row_in_list_table('2: Użyć pawich piór do zrobienia przynęty')

    # Magda była ciekawa, czy witryna zapamięta jej listę. Zwróciła uwagę na wygenerowany dla niej
    # unikatowy adres URL, obok którego znajduje się tekst z wyjaśnieniem.
    self.fail('Zakończenie testu!')

    # Przechodzi pod podany adres URL i widzi wyświetloną swoją listę rzeczy do zrobienia.
