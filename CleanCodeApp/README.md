Setup Guide:
- check your pip and python version are matching
- run pip install -r requirements.txt
- run python install_custom_admin_black.py
- then run python manage.py migrate
- then run python manage.py runserver
- in case of port error, python manage.py runserver 8001
- (optional) to create a superuser run python manage.py createsuperuser

