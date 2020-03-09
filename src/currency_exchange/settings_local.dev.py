# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's=7$c1s-&8f9*9u^1!s9fif*_^vo3w=8%j@sncl2gthb*+j(tx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'example',
        'USER': 'example',
        'PASSWORD': 'example',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
