import re

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import auth, messages

from accounts.models import Token

NOREPLY_EMAIL = 'noreply@twojelisty'
EMAIL_TITLE = 'Twój link do zalogowania się w serwisie Twoje Listy'

class UserMessage(object):

    MSG_SUCCESS = 'Sprawdź swoją skrzynkę pocztową. Wysłaliśmy Ci wiadomość z linkiem, który pozwoli Ci się zalogować.'
    MSG_WARNING = 'Niestety coś poszło nie tak. Wprowadź swój poprawny adres e-mail.'

    def __init__(self, request, status):
        self.request = request
        self.status = status
        self.__display_message()

    def __message_success(self):
        messages.success(self.request, MSG_SUCCESS)

    def __message_warning(self):
        messages.warning(self.request, MSG_WARNING)

    def __display_message(self):
        if self.status:
            self.__message_success()
        else:
            self.__message_warning()


class TokenizedURL(object):

    def __init__(self, base_uri, uid):
        self.base_uri = base_uri
        self.uid = uid
        self.__tokenized_uri = self.__compose_tokenized_uri()
        self.__tokenized_url = self.__compose_tokenized_url()

    def __compose_tokenized_uri(self):
        return reverse('login') + '?token=' + str(self.uid)

    def __compose_tokenized_url(self):
        return self.base_uri + self.__tokenized_uri

    def get_tokenized_URL(self):
        return self.__tokenized_url

def validate_email(email):
    EMAIL_REGEXP = re.compile(r'^([\w.-]+)@([\w.-]+)$')
    return EMAIL_REGEXP.match(email)


def send_login_email(request):
    send_status = false

    email = request.POST['email']
    if validate_email(email):
        try:
            token = Token.objects.create(email=email)

            url = TokenizedURL(base_uri=request.build_absolute_uri(), uid=token.uid)
            message_body = f'Kliknij w poniższy link aby się zalogować w serwisie Twoje Listy:\n\n{url.get_tokenized_URL()}'

            send_status = send_mail(
                EMAIL_TITLE,
                message_body,
                NOREPLY_EMAIL,
                [email]
            )
        except:
            pass

    UserMessage(request, send_status)
    return redirect('/')

def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
