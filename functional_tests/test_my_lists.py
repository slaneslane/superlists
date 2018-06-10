import os
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

User = get_user_model()

class MyListsTest(FunctionalTest):
    TEST_EMAIL = 'magda@naprzyklad.pl'

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, os.environ.get('MY_SERVER_PORT'), email)
        else:
            session_key = create_pre_authenticated_session(email)
        ## aby ustawić cookie trzeba najpierw odwiedzić stronę.
        ## 404 !
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Magda jest zalogowanym użytkownikiem:
        self.create_pre_authenticated_session(self.TEST_EMAIL)

        # Udaje się na stronę główną i tworzy nową listę:
        self.browser.get(self.live_server_url)
        self.add_list_item('Przygotować siatkę')
        self.add_list_item('Kupić przynętę')
        first_list_url = self.browser.current_url

        # Po raz pierwszy zauważyła łącze 'Moje Listy':
        self.browser.find_element_by_link_text('Moje Listy').click()

        # Zauważyła, że znajduje się tam jej lista.
        # Nazwa listy pochodzi od pierwszego elementu na niej:
        self.wait_for(lambda: self.browser.find_element_by_link_text('Przygotować siatkę'))
        self.browser.find_element_by_link_text('Przygotować siatkę').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        # Postanowiła utworzyć kolejną listę:
        self.browser.get(self.live_server_url)
        self.add_list_item('Przygotowania do wyprawy')
        second_list_url = self.browser.current_url

        # Strona 'Moje Listy' zawiera teraz tę nową listę:
        self.browser.find_element_by_link_text('Moje Listy').click()
        self.wait_for(lambda: self.browser.find_element_by_link_text('Przygotowania do wyprawy'))
        self.browser.find_element_by_link_text('Przygotowania do wyprawy').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

        # Wylogowała się. Opcja 'Moje Listy' zniknęła:
        self.browser.find_element_by_link_text('Wyloguj').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_link_text('Moje Listy'),
            []
        ))
