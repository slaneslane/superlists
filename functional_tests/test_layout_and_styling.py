from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):

  def test_layout_and_styling(self):
    # Magda odwiedza stronę główną aplikacji.
    self.browser.get(self.live_server_url)

    # Zauważa, że inputbox znajduje się na środku strony.
    self.element_centered('id_text', 45)

    # Magda tworzy nową listę.
    self.get_item_input_box().send_keys('testowy')
    self.get_item_input_box().send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: testowy')

    # Zauważa, że inputbox jest wciąż na środku strony.
    self.element_centered('id_text', 45)

  def test_list_filtering(self):
    # Magda odwiedza strone główną aplikacji i wpisuje swoje plany na listę.
    self.browser.get(self.live_server_url)

    self.get_item_input_box().send_keys('Kupic pawie piora')
    self.get_item_input_box().send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: Kupic pawie piora')

    self.get_item_input_box().send_keys('Uzyc pawich pior do zrobienia przynety')
    self.get_item_input_box().send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('2: Uzyc pawich pior do zrobienia przynety')

    # Po czym filtruje listę zakupów:
    self.get_item_input_box().send_keys('Kupic')

    # Na liście zostaje jedynie 'Kupić pawie pióra'.
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertIn('Kupic pawie piora', page_text)
    self.assertNotIn('Uzyc pawich pior do zrobienia przynety', page_text)
