import os

# SECURITY WARNING: keep the secret key used in production secret!
from kombu import Exchange, Queue

SECRET_KEY = 'django-insecure-%+=nxz1jr)6mnu@5ma4nyn$ej-i%=asgs+zv$yu4_#b8-@91o1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Database Config:
POSTGRES_DATABASE_LOCAL = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'instagram_7learn',
    'USER': 'mohsen',
    'PASSWORD': 'root',
    'HOST': '127.0.0.1',
    'PORT': '5432',
}

POSTGRES_DATABASE = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.environ.get("POSTGRES_DB", ""),
    'USER': os.environ.get("POSTGRES_USER", ""),
    'PASSWORD': os.environ.get("POSTGRES_PASSWORD", ""),
    'HOST': os.environ.get("POSTGRES_HOST", ""),
    'PORT': os.environ.get("POSTGRES_POST", ""),
}


# Celery Config:
if DEBUG:
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
else:
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", "redis://redis:6379/0")

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = "Asia/Tehran"
CELERY_ENABLE_UTC = True
CELERY_QUEUES = {
    Queue("high", Exchange("high"), routing_key="high"),
    Queue("mid", Exchange("mid"), routing_key="mid"),
    Queue("low", Exchange("low"), routing_key="low"),
}
CELERY_DEFAULT_QUEUE = "low"