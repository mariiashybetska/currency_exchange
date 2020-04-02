from currency_exchange.settings import *

DEBUG = False
ALLOWED_HOSTS = ['*']

CELERY_ALWAYS_EAGER = True
CELERY_TASK_ALWAYS_EAGER = True


DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
}

EMAIL_BACKEND = 'django.core.mail.outbox'