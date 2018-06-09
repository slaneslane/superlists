from django.test import TestCase
from unittest.mock import patch, call

import accounts.views
from accounts.models import Token
from accounts.lib.utils import send_mail, EMAIL_TITLE, NOREPLY_EMAIL, UserMessage
    
class SendLoginEmailViewTest(TestCase):
    TEST_EMAIL = 'magda@naprzyklad.pl'
    
    def test_send_login_email_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email',
            data={'email': self.TEST_EMAIL}
        )
        self.assertRedirects(response, '/')

#    def test_sends_mail_to_address_from_post(self):
#        self.send_mail_called = False
#
#        def fake_send_mail(subject, body, from_email, to_list):
#            self.send_mail_called = True
#            self.subject = subject
#            self.body = body
#            self.from_email = from_email
#            self.to_list = to_list
#
#        accounts.views.send_mail = fake_send_mail
#
#        self.client.post('/accounts/send_login_email', data={
#            'email': 'magda@naprzyklad.pl' 
#        })
#
#        self.assertTrue(self.send_mail_called)
#        self.assertEqual(self.subject, 'Twój link to zalogowania się w serwisie Twoje Listy')
#        self.assertEqual(self.from_email, 'noreply@twojelisty')
#        self.assertEqual(self.to_list, ['magda@naprzyklad.pl'])
    
    # inaczej to samo co powyżej - używając monkeypatching:
    @patch('accounts.lib.utils.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post('/accounts/send_login_email',
            data={'email': self.TEST_EMAIL}
        )
        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, EMAIL_TITLE)
        self.assertEqual(from_email, NOREPLY_EMAIL)
        self.assertEqual(to_list, [self.TEST_EMAIL])

    def test_adds_success_message(self):
        response = self.client.post('/accounts/send_login_email',
            data={'email': self.TEST_EMAIL},
            follow=True
        )
        message = list(response.context['messages'])[0]
        self.assertEqual(message.message, UserMessage.MSG_SUCCESS)
        self.assertEqual(message.tags, "success")

#    # inaczej to samo co powyżej - używając monkeypatching:
#    @patch('accounts.views.messages')
#    def test_adds_success_message_with_mocks(self, mock_messages):
#        response = self.client.post('/accounts/send_login_email', data={
#            'email': 'magda@naprzyklad.pl'
#        })
#
#        expected = 'Sprawdź swoją skrzynkę pocztową. Wysłaliśmy Ci wiadomość z linkiem, który pozwoli Ci się zalogować.'
#        self.assertEqual(
#            mock_messages.success.call_args,
#            call(response.wsgi_request, expected),
#        )

    def test_creates_token_associated_with_email(self):
        self.client.post('/accounts/send_login_email',
            data={'email': self.TEST_EMAIL}
        )
        token = Token.objects.first()
        self.assertEqual(token.email, self.TEST_EMAIL)

    @patch('accounts.lib.utils.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post('/accounts/send_login_email',
            data={'email': self.TEST_EMAIL}
        )
        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):

    def test_login_redirects_to_home_page(self, mock_auth):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abcd123')
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )
        # można i tak lecz w przypadku literówki test będzie zawsze zaliczany!!! 
        #mock_auth.login.assert_called_with(response.wsgi_request, mock_auth.authenticate.return_value)

    def test_does_not_login_with_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.login.called, False)
