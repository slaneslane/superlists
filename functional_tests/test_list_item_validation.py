from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

  def test_cannot_add_empty_list_items(self):
    # Magda przeszla na strone glowna i przypadkowo sprobowala utworzyc
    # pusty element na liscie. Nacisnala klawisz ENTER w pustym polu tekstowym.
    self.browser.get(self.live_server_url)
    self.get_item_input_box().send_keys(Keys.ENTER)

    # Po odswiezeniu strony glownej zobaczyla komunikat bledu
    # informujacy o niemozliwosci utworzenia pustego elementu na liscie.
    self.wait_for(lambda: self.assertEqual(
        self.browser.find_element_by_css_selector('.has-error').text,
        "Element nie może być pusty!"
    ))

    # Sprobowala ponownie wpisujac dowolny tekst i tym razem wszystko zadzialalo.
    self.get_item_input_box().send_keys('Kupic mleko')
    self.get_item_input_box().send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table_and_check_it('1: Kupic mleko')

    # Przekornie po raz drugi sprobowala utworzyc pusty element na liscie.
    self.get_item_input_box().send_keys(Keys.ENTER)

    # Na stronie listy otrzymala ostrzezenie podobne do wczesniejszego.
    self.wait_for(lambda: self.assertEqual(
        self.browser.find_element_by_css_selector('.has-error').text,
        "Element nie może byc pusty!"
    ))

    # Element mogla poprawic wpisujac w nim dowolny tekst.
    self.get_item_input_box().send_keys('Zrobic herbate')
    self.get_item_input_box().send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table_and_check_it('1: Kupic mleko')
    self.wait_for_row_in_list_table_and_check_it('2: Zrobic herbate')
