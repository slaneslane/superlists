Przygotowanie Serwera dla Nowej Strony:
=======================================

## Wymagane pakiety:

* nginx
* Python 3.6
* venv i pip
* Git

przykład dla Ubuntu:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install nginx git python36 python3.6-venv

## Konfiguracja wirtualnych hostów w Nginx:

* patrz: nginx.template.conf
* podmień DOMAIN na nazwę strony, np: superlisty.pl

## Serwis Systemd:

* patrz: gunicorn-systemd.template.service
* podmień DOMAIN na nazwę strony, np: superlisty.pl

## Struktura katalogów projektu:

Przypuśćmy, że mamy użytkownika 'username' i jego katalog domowy:

/home/username
 |----- DOMAIN1
 |   |- .env
 |   |- db.sqlite3
 |   |- manage.py 
 |   |- etc
 |   |- static
 |   |- virtualenv
 |----- DOMAIN2
     |- .env
     |- db.sqlite3
     |- etc
