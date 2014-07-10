<<<<<<< HEAD
portal
======

procedimentos para utilização local:
- sudo aptitude install gettext
- cd ~/
- git clone https://github.com/eldioschalm/portal.git
- virtualenv portal
- cd portal
- source bin/activate
- pip install -r requirements.txt
- renomear arquivo settings_default.py para settings.py
- python manage.py syncdb
- python manage.py runserver 0.0.0.0:8000

procedimentos para utilização no servidor (postgresql + gunicorn + supervisor):
- sudo aptitude install gexttext
- sudo aptitude install postgresql-9.3
- sudo aptitude install python-dev
- sudo aptitude install libpq-dev
- cd ~/
- git clone https://github.com/eldioschalm/portal.git
- virtualenv portal
- cd portal
- source bin/activate
- pip install -r requirements_server.txt
- renomear arquivo settings_server_default.py para settings.py
- python manage.py syncdb
- editar o arquivo settings.py e adicionar "gunicorn" em INSTALLED_APPS
- python manage.py run_gunicorn

=======
site-eventos
============
>>>>>>> 353149c1c731a1af73a968155080ad025c1d02e5
