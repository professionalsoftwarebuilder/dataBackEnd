import os
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = Path(__file__).resolve().parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# try:
#     SECRET_KEY = os.environ["SECRET_KEY"]
# except KeyError as e:
#     raise RuntimeError("Could not find a SECRET_KEY in environment")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv())

# Application definition

INSTALLED_APPS = [
    'drzData',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'constance',
    'django_extensions',
    'django.contrib.admindocs',
    'multiselectfield',
    'ckeditor',
    'constance.backends.database',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'duurzmWrdn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'duurzmWrdn.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NM'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWRD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        #'OPTIONS': {'sslmode': 'require'},
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'nl-nl'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# Setting Static Root
# Let op: niet "static/" zoals project setup doet, hierdoor heeft login module geen css in deployde toestand
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'Static_Code'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

LOGOUT_REDIRECT_URL = '/'

# CORS_REPLACE_HTTPS_REFERER      = True
# HOST_SCHEME                     = "https://"
# SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
# #SECURE_SSL_REDIRECT             = True
# SESSION_COOKIE_SECURE           = True
# CSRF_COOKIE_SECURE              = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
# SECURE_HSTS_SECONDS             = 1000000
# SECURE_FRAME_DENY               = True

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)


GRAPH_MODELS = {
    'all_applications': False,
    'group_models': True,
    'app_labels': ["Duurzaam Woerden", "auth"],
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

defEmailBody = """
Geachte heer/mevrouw {0},

Dit is een afspraakbevestiging van Stichting Duurzaam Woerden, wij hebben u op {1} ingeplanned voor een bezoek met een van onze energiecoaches.
Tijdens dit coachgesprek zal er een zgn "woningtour" plaatsvinden waarbij u samen met de energiecoach('s) door de woning gaat om vast te stellen waar eventueel besparingen te verwezelijken zijn en wat de staat is van de isolatie van het huis.
Het coachgesprek wordt gevoerd door {2}, hierbij kan eventueel een extra "collega energiecoach" (in opleiding) aanwezig zijn.

Wij hopen u hierbij voldoende geinformeerd te hebben, en zien u graag bij het komende coachgesprek.

Mocht u verhinderd zijn op de aangegeven datum, dan kunt u dat doorgeven via het volgende e-mail adres:
energiecoach@duurzaamwoerden.nl
(U kunt desgewenst deze e-mail beantwoorden)

Met vriendelijke groet,

Stichting Duurzaam Woerden.
"""

defEmailBodyVrg = """
Geachte heer/mevrouw {0},

U hebt op {1} in de winkel van Duurzaam Woerden een vraag gesteld aan een van de medewerkers.
We hebben uw vraag in ons systeem opgenomen en deze wordt door ons in behandeling genomen.
Wij stellen u op de hoogte wanneer wij antwoord hebben en / of vervolgactie ondernemen.
Uw vraag staat bij ons als volgt geformuleerd:

{2}.

(U kunt desgewenst op deze e-mail reageren door hem te beantwoorden)

Met vriendelijke groet,

Stichting Duurzaam Woerden.
"""

CONSTANCE_CONFIG = {
    'BEVESTIGINGSMAIL_COACHGESPR_BODY': (defEmailBody, 'E-mail bevestiging bezoek energiecoach', str),
    'BEVESTIGINGSMAIL_ADVIESCONTACTVRAAG_BODY': (defEmailBodyVrg, 'E-mail bevestiging op vraag van adviescontact', str),
    'BCC_MAILADRESS_BEVESTIGINGSMAIL_ADVIESCONTACTVRAAG': ('advies@duurzaamwoerden.nl', 'E-mailadres voor bcc mail van bevestiging adviescontact', str),
}