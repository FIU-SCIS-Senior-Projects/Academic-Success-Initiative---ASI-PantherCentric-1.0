import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '=c-^d!fwwc8a+6d&na6hdy(u(8q47n-#a1z(pr1lkbqou98n$i'

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'analytical',
    'availabilities',
    'atrisk',
    'courses',
    'projects',
    'restrictions',
    'reports',
    'rquests',
    'semesters',
    'surveys',
    'timesheets',
    'team_leader_tools',
    'tokens',
    'tutoring_sessions',
    'custom_things',
    'suit',
    'user_profiles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'debug_toolbar', only for development!
    'channels',
    'django_extensions',
    'admindashboard'
]


ROOT_URLCONF = 'asiapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates').replace('\\','/')],
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

WSGI_APPLICATION = 'asiapp.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_FROM_EMAIL = 'no-reply@asi.cis.fiu.edu'

STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
        ]
MIXPANEL_API_TOKEN = 'a1ece7175b7fdeb1e03ebdb54e62cfd4'
MIXPANEL_SECRET = '3ab4f05a44abd335fa9dcb9118898329'

CHANNEL_LAYERS = {
        "default" : {
            "BACKEND" : "asgi_redis.RedisChannelLayer",
            "CONFIG" : {
                "hosts" : [('127.0.0.1', 6379)],
                },
            "ROUTING" : "asiapp.routing.channel_routing",
            },
}
