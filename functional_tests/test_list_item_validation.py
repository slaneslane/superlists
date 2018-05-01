from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from lists.forms import DUPLICATE_ITEM_ERROR

class ItemValidationTest(FunctionalTest):

  def get_error_element(self):
    return self.browser.find_element_by_css_selector('.has-error')

  def test_cannot_add_empty_list_items(self):
    # Magda przeszla na strone glowna i przypadkowo sprobowala utworzyc
    # pusty element na liscie. Nacisnala klawisz ENTER w pustym polu tekstowym.
    self.browser.get(self.live_server_url)
    self.get_item_input_box().send_keys(Keys.ENTER)

    # Przegladarka wykrywa pusty inputbox i informuje o tym uzytkownika:
    self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

    # Kiedy zaczyna wpisywać tekst błąd znika:
    self.get_item_input_box().send_keys('Kupic mleko')
    self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))

    # Z powodzeniem wysyla teraz wprowadzony tekst:
    self.get_item_input_box().send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table_and_check_it('1: Kupic mleko')

    # Przekornie po raz drugi sprobowala utworzyc pusty element na liscie.
    self.get_item_input_box().send_keys(Keys.ENTER)

    # Przegladarka znowu wskazuje na blad:
    self.wait_for_row_in_list_table_and_check_it('1: Kupic mleko')
    self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

    # Element mogla poprawic wpisujac w nim dowolny tekst.
    self.get_item_input_box().send_keys('Zrobic herbate')
    self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
    self.get_item_input_box().send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table_and_check_it('1: Kupic mleko')
    self.wait_for_row_in_list_table_and_check_it('2: Zrobic herbate')

  def test_cannot_add_duplicate_items(self):
    # Magda przeszla na strone glowna i zaczela tworzyc nowa liste
    self.browser.get(self.live_server_url)
    self.get_item_input_box().send_keys('Kupic kalosze')
    self.get_item_input_box().send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table_and_check_it('1: Kupic kalosze')

    # Przypadkowo sprobowala wpisac element, ktory juz znajdowal sie na liscie
    self.get_item_input_box().send_keys('Kupic kalosze')
    self.get_item_input_box().send_keys(Keys.ENTER)
      
    # Otrzymala czytelny komunikat bledu:
    self.wait_for(lambda: self.assertEqual(self.get_error_element().text, DUPLICATE_ITEM_ERROR))

  def test_error_messages_are_cleared_on_input(self):
    # Magda utworzyla nowa liste w sposob, ktory spowodowal powstanie bledu weryfikacji:
    self.browser.get(self.live_server_url)
    self.get_item_input_box().send_keys('Glupie zart')
    self.get_item_input_box().send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table_and_check_it('1: Glupie zart')

    # Powtórnie wpisała to samo hasło:
    self.get_item_input_box().send_keys('Glupie zart')
    self.get_item_input_box().send_keys(Keys.ENTER)
    self.wait_for(lambda: self.assertTrue(self.get_error_element().is_displayed()))

    # Rozpoczela wpisywanie danych w elemencie <input> aby usunac blad:
    self.get_item_input_box().send_keys('y')
    print(self.get_item_input_box().get_attribute('value'))
    self.browser.implicitly_wait(5)

    # Byla zadowolona widzac, ze komunikat bledu zniknal:
    self.wait_for(lambda: self.assertFalse(self.get_error_element().is_displayed()))
