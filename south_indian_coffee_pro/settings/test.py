from .base import *

DEBUG = True

ALLOWED_HOSTS = ['tsich.test.api.vgts.tech']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {'options': '-c search_path=test'},
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

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://3292be1e5391489bbdab0790fb7895b4@o562285.ingest.sentry.io/5703500",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.2,
    send_default_pii=True,
)
