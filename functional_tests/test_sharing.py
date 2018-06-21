from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_list_page import MyListsPage

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
        list_page = ListPage(self).add_list_item('Kupić sprzęty AGD')

        # Zauważyła opcję "Udostępnij tą listę":
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'twoj-przyjaciel@naprzyklad.pl'
        )

        # Udostępnia swoją listę:
        # Strona uaktualnia się podając informację, że lista jest współdzielona z Szymonem:
        list_page.share_list_with('szymon@naprzyklad.pl')

        # Szymon odwiedza stronę aplikacji:
        self.browser = szymon_browser
        MyListsPage(self).go_to_my_lists_page()

        # Zauważa listę tam Magdy!
        self.browser.find_element_by_link_text('Kupić sprzęty AGD').click()

        # Na stronie współdzielonej listy Szymon widzi, że lista należy do Magdy:
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'magda@naprzyklad.pl'
        ))

        # Dodaje nowy element do listy:
        list_page.add_list_item('Dokupić meble do kuchni')
        
        # Kiedy Magda odświeża stronę w swojej przeglądarce widzi element dodany przez Szymona:
        self.browser = magda_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Dokupić meble do kuchni', 2)
