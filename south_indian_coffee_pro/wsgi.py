import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'south_indian_coffee_pro.settings.pro')

application = get_wsgi_application()
