Automated Django CSS testing
============================

In this tutorial I will describe how we do automated CSS testing in Django, here
in [ottofeller](http://ottofeller.com). Our approach is generally based on comparing sample screenshot of page
DOM-element to one made during tests. What we need to do this is Django management
command to capture sample screenshot, [phantomjs](http://phantomjs.org/) based tool [Ghost.py](http://jeanphix.me/Ghost.py/) for in-memory rendering
and ImageDiff method of [needle](http://needle.readthedocs.org/en/latest/) python package.

In [management/command/capture.py](https://github.com/gvidon/django-screenshot-assert-tutorial/blob/master/management/commands/capture.py) we do set up test environment DB, run Django live
server and capture screenshot. It looks bit complicated, but we haven't yet found simpler solution ([this](https://docs.djangoproject.com/en/1.5/topics/testing/advanced/#running-tests-outside-the-test-runner) just doesn't work). This command accepts test case import path and
capturing test name. It will utilize `screenshot_<name>` method of test case
to capture page and save it. 

`screenshot_<name>` is also used to obtain screenshot image during tests, what it does
is actual image capturing and saving to specified directory. Its essential part
is so called webdriver Ghost.py — phantomjs based python tool that renders
page in-memory and allow to play with it's DOM in simple manner. Like this:

```python
ghost.fill('form', {
	'username': 'test',
	'password': 'password'
})

ghost.fire_on('form', 'submit', expect_loading=True)
```

Now as we have captured sample page we can later run tests. We use the same
`screenshot_<name>` method of test case and pass captured screenshot image to the needle
ImageDiff method to have the value of images differences and fail test if it is too high:

```python
if abs(ImageDiff(screenshot, sample).get_distance()) > threshold:
	raise AssertionError('Screenshot didn\'t match')
```

During tests and capturing we use custom test settings stored in [settings_test.py](https://github.com/gvidon/django-screenshot-assert-tutorial/blob/master/settings_test.py)
We overwrite DATABASE setting here to have test DB in sqlite for convenient reasons.
