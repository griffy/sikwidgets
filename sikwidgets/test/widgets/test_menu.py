import unittest
import os
import time
import shutil
from java.awt import Dimension, Robot
from sikuli.Sikuli import Match
from sikwidgets.application import Application
from sikwidgets.window import Window
from sikwidgets.widgets.menu import Menu
from sikwidgets.test.test_case import TestCase

class MenuTestSubmenu(Menu):
	def contains(self):
		self.test_button = self.button('test_button')

class MenuTestMenu(Menu):
	def contains(self):
		self.test_button = self.button('test_button')
		self.test_submenu_button = self.menu_button('test_submenu_button')
		self.test_submenu = self.menu(MenuTestSubmenu, self.test_submenu_button)
		self.test_check_box = self.check_box('test_check_box')

class MenuTestWindow(Window):
	def contains(self):
		self.test_menu_button = self.menu_button('test_menu_button')
		self.test_menu = self.menu(MenuTestMenu, self.test_menu_button)

class MenuTestApp(Application):
	windows = [MenuTestWindow]

class MenuTestCase(TestCase):
	def setUp(self):
		Robot().mouseMove(800, 600)
		self.launch_app()
		self.app = MenuTestApp()

	def tearDown(self):
		self.frame.setVisible(False)
		self.frame.dispose()

	# FIXME: completely rewrite this to be an actual test
	#        with proper assertions
	def test_all(self):
		window = self.app.focused_window(2)
		window.test_menu_button.click()
		self.assertTrue(window.test_menu.exists())
		window.test_menu.test_button.click()
		window.test_menu_button.click()
		window.test_menu.test_check_box.check()
		window.test_menu_button.click()
		window.test_menu.test_submenu_button.hover()
		window.test_menu.test_submenu.test_button.click()

"""
	def test___init__(self): pass

	def test___str__(self): pass

	def test_image_folder(self): pass

	def test_create_image_folder(self): pass

	def test_find_states(self): pass

	def test_load_states(self): pass

	def test_exists(self): pass

	def test_find(self): pass

	def test_hover(self): pass

	def test_click(self): pass

	def test_double_click(self): pass

	def test_right_click(self): pass
"""

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(MenuTestCase)

if __name__ == "__main__":
	unittest.TextTestRunner(verbosity=2).run(suite())