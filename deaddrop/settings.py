import sys, os
import dj_database_url


# PATH vars

here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
PROJECT_ROOT = here("")
root = lambda *x: os.path.join(os.path.abspath(PROJECT_ROOT), *x)

sys.path.insert(0, root('apps'))

SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_FROM_NUMBER = os.environ["TWILIO_FROM_NUMBER"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# Read only flag for maintenance
READ_ONLY = False

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv("ENVIRONMENT", "") == "dev":
    DEBUG = True
else:
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

ADMINS = (
    ('Philip Deuchler', 'pbdeuchler@gmail.com'),
)

MANAGERS = ADMINS

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

CUSTOM_APPS = (
    'deaddrop.api',
)

LIBRARY_APPS = (
    'rest_framework',
    'djoser',
    'authtools',
    'rest_framework_swagger',
    # See: http://django-rest-framework.org/api-guide/authentication#tokenauthentication
    'rest_framework.authtoken',
    # 'bootstrap3',
)

INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS + LIBRARY_APPS


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

if os.getenv("ENVIRONMENT", "") == "dev":
    MIDDLEWARE_CLASSES += (
        # 'deaddrop.web.middleware.LogRequests',
        # 'deaddrop.web.middleware.ReadOnly'
    )

ROOT_URLCONF = 'deaddrop.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'deaddrop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {'default': dj_database_url.config()}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'  # 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = root('assets', 'uploads')
MEDIA_URL = '/media/'

# Additional locations of static files

STATICFILES_DIRS = (
    root('assets'),
)

STATIC_ROOT = root('growloop/staticfiles/')

TEMPLATE_DIRS = (
    root('templates'),
)

AUTH_USER_MODEL = 'authtools.User'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': '/path/to/django/debug.log',
        # },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console-verbose': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'requests-dev': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'print-debug': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ]
}

DJOSER = {
    # 'DOMAIN': 'frontend.com',
    # 'SITE_NAME': 'Frontend',
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'LOGIN_AFTER_ACTIVATION': True,
    'SEND_ACTIVATION_EMAIL': True,
}


# test settings
if len(sys.argv) > 1 and 'test' in sys.argv[1]:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/deaddrop_test.db',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }
