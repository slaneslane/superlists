from selenium import webdriver
from .base import FunctionalTest

def quit_if_possible(browser):
    try: browser.quit()
    except: pass

class SharingTest(FunctionalTest):
    def test_can_share_a_list_with_another_user(self):
        # Magda jest zalogowanym użytkownikiem:
        self.create_pre_authenticated_session('magda@naprzyklad.pl')
        magda_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(magda_browser))

        # Szymon również korzysta z tej samej aplikacji:
        szymon_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(szymon_browser))
        self.browser = szymon_browser
        self.create_pre_authenticated_session('szymon@naprzyklad.pl')

        # Magda udaje się na stronę główną aplikacji i tworzy nową listę:
        self.browser = magda_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('Uzyskaj pomoc')

        # Zauważyła opcję "Udostępnij tą listę":
        share_box = self.browser.find_element_by_css_selector(
            'input[name="sharee"]'
        )
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'twoj-przyjaciel@naprzyklad.pl'
        )
