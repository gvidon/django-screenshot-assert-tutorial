import os

from needle.diff    import ImageDiff
from django.test    import LiveServerTestCase
from django.conf    import settings
from rew3.webdriver import Stepan


class CSSTestCase(LiveServerTestCase):
	def __init__(self, *args, **kwargs):
		# When this class instance is used for capturing setUpClass() is not called,
		# so self.driver need to be created some where else
		if kwargs.get('capture'):
			self.driver = Stepan()

		# Do not pass capture param to parent __init__
		try:
			del(kwargs['capture'])
		except KeyError:
			pass

		super(CSSTestCase, self).__init__(*args, **kwargs)

	@classmethod
	def setUpClass(cls):
		super(CSSTestCase, cls).setUpClass()
		cls.driver = Stepan()

	@classmethod
	def tearDownClass(cls):
		super(CSSTestCase, cls).tearDownClass()
		cls.driver.close()

	# This method utilizes driver's custom login() method which do the login job
	# and for page is loaded
	def login(self):
		# self.live_server_url is created by LiveServerTestCase
		self.driver.login(
			'%s%s' % (self.live_server_url, settings.LOGIN_URL),
			settings.TEST_USER,
			settings.TEST_PASSWORD
		)
	
	# Save current screenshot and compare it to captured before
	def assertScreenshot(self, selector, filename, threshold=0.01):
		from PIL import Image

		sample = Image.open(os.path.join(settings.SCREENSHOT_ROOT, '%s.png' % filename))

		screenshot = self.driver.find_element_by_css_selector(selector).get_screenshot()
		screenshot.save(os.path.join(settings.SCREENSHOT_TMP_ROOT, '%s.png' % filename))

		if abs(ImageDiff(screenshot, sample).get_distance()) > threshold:
			raise AssertionError('Screenshot didn\'t match')