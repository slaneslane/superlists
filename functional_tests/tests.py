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
    # Rozpoczynamy nową sesję przeglądarki.
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    # Na koniec wyłączamy sesję przeglądarki aby mieć pewność, że żadne
    # informacje dotyczące poprzedniego użytkownika nie zostaną ujawnione, na przykład przez cookies.
    self.browser.quit()

  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text, [row.text for row in rows])

  @contextmanager
  def wait_for_page_load(self, timeout=5):
    old_page = self.browser.find_element_by_tag_name("html")
    yield WebDriverWait(self, timeout).until(
         staleness_of(old_page)
    )


  def test_can_start_a_list_for_one_user(self):

    # Magda dowiedziała się o nowej, wspaniałej aplikacji w postaci listy rzeczy do zrobienia.
    # Przechodzi więc na stronę główną tej aplikacji.
    self.browser.get(self.live_server_url)

    # Magda zwróciła uwagę, że tytuł strony i nagłówek zawierają słowo 'Listy' i 'rzeczy do zrobienia'.
    self.assertIn('Listy', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('rzeczy do zrobienia', header_text)

    # Od razu zostaje zachęcona, aby wpisać rzecz do zrobienia.
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(
        inputbox.get_attribute('placeholder'),
        'Wpisz rzeczy do zrobienia'
    )

    # W polu tekstowym wpisała "Kupić pawie pióra"
    # (hobby Magdy polegające na tworzeniu ozdobnych przynęt).
    inputbox.send_keys('Kupić pawie pióra')

    # Po wciśnięciu klawisza Enter strona została uaktualniona i wyświetla
    # "1: Kupić pawie pióra" jako element listy rzeczy do zrobienia.
    inputbox.send_keys(Keys.ENTER)

    # Wpisane przez Magdę hasło pojawia się na jej liście.
    with self.wait_for_page_load(timeout=2):
        self.check_for_row_in_list_table('1: Kupić pawie pióra')

    # Lista Magdy ma swój własny URL.
    magda_list_url = self.browser.current_url
    self.assertRegex(magda_list_url, '/lists/.+')

    # Na stronie nadal znajduje się pole tekstowe zachęcające do podania kolejnego zadania.
    # Magda wpisała "Użyć pawich piór do zrobienia przynęty" (Magda jest niezwykle skrupulatna).
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Użyć pawich piór do zrobienia przynęty')
    inputbox.send_keys(Keys.ENTER)

    # Strona została ponownie uaktualniona i teraz wyświetla dwa elementy na liście rzeczy do zrobienia.
    with self.wait_for_page_load(timeout=2):
    	self.check_for_row_in_list_table('1: Kupić pawie pióra')
    	self.check_for_row_in_list_table('2: Użyć pawich piór do zrobienia przynęty')


  def test_multiple_users_can_start_lists_at_different_urls(self):

    # Magda odpala stronę aplikacji i wpisuje hasło generując nową listę.
    self.browser.get(self.live_server_url)
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Kupić pawie pióra')
    inputbox.send_keys(Keys.ENTER)

    # Wpisane przez Magdę hasło pojawia się na jej liście.
    with self.wait_for_page_load(timeout=2):
        self.check_for_row_in_list_table('1: Kupić pawie pióra')

    # Zauważa, że jej lista ma unikalny adres URL.
    magda_list_url = self.browser.current_url
    self.assertRegex(magda_list_url, '/lists/.+')

    # Magda wyłącza swoją przeglądarkę.
    self.browser.quit()

    # Teraz nowy użytkownik Szymon zaczyna korzystać z witryny.
    self.browser = webdriver.Firefox()

    # Szymon odwiedza stronę główną.
    # Nie znajduje żadnych śladów listy Magdy.
    self.browser.get(self.live_server_url)
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Kupić pawie pióra', page_text)
    self.assertNotIn('Użyć pawich piór do zrobienia przynęty', page_text)

    # Szymon tworzy własną listę, wprowadzając nowy element.
    # Jego lista jest mniej interesująca niż lista Magdy...
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Kupić mleko')
    inputbox.send_keys(Keys.ENTER)
    
    # Wpisane przez Szymona hasło pojawia się na jego liście.
    with self.wait_for_page_load(timeout=2):
        self.check_for_row_in_list_table('1: Kupić mleko')

    # Szymon otrzymuje unikatowy adres URL prowadzący do listy.
    szymon_list_url = self.browser.current_url
    self.assertRegex(szymon_list_url, '/lists/.+')

    # Adresy URL list Magdy i Szymona różnią się od siebie.
    self.assertNotEqual(szymon_list_url, magda_list_url)

    # Ponownie nie ma żadnego śladu po Magdzie.
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Kupić pawie pióra', page_text)
    self.assertIn('Kupić mleko', page_text)

    # Usatysfakcjonowani, oboje kładą się spać.
    #self.fail('Koniec testu!')
