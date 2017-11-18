from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

  def setUp(self):
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    # Usatysfakcjonowana kładzie się spać.
    self.browser.quit()

  def test_can_start_a_list_and_retrive_it_later(self):
    # Magda dowiedziała się o nowej, wspaniałej aplikacji w postaci listy rzeczy do zrobienia.
    # Postanowiła więc przejść na stronę główną tej aplikacji.
    self.browser.get('http://localhost:8000')

    # Zwróciła uwagę, że tytuł strony i nagłówek zawierają słowo Listy.
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
    
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn('1: Kupić pawie pióra', [row.text for row in rows])

    # Na stronie nadal znajduje się pole tekstowe zachęcające do podania kolejnego zadania.
    # Magda wpisała "Użyć pawich piór do zrobienia przynęty" (Magda jest niezwykle skrupulatna).
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Użyć pawich piór do zrobienia przynęty')
    inputbox.send_keys(Keys.ENTER)

    # Strona została ponownie uaktualniona i teraz wyświetla dwa elementy na liście rzeczy do zrobienia.
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn('1: Kupić pawie pióra', [row.text for row in rows])
    self.assertIn('2: Użyć pawich piór do zrobienia przynęty', [row.text for row in rows])

    # Magda była ciekawa, czy witryna zapamięta jej listę. Zwróćiła uwagę na wygenerowany dla niej
    # unikatowy adres URL, obok którego znajduje się tekst z wyjaśnieniem.
    self.fail('Zakończenie testu!')

    # Przechodzi pod podany adres URL i widzi wyświetloną swoją listę rzeczy do zrobienia.

if __name__ == '__main__':
  unittest.main(warnings='ignore') 



