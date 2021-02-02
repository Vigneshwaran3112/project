import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'south_indian_coffee_pro.settings.development_settings')

application = get_wsgi_application()
