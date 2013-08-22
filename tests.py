import os

from django.conf import settings
from basetestcase import CSSTestCase


class DocumentsCSSTestCase(CSSTestCase):
	fixtures = ['users', 'documents']
	
	def test_list(self):
		self.screenshot_cards()
		self.assertScreenshot('documents-list')

	def screenshot_list(self, path=settings.SCREENSHOT_TMP_ROOT):
		self.login()
		self.driver.open('%s%s' % (self.live_server_url, '/documents'))
		self.driver.click('#menu .control-button.list')
		return self.driver.capture_to(os.path.join(path, 'documents-list.png'), selector='.content')