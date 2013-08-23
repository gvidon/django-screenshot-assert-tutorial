from django.conf import settings
from ghost import Ghost


class Stepan(Ghost):
	# Login and wait for response
	def login(self, url, username, password):
		super(Stepan, self).open(url)

		# Fill up and submit login form
		self.fill('form', {
			'username': settings.TEST_USER,
			'password': settings.TEST_PASSWORD
		})

		self.fire_on('form', 'submit', expect_loading=True)

	# Go to URL and wait before page loaded including js-driven loading
	def open(self, url):
		super(Stepan, self).open(url)
		self.wait_for_selector("#module-content:not(.hidden)")