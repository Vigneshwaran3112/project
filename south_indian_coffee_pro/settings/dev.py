from .base import *

DEBUG = True

ALLOWED_HOSTS = ['tsich.dev.api.vgts.tech', '*']

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

CORS_ALLOW_ALL_ORIGINS = True
