import os

from needle.diff    import ImageDiff
from django.test    import LiveServerTestCase
from django.conf    import settings

from webdriver      import Stepan


class CSSTestCase(LiveServerTestCase):
	# Is used both while sample capturing and while testing
	@classmethod
	def init_driver(self):
		self.driver = Stepan(viewport_size=(1024, 768))
		return self.driver

	@classmethod
	def setUpClass(cls):
		super(CSSTestCase, cls).setUpClass()
		cls.driver = CSSTestCase.init_driver()

	@classmethod
	def tearDownClass(cls):
		cls.driver.exit()
		super(CSSTestCase, cls).tearDownClass()

	# Convinient method for login in current application
	def login(self):
		self.driver.login(
			'%s%s' % (self.live_server_url, settings.LOGIN_URL),
			settings.TEST_USER,
			settings.TEST_PASSWORD
		)

	# Compare jsut captured screenshot to one captured before (the sample screenshot)
	def assertScreenshot(self, filename, threshold=0.01):
		from PIL import Image

		sample = Image.open(os.path.join(settings.SCREENSHOT_ROOT, '%s.png' % filename))
		screenshot = Image.open(os.path.join(settings.SCREENSHOT_TMP_ROOT, '%s.png' % filename))

		if abs(ImageDiff(screenshot, sample).get_distance()) > threshold:
			raise AssertionError('Screenshot didn\'t match')
