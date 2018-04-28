from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys



class ItemValidationTest(FunctionalTest):

  def test_cannot_add_empty_list_items(self):
    # Magda przeszla na strone glowna i przypadkowo sprobowala utworzyc
    # pusty element na liscie. Nacisnala klawisz ENTER w pustym polu tekstowym.

    # Po odswiezeniu strony glownej zobaczyla komunikat bledu
    # informujacy o niemozliwosci utworzenia pustego elementu na liscie.

    # Sprobowala ponownie wpisujac dowolny tekst i tym razem wszystko zadzialalo.

    # Przekornie po raz drugi sprobowala utworzyc pusty element na liscie.

    # Na stronie listy otrzymala ostrzezenie podobne do wczesniejszego.

    # Element mogla poprawic wpisujac w nim dowolny tekst.
    self.fail('Kontynuuj!')
