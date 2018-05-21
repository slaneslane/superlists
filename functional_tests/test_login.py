from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_MAIL = 'slane@wp.pl'
SUBJECT = 'Twój link to zalogowania się w serwisie Twoje Listy'


class LoginTest(FunctionalTest):

    def test_can_get_email_to_log_in(self):
        # Magda udaje się na stronę TwojeListy i zauważa,
        # że pojawiła się nowa opcja 'Zaloguj' w pasie nawigacji.
        # Magda zostaje poinformowana, że musi podać swój adres email co też robi.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_MAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # Pojawia się wiadomość o wysłaniu emaila na jej skrzynkę pocztową.
        self.wait_for(lambda: self.assertIn(
                'Sprawdź swoją skrzynkę pocztową',
                self.browser.find_element_by_tag_name('body').text
            )
        )

        # Magda sprawdza swoją skrzynkę pocztową i znajduje w niej wiadomość..
        email = mail.outbox[0]
        self.assertIn(TEST_MAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # Wiadomość zawiera link:
        self.assertIn('Kliknij w poniższy link aby się zalogować w serwisie Twoje Listy:', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Nie znaleziono adresu url w wiadomości:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Magda klika w link:
        self.browser.get(url)

        # Magda jest teraz zalogowana w serwisie Twoje Listy!
        self.wait_for(
                lambda: self.browser.find_element_by_link_text('Wyloguj')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_MAIL, navbar.text)

        # Teraz się wylogowuje:
        self.browser.find_element_by_link_text('Wyloguj').click()

        # Magda jest wylogowana.
        self.wait_for(
            lambda: self.browser.find_element_by_name('email')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(TEST_MAIL, navbar.text)
