from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {'options': '-c search_path=development'},
        'NAME': 'south_indian_coffee_test',
        'USER': 'dbmasteruser',
        'PASSWORD': 'S0S-GfhoBlIrIm.#-L97.z-R7I9J-8I%',
        'HOST': 'ls-db8b34df60a76c46c35bf55d1ffa56efbe9596b2.cjzymyxx2u8h.ap-south-1.rds.amazonaws.com',
        'PORT': '5432'
    }
}

CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://127.0.0.1:3000',
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3002',
    'http://localhost:3002',
    'http://sich.vgts.tech'
)
