# -*- coding: utf-8 -*-
# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *

import os
rel = lambda *x: os.path.join(os.path.dirname(os.path.abspath(__file__)), *x)
# Activate django-dbindexer for the default database
DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
AUTOLOAD_SITECONF = 'indexes'

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

INSTALLED_APPS = (
    #'django_admin_bootstrapped.bootstrap3',
    #'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'permission_backend_nonrel',
    'djangotoolbox',
    'autoload',
    'dbindexer',
    'home',
    'pytz',
    'mce_filebrowser',
    'tinymce',
    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',

)
DBINDEXER_BACKENDS = (
    'dbindexer.backends.BaseResolver',
    #'dbindexer.backends.InMemoryJOINResolver',
    'dbindexer.backends.FKNullFix',
    'dbindexer.backends.ConstantFieldJOINResolver',
)

AUTHENTICATION_BACKENDS = (
    'permission_backend_nonrel.backends.NonrelPermissionBackend',
)
MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'django.middleware.gzip.GZipMiddleware',
    'autoload.middleware.AutoloadMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'context_processors.host_name',
    'context_processors.url_upload_image',
    "django.core.context_processors.i18n",
)

SITE_ID = 1
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

PAGE_SIZE = 9
# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

STATIC_URL = '/static/'
STATIC_ROOT = rel('../../staticfiles')
STATICFILES_DIRS = (
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'static/'),
)

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)


ROOT_URLCONF = 'urls'
gettext = lambda s: s

LANGUAGE_CODE = 'vi'

LANGUAGES = (
  ('vi', gettext(u'Tiếng Việt')),
)


SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 30 * 60 #

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Ho_Chi_Minh'


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

HOST = "http://lanrungbuiquocviet.appspot.com"
#HOST = "http://localhost:8000"

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace,fullscreen",
    'theme': "advanced",
    'theme_advanced_buttons1': "formatselect,bold,italic,sizeselect,fontselect,fontsizeselect,"
                               "underline,bullist,numlist,undo,redo,"
                               "link,unlink,justifyleft,justifycenter,justifyright,justifyfull,"
                               "fullscreen,pasteword,media,charmap",
    'theme_advanced_buttons2': 'image,search,pasteword,template,media,charmap,'
                               'cleanup,grappelli_documentstructure,forecolor',
    'theme_advanced_buttons3_add' : "fullscreen",
    'extended_valid_elements': "script[type|src]",
    'theme_advanced_blockformats': "p,h2,h3,h4,h5,h6",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'theme_advanced_resizing': True,
    'file_browser_callback': 'mce_filebrowser',
    'fontsize_formats': "8pt 10pt 12pt 14pt 18pt 24pt 36pt",
}