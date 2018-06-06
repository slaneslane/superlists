import re

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import auth, messages

from accounts.models import Token

def message_success():
    messages.success(
        request,
        'Sprawdź swoją skrzynkę pocztową. Wysłaliśmy Ci wiadomość z linkiem, który pozwoli Ci się zalogować.'
    )

def message_warning():
    messages.warning(
        request,
        'Niestety coś poszło nie tak. Wprowadź swój poprawny adres e-mail.'
    )

def ok_message(flag):
    if flag:
        message_success()
    else:
        message_warning()
    return flag

def validate_email(email):
    EMAIL_REGEXP = re.compile(r'/^([a-z0-9_\.-+]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/')
    return EMAIL_REGEXP.match(email)

def send_login_email(request):
    email = request.POST['email']
    if not ok_message(validate_email(email)):
        return redirect('/')

    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Kliknij w poniższy link aby się zalogować w serwisie Twoje Listy:\n\n{url}'

    send_status = send_mail(
        'Twój link do zalogowania się w serwisie Twoje Listy',
        message_body,
        'noreply@twojelisty',
        [email]
    )
    ok_message(send_status)
    return redirect('/')

def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
