import unittest
from sikwidgets import settings
from sikwidgets.test import test_application
from sikwidgets.test.widgets import test_button
from sikwidgets.test.widgets import test_check_box
from sikwidgets.test.widgets import test_menu

#settings.debug()

loader = unittest.TestLoader()
suite = loader.loadTestsFromModule(test_application)
suite.addTests(loader.loadTestsFromModule(test_button))
suite.addTests(loader.loadTestsFromModule(test_check_box))
suite.addTests(loader.loadTestsFromModule(test_menu))
unittest.TextTestRunner(verbosity=2).run(suite)
