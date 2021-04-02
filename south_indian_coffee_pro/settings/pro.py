from .base import *

DEBUG = False

ALLOWED_HOSTS = ['tsich.api.vgts.tech']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'SouthIndianCoffee-Production',
        'USER': 'dbmasteruser',
        'PASSWORD': 'S0S-GfhoBlIrIm.#-L97.z-R7I9J-8I%',
        'HOST': 'ls-db8b34df60a76c46c35bf55d1ffa56efbe9596b2.cjzymyxx2u8h.ap-south-1.rds.amazonaws.com',
        'PORT': '5432'
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 86400
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

CORS_ORIGIN_WHITELIST = ('https://tsich.vgts.tech', )

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://a1eb474c173d404089eb5893b0d10b82@o562285.ingest.sentry.io/5703503",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.2,
    send_default_pii=True,
)
