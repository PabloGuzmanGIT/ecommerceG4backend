from datetime import timedelta
from pathlib import Path
from os import environ
from dotenv import load_dotenv
#PODRE USAR LA API DE CLOUDINARY
import cloudinary
import cloudinary.uploader
import cloudinary.api

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f+&$q)t4jz4e8u##o6*%)1$-lm=vaz^w!=z56&)=v85drx+i4e'


#######################################################
# MODO DESARROLLADOR
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []
#######################################################

#######################################################
# #modo your#modo PRODUCCION
# DEBUG = False
# #se completa cuando se usa el modo PRODUCCION
# ALLOWED_HOSTS = ['http://localhost','127.0.0.1']
#######################################################

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #librerias    
    'rest_framework',
    'cloudinary',
    
    #aplicaciones
    #'corsheaders',
     'autorizacion',
     'fac_electronica',
     'lista_producto'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #agrege el middleware de los cors
    #'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'muebleria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'muebleria.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # postgresql | sqlite3 | oracle
        'NAME': environ.get('DB_NAME'),
        'PASSWORD':environ.get('DB_PASSWORD'),
        'USER':environ.get('DB_USER'),
        'HOST':environ.get('DB_HOST'),
        'PORT':environ.get('DB_PORT')
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# sera la ruta por la cual se podra devolver todos los archivos multimedias de el proyecto
MEDIA_URL = '/archivos/'

# MEDIA > multimedia
# sirve para ubicar de donde se extraeran los archivos solicitados por la url y ademas donde se almaceran los archivo mediante el metodo default_storage
MEDIA_ROOT = BASE_DIR / 'imagenes'

#sirve para definir cuando modificamos el contenido del modelo auth_user
AUTH_USER_MODEL='autorizacion.Usuario'

# sirve para toda la configuracion de nuestro DjangoRestFramework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5, hours=1),
    'ALGORITHM': 'HS384',
    # 'SIGNING_KEY': 'mimamamemima'
}

cloudinary.config(
    cloud_name=environ.get('CLOUDINARY_NAME'),
    api_key=environ.get('CLOUDINARY_API_KEY'),
    api_secret=environ.get('CLOUDINARY_SECRET')
)

#sirve para indicar de donde cargar als configuraciones y estilos de archivos estaticos
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

#SE USA CUANDO EJECUTAMOS:: python.manage.py collectstatic
STATIC_ROOT=BASE_DIR/'staticfiles'

#configuirando cors 
#origenes permitidos, si queremos todos: CORS_ALLOWED_ORIGINS_ALL
CORS_ALLOWED_ORIGINS_ALL= True
#CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:5500']

#metodos permitidos
#por ahora usamos por defecto todos
#CORS_ALLOWED_METHODS = ['GET','POST']

#cabeceras permitidas
CORS_ALLOWED_HEADERS = ['content-type','authorization','origin']