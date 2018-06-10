import os
import poplib
import re
import time

from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

SUBJECT = 'Twój link do zalogowania się w serwisie Twoje Listy'
LINK = 'Kliknij w poniższy link aby się zalogować w serwisie Twoje Listy:'


class LoginTest(FunctionalTest):

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.gmail.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['TEST_MAIL_PASSWORD'])
            while time.time() - start < 60:
                # pobierz 10 najnowszych wiadomości:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('pobieranie wiadomości', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if LINK in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_to_log_in(self):
        # Magda udaje się na stronę TwojeListy i zauważa,
        # że pojawiła się nowa opcja 'Zaloguj' w pasie nawigacji.
        # Magda zostaje poinformowana, że musi podać swój adres email co też robi.
        if self.staging_server:
            test_email = 'recent:' + 'twojelisty.test@gmail.com'
        else:
            test_email = 'magda@naprzyklad.pl'

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # Pojawia się wiadomość o wysłaniu emaila na jej skrzynkę pocztową.
        self.wait_for(lambda: self.assertIn(
           'Sprawdź swoją skrzynkę pocztową',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Magda sprawdza swoją skrzynkę pocztową i znajduje w niej wiadomość..
        body = self.wait_for_email(test_email, SUBJECT)

        # Wiadomość zawiera link:
        self.assertIn(LINK, body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Nie znaleziono adresu url w wiadomości:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Magda klika w link:
        self.browser.get(url)

        # Magda jest teraz zalogowana w serwisie Twoje Listy!
        self.wait_to_be_logged_in(email=test_email) 

        # Teraz się wylogowuje:
        self.browser.find_element_by_link_text('Wyloguj').click()

        # Magda jest wylogowana.
        self.wait_to_be_logged_out(email=test_email)
