import os

from settings import *
from settings_local import *
from webdriver import Stepan

os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8100-8110'

TEST_USER           = ''
TEST_PASSWORD       = ''
WEBDRIVER           = Stepan

SCREENSHOT_ROOT     = os.path.join(PROJECT_ROOT, 'screenshots')
SCREENSHOT_TMP_ROOT = os.path.join(SCREENSHOT_ROOT, 'tmp')

DATABASES = {
	'default': {
		'ENGINE'   : 'django.db.backends.sqlite3',
		'USER'     : '',
		'NAME'     : 'test.db',
		'TEST_NAME': 'test.db',
		'PASSWORD' : '',
		'HOST'     : '',
		'PORT'     : '',
	}
}