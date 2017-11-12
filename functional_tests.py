from selenium import webdriver
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
    self.fail('Zakończenie testu!')

    # Od razu zostaje zachęcona, aby wpisać rzecz do zrobienia.

    # W polu tekstowym wpisała "Kupić pawie pióra"
    # (hobby Magdy polegające na tworzeniu ozdobnych przynęt).

    # Po wciśnięciu klawisza Enter strona została uaktualniona i wyświetla
    # "1: Kupić pawie pióra" jako element listy rzeczy do zrobienia.

    # Na stronie nadal znajduje się pole tekstowe zachęcające do podania kolejnego zadania.
    # Magda wpisała "Użycie pawich piór do zrobienia przynęty" (Magda jest niezwykle skrupulatna).

    # Strona została ponownie uaktualniona i teraz wyświetla dwa elementy na liście rzeczy do zrobienia.

    # Magda była ciekawa, czy witryna zapamięta jej listę. Zwróćiła uwagę na wygenerowany dla niej
    # unikatowy adres URL, obok którego znajduje się tekst z wyjaśnieniem.

    # Przechodzi pod podany adres URL i widzi wyświetloną swoją listę rzeczy do zrobienia.

if __name__ == '__main__':
  unittest.main(warnings='ignore') 



