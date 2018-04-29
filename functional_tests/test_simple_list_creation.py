from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

  def test_can_start_a_list_for_one_user(self):

    # Magda dowiedziala sie o nowej, wspanialej aplikacji w postaci listy rzecz do zrobienia.
    # Przechodzi wiec na strone glowna tej aplikacji.
    self.browser.get(self.live_server_url)

    # Magda zwrocila uwage, ze tytul strony i naglowek zawieraja slowo 'Listy' i 'rzeczy do zrobienia'.
    self.assertIn('Listy', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('Utwórz nową listę rzeczy do zrobienia', header_text)

    # Od razu zostaje zachecona, aby wpisac rzecz do zrobienia.
    inputbox = self.get_item_input_box()
    self.assertEqual(
        inputbox.get_attribute('placeholder'),
        'Wpisz rzecz do zrobienia'
    )

    # W polu tekstowym wpisala "Kupic pawie piora"
    # (hobby Magdy polegajace na tworzeniu ozdobnych przynet).
    inputbox.send_keys('Kupic pawie piora')

    # Po wcisnieciu klawisza Enter strona zostala uaktualniona i wyswietla
    # "1: Kupic pawie piora" jako element listy rzecz do zrobienia.
    inputbox.send_keys(Keys.ENTER)

    # Wpisane przez Magde haslo pojawia sie na jej liscie.
    self.wait_for_row_in_list_table_and_check_it('1: Kupic pawie piora')

    # Lista Magdy ma swoj wlasny URL.
    magda_list_url = self.browser.current_url
    self.assertRegex(magda_list_url, '/lists/.+')

    # Na stronie nadal znajduje sie pole tekstowe zachecajace do podania kolejnego zadania.
    # Magda wpisala "Uzyc pawich pior do zrobienia przynety" (Magda jest niezwykle skrupulatna).
    inputbox = self.get_item_input_box()
    inputbox.send_keys('Uzyc pawich pior do zrobienia przynety')
    inputbox.send_keys(Keys.ENTER)

    # Strona zostala ponownie uaktualniona i teraz wyswietla dwa elementy na liscie rzecz do zrobienia.
    self.wait_for_row_in_list_table_and_check_it('1: Kupic pawie piora')
    self.wait_for_row_in_list_table_and_check_it('2: Uzyc pawich pior do zrobienia przynety')


  def test_multiple_users_can_start_lists_at_different_urls(self):

    # Magda odpala strone aplikacji i wpisuje haslo generujac nowa liste.
    self.browser.get(self.live_server_url)
    inputbox = self.get_item_input_box()
    inputbox.send_keys('Kupic pawie piora')
    inputbox.send_keys(Keys.ENTER)

    # Wpisane przez Magde haslo pojawia sie na jej liscie.
    self.wait_for_row_in_list_table_and_check_it('1: Kupic pawie piora')

    # Zauwaza, ze jej lista ma unikalny adres URL.
    magda_list_url = self.browser.current_url
    self.assertRegex(magda_list_url, '/lists/.+')

    # Magda wylacza swoja przegladarke.
    self.browser.quit()

    # Teraz nowy uzytkownik Szymon zaczyna korzystac z witryny.
    self.browser = webdriver.Firefox()

    # Szymon odwiedza strone glowna.
    # Nie znajduje zadnych sladow listy Magdy.
    self.browser.get(self.live_server_url)
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Kupic pawie piora', page_text)
    self.assertNotIn('Uzyc pawich pior do zrobienia przynety', page_text)

    # Szymon tworzy wlasna liste, wprowadzajac nowy element.
    # Jego lista jest mniej interesujaca niz lista Magdy...
    inputbox = self.get_item_input_box()
    inputbox.send_keys('Kupic mleko')
    inputbox.send_keys(Keys.ENTER)

    # Wpisane przez Szymona haslo pojawia sie na jego liscie.
    self.wait_for_row_in_list_table_and_check_it('1: Kupic mleko')

    # Szymon otrzymuje unikatowy adres URL prowadzacy do listy.
    szymon_list_url = self.browser.current_url
    self.assertRegex(szymon_list_url, '/lists/.+')

    # Adresy URL list Magdy i Szymona roznia sie od siebie.
    self.assertNotEqual(szymon_list_url, magda_list_url)

    # Ponownie nie ma zadnego sladu po Magdzie.
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Kupic pawie piora', page_text)
    self.assertIn('Kupic mleko', page_text)

   
