from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import auth, messages

from accounts.models import Token

def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Kliknij w poniższy link aby się zalogować w serwisie Twoje Listy:\n\n{url}'
    send_mail(
        'Twój link do zalogowania się w serwisie Twoje Listy',
        message_body,
        'noreply@twojelisty',
        [email]
    )
    messages.success(
        request,
        'Sprawdź swoją skrzynkę pocztową. Wysłaliśmy Ci wiadomość z linkiem, który pozwoli Ci się zalogować.'
    )
#    # inaczej (niestety nie współgra z mockiem):
#    messages.add_message(
#        request,
#        messages.SUCCESS,
#        'Sprawdź swoją skrzynkę pocztową. Wysłaliśmy Ci wiadomość z linkiem, który pozwoli Ci się zalogować.'
#    )
    return redirect('/')

def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
