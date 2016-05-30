from elude_web_application.settings.base import *


DEBUG = True
INSTALLED_APPS += (
 "sslserver",
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': TEST_DATABASE_NAME,
        'USER': USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
    }
}