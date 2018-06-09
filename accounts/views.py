from django.shortcuts import redirect
from django.contrib import auth

from accounts.models import Token
from accounts.lib.utils import validate_email, send_link_in_message, UserMessage

def send_login_email(request):
    send_status = False
    email = request.POST['email'].lower()
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
