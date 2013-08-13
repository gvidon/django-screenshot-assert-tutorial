import os
import re
import sys

from pyvirtualdisplay            import Display
from optparse                    import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.management      import call_command
from django.test.testcases       import LiveServerThread
from django.conf                 import settings
from django.db                   import connection, connections

from rew3.webdriver              import Stepan


class Command(BaseCommand):
	option_list = BaseCommand.option_list + (
		make_option('--testcase', dest='testcase', default=None, help='Import path of captured test'),
		make_option('--filename', dest='filename', default=None, help='Screenshot filename'),
		make_option('--name', default=None, help='Test name without test_ prefix'),
	)

	def handle(self, *args, **options):
		address = os.environ.get('DJANGO_LIVE_TEST_SERVER_ADDRESS')

		# Run live server on all hosts if user haven't defined hostname
		if re.match(address, '^:'):
			address = '0.0.0.0%s' % address

		try:
			host, ports = address.split(':')
		except ValueError:
			raise CommandError('Live server port not defined')

		# Get testcase class
		test_class = options['testcase'].split('.')[-1]
		module = __import__(('.').join(options['testcase'].split('.')[:-1]), fromlist=test_class)

		TestCase = getattr(module, test_class)

		# print TestCase('test_%s' % options['name'])
		# return

		# Prepare DB connection for live server
		connections_override = {}
		
		for C in connections.all():
			if (C.settings_dict['ENGINE'].rsplit('.', 1)[-1] in ('sqlite3', 'spatialite') and C.settings_dict['NAME'] == ':memory:'):
				# Explicitly enable thread-shareability for this connection
				C.allow_thread_sharing = True
				connections_override[C.alias] = C

		# Setup DB and fixtures
		db_name = connection.creation.create_test_db(verbosity=False, autoclobber=False)

		call_command('migrate')

		if hasattr(TestCase, 'fixtures'):
			call_command('loaddata', *TestCase.fixtures, **{'verbosity': False})

		# Start live server. No need to parse ports ranges for screen capturing.
		server = LiveServerThread(host, map(lambda P: int(P), re.split('\-|,', ports)), connections_override)

		server.setDaemon(False)
		server.start()
		server.is_ready.wait()

		test = TestCase('test_%s' % options['name'], **{'capture': True})

		test.server_thread = server

		getattr(test, 'screenshot_%s' % options['name'])().save(os.path.join(
			settings.SCREENSHOT_ROOT,
			'%s.png' % options.get('filename', '%s.%s' % (options['testcase'], options['name']))
		))

		# Clean up test environment
		test.driver.quit()
		server.join()
		connection.creation.destroy_test_db(db_name)