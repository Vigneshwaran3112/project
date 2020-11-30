import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'south_indian_coffee_pro.settings')

application = get_asgi_application()
