from .base import FunctionalTest

class MyListsTest(FunctionalTest):
    TEST_EMAIL = 'magda@naprzyklad.pl'

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
            self.browser.find_elements_by_link_text('Moje Listy'),
            []
        ))
