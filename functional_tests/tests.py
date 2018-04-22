from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):

  def setUp(self):
    # Rozpoczynamy nowa sesje przegladarki.
    self.browser = webdriver.Firefox()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    # Na koniec wylaczamy sesje przegladarki aby miec pewnosc, ze zadne
    # informacje dotyczace poprzedniego uzytkownika nie zostana ujawnione, na przyklad przez cookies.
    self.browser.quit()

  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text, [row.text for row in rows])

  def wait_for_row_in_list_table_and_check_it(self, row_text):
    start_time = time.time()
    while True:
        try:
            self.check_for_row_in_list_table(row_text)
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5 )

  def element_centered(self, element_tag, delta_=10):
    element = self.browser.find_element_by_id(element_tag)
    browser_size = self.browser.get_window_size() 
    self.assertAlmostEqual(
        element.location['x'] + (element.size['width'] / 2), (browser_size['width'] / 2), 2, delta=delta_
    )

  def test_can_start_a_list_for_one_user(self):

    # Magda dowiedziala sie o nowej, wspanialej aplikacji w postaci listy rzeczy do zrobienia.
    # Przechodzi wiec na strone glowna tej aplikacji.
    self.browser.get(self.live_server_url)

    # Magda zwrocila uwage, ze tytul strony i naglowek zawieraja slowo 'Listy' i 'rzeczy do zrobienia'.
    self.assertIn('Listy', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('rzeczy do zrobienia', header_text)

    # Od razu zostaje zachecona, aby wpisac rzecz do zrobienia.
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(
        inputbox.get_attribute('placeholder'),
        'Wpisz rzeczy do zrobienia'
    )

    # W polu tekstowym wpisala "Kupic pawie piora"
    # (hobby Magdy polegajace na tworzeniu ozdobnych przynet).
    inputbox.send_keys('Kupic pawie piora')

    # Po wcisnieciu klawisza Enter strona zostala uaktualniona i wyswietla
    # "1: Kupic pawie piora" jako element listy rzeczy do zrobienia.
    inputbox.send_keys(Keys.ENTER)

    # Wpisane przez Magde haslo pojawia sie na jej liscie.
    self.wait_for_row_in_list_table_and_check_it('1: Kupic pawie piora')

    # Lista Magdy ma swoj wlasny URL.
    magda_list_url = self.browser.current_url
    self.assertRegex(magda_list_url, '/lists/.+')

    # Na stronie nadal znajduje sie pole tekstowe zachecajace do podania kolejnego zadania.
    # Magda wpisala "Uzyc pawich pior do zrobienia przynety" (Magda jest niezwykle skrupulatna).
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Uzyc pawich pior do zrobienia przynety')
    inputbox.send_keys(Keys.ENTER)

    # Strona zostala ponownie uaktualniona i teraz wyswietla dwa elementy na liscie rzeczy do zrobienia.
    self.wait_for_row_in_list_table_and_check_it('1: Kupic pawie piora')
    self.wait_for_row_in_list_table_and_check_it('2: Uzyc pawich pior do zrobienia przynety')


  def test_multiple_users_can_start_lists_at_different_urls(self):

    # Magda odpala strone aplikacji i wpisuje haslo generujac nowa liste.
    self.browser.get(self.live_server_url)
    inputbox = self.browser.find_element_by_id('id_new_item')
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
    inputbox = self.browser.find_element_by_id('id_new_item')
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


  def test_layout_and_styling(self):

    # Magda odwiedza strone glowna aplikacji.
    self.browser.get(self.live_server_url)

    # Zauwaza, ze inputbox znajduje sie na srodku strony.
    self.element_centered('id_new_item')

    # Magda tworzy nowa liste
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('testowy')
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table_and_check_it('1: testowy')

    # Zauwaza, ze inputbox jest wciaz na srodku strony.
    self.element_centered('id_new_item')




# Usatysfakcjonowani, oboje klada sie spac.
#self.fail('Koniec testu!')
