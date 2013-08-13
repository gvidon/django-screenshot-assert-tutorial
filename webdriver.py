import sys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.webdriver import WebDriver
from needle.driver import NeedleWebDriver


# NeedleWebDriver is required as it provide WebElement with .get_screenshot() method
# which is used for page ELEMENTS (not the whole page) capturing
class Stepan(NeedleWebDriver, WebDriver):
	def __init__(self, *args, **kwargs):
		super(Stepan, self).__init__(*args, **kwargs)
		
		# This tool is used for waiting for WebDriver certain events described in lambda
		# passed to it's methods
		self.wait = WebDriverWait(self, 30)

	# Login and wait for response
	def login(self, url, username, password):
		super(WebDriver, self).get(url)

		# Fill up and submit login form
		userinput = self.find_element_by_css_selector('input[name="username"]')

		userinput.send_keys(username)
		self.find_element_by_css_selector('input[name="password"]').send_keys(password)
		userinput.submit()

		# .container is main content part. As it is visible page is considered to be loaded
		self.wait.until(lambda D: D.find_element_by_css_selector('.container').is_displayed())

	# Go to URL and wait before page loaded including js-driven loading
	def get(self, url):
		super(WebDriver, self).get(url)
		self.wait.until(lambda D: D.find_element_by_css_selector('#module-content').is_displayed())