from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {'options': '-c search_path=dev'},
        'NAME': 'southindiancoffee',
        'USER': 'dbmasteruser',
        'PASSWORD': '8^uwP1$78!&|%As.HqoS)cg]41DK}_rS',
        'HOST': 'ls-f2640e88f8e1b2c149072172a99cfbe52167b5e8.cl4kxps5wa80.ap-south-1.rds.amazonaws.com',
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
