from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):

  def test_layout_and_styling(self):

    # Magda odwiedza strone glowna aplikacji.
    self.browser.get(self.live_server_url)

    # Zauwaza, ze inputbox znajduje sie na srodku strony.
    self.element_centered('id_new_item', 45)

    # Magda tworzy nowa liste
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('testowy')
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table_and_check_it('1: testowy')

    # Zauwaza, ze inputbox jest wciaz na srodku strony.
    self.element_centered('id_new_item', 45)
