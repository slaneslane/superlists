from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):

  def test_layout_and_styling(self):

    # Magda odwiedza strone glowna aplikacji.
    self.browser.get(self.live_server_url)

    # Zauwaza, ze inputbox znajduje sie na srodku strony.
    self.element_centered('id_text', 45)

    # Magda tworzy nowa liste
    self.get_item_input_box().send_keys('testowy')
    self.get_item_input_box().send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: testowy')

    # Zauwaza, ze inputbox jest wciaz na srodku strony.
    self.element_centered('id_text', 45)
