from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9azf@n#-u!+x+w0q-t1w%7avw!7+y(pb!uf&k=!#&+=x-9fk8+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mangovodo',
        'USER': 'mangovodo',
        'PASSWORD': 'mangovodo',
        'HOST': 'pgdb',
        'PORT': 5432,
    }
}


# Braintree setup

BRAINTREE_MERCHANT_ID = '3zf89w7rxf63grkc'
BRAINTREE_PUBLIC_KEY = 'zzr53zkgn2wxvvn5'
BRAINTREE_PRIVATE_KEY = 'b573c27d06c05feab6a3a001c5c78803'

BRAINTREE_CONF = braintree.Configuration(
    braintree.Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)

# Redis config

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Celery Broker

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")

# Mail config

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
