import re

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import auth, messages

from accounts.models import Token

MESSAGE_STRING = 'Kliknij w poniższy link aby się zalogować w serwisie Twoje Listy:'
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
        messages.success(self.request, self.MSG_SUCCESS)

    def __message_warning(self):
        messages.warning(self.request, self.MSG_WARNING)

    def __display_message(self):
        if self.status:
            self.__message_success()
        else:
            self.__message_warning()


def validate_email(email):
    EMAIL_REGEXP = re.compile(r'^([\w.-]+)@([\w.-]+)$')
    return EMAIL_REGEXP.match(email)

def build_tokenized_uri(uid):
    return reverse('login') + '?token=' + str(uid)

def build_tokenized_url(request, uid):
    return request.build_absolute_uri(build_tokenized_uri(uid))
    
def create_message_body(url):
    return MESSAGE_STRING + '\n\n' + url

def send_link_in_message(request, uid, email):
    message_body = create_message_body(build_tokenized_url(request, uid))
    return send_mail(EMAIL_TITLE, message_body, NOREPLY_EMAIL, [email])

def send_login_email(request):
    send_status = False
    email = request.POST['email']
    if validate_email(email):
        token = Token.objects.create(email=email)
        try:
            send_status = send_link_in_message(request, token.uid, email)
        except:
            pass
    UserMessage(request, send_status)
    return redirect('/')

def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
