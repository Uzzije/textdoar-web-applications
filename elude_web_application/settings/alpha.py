from elude_web_application.settings.base import *

DEBUG = True
INSTALLED_APPS += (

)
ALLOWED_HOSTS = [
    'https://www.textdoar.com',
    '.textdoar.com'
    ]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASE_NAME,
        'USER': ALPHA_DATABASE_USER_NAME,
        'PASSWORD': ALPHA_DATABASE_PASSWORD,
        'HOST': MYSQL_HOST_NAME,
    }
}
