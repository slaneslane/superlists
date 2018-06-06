import re

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import auth, messages

from accounts.models import Token

NOREPLY_EMAIL = 'noreply@twojelisty'
EMAIL_TITLE = 'Twój link do zalogowania się w serwisie Twoje Listy'

class ProcessMessage(object):

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


class URL(object):
    def __init__(self, request, token):
        self.request = request
        self.token = token
        return self.__compose_url()

    def __compose_tokenized_uri(self):
        return reverse('login') + '?token=' + str(self.token.uid)

    def __compose_url(self):
        return self.request.build_absolute_uri(self.__compose_tokenized_uri())


def validate_email(email):
    EMAIL_REGEXP = re.compile(r'/^([a-z0-9_\.-+]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/')
    return EMAIL_REGEXP.match(email)

def compose_message_body(request, token):
    url = URL(request=request, token=token)
    return f'Kliknij w poniższy link aby się zalogować w serwisie Twoje Listy:\n\n{url}'


def send_login_email(request):
    send_status = false

    email = request.POST['email']
    if validate_email(email=email):
        token = Token.objects.create(email=email)
        message_body = compose_message_body(request=request, token=token)

        send_status = send_mail(
            EMAIL_TITLE,
            message_body,
            NOREPLY_EMAIL,
            [email]
        )

    ProcessMessage(request=request, status=send_status)
    return redirect('/')

def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
