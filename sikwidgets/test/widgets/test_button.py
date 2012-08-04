import unittest
import os
import time
import shutil
from java.awt import Dimension, Robot
from sikuli.Sikuli import Match
from sikwidgets.application import Application
from sikwidgets.window import Window
from sikwidgets.test.test_case import TestCase

class ButtonTestWindow(Window):
	def contains(self):
		self.test_button = self.button('test_button')

class ButtonTestApp(Application):
	windows = [ButtonTestWindow]

class ButtonTestCase(TestCase):
	def setUp(self):
		Robot().mouseMove(800, 600)
		self.launch_app()
		self.app = ButtonTestApp()

	def tearDown(self):
		self.frame.setVisible(False)
		self.frame.dispose()

	def test___init__(self):
		button = self.app.focused_window(2).test_button
		self.assertTrue(hasattr(button, 'is_enabled'))
		self.assertTrue(hasattr(button, 'is_disabled'))
		self.assertTrue(hasattr(button, 'is_focused'))
		self.assertTrue(hasattr(button, 'is_hovered'))

	def test_is_enabled(self):
		button = self.app.focused_window(2).test_button
		self.assertTrue(button.is_enabled())

	def test_is_disabled(self):
		self.button.setEnabled(False)
		self.frame.getContentPane().revalidate()
		self.frame.getContentPane().repaint()
		button = self.app.focused_window(2).test_button
		self.assertTrue(button.is_disabled())

	def test_is_focused(self):
		self.button.setFocusable(True)
		self.frame.getContentPane().revalidate()
		self.frame.getContentPane().repaint()
		button = self.app.focused_window(2).test_button
		self.assertTrue(button.is_focused())
		
	def test_is_hovered(self):
		button = self.app.focused_window(2).test_button
		button.hover()
		self.assertTrue(button.is_hovered())

	def test___str__(self):
		expected_name = os.path.join('button_test_window', 'test_button')
		button = self.app.focused_window(2).test_button
		self.assertEqual(str(button), expected_name)

	def test_image_folder(self):
		expected_path = os.path.abspath(os.path.join('images', 'button_test_window', 'test_button'))
		button = self.app.focused_window(2).test_button
		self.assertEqual(button.image_folder(), expected_path)

	def test_create_image_folder(self):
		button = self.app.focused_window(2).test_button
		self.assertFalse(button.create_image_folder())

		path = os.path.join('images', 'button_test_window', 'test_button')
		shutil.move(os.path.join(path, 'enabled.png'), os.path.join('images', '.enabled.png.tmp'))
		shutil.move(os.path.join(path, 'disabled.png'), os.path.join('images', '.disabled.png.tmp'))
		shutil.move(os.path.join(path, 'focused.png'), os.path.join('images', '.focused.png.tmp'))
		shutil.move(os.path.join(path, 'hovered.png'), os.path.join('images', '.hovered.png.tmp'))
		shutil.rmtree(os.path.join('images', 'button_test_window', 'test_button'))
		self.assertTrue(button.create_image_folder())
		self.assertTrue(os.path.exists(path))
		shutil.move(os.path.join('images', '.enabled.png.tmp'), os.path.join(path, 'enabled.png'))
		shutil.move(os.path.join('images', '.disabled.png.tmp'), os.path.join(path, 'disabled.png'))
		shutil.move(os.path.join('images', '.focused.png.tmp'), os.path.join(path, 'focused.png'))
		shutil.move(os.path.join('images', '.hovered.png.tmp'), os.path.join(path, 'hovered.png'))

	def test_find_states(self):
		button = self.app.focused_window(2).test_button
		state_map = button.find_states(button.image_folder())
		self.assertTrue('enabled' in state_map)
		self.assertTrue('disabled' in state_map)
		self.assertTrue('focused' in state_map)
		self.assertTrue('hovered' in state_map)

	def test_load_states(self):
		button = self.app.focused_window(2).test_button
		button.load_states()
		self.assertTrue('enabled' in button.states)
		self.assertTrue('disabled' in button.states)
		self.assertTrue('focused' in button.states)
		self.assertTrue('hovered' in button.states)

	def test_exists(self):
		button = self.app.focused_window(2).test_button
		self.assertTrue(button.exists())
		self.frame.getContentPane().remove(self.button)
		self.frame.getContentPane().revalidate()
		self.frame.getContentPane().repaint()
		self.assertTrue(button.exists())
		self.assertFalse(button.exists(force_check=True))

	def test_find(self):
		button = self.app.focused_window(2).test_button
		match = button.find()
		self.assertNotEqual(match, None)
		self.assertTrue(match, isinstance(match, Match))
		self.frame.getContentPane().remove(self.button)
		self.frame.getContentPane().revalidate()
		self.frame.getContentPane().repaint()
		self.assertNotEqual(button.find(), None)
		self.assertEqual(button.find(force_check=True), None)

	def test_hover(self):
		button = self.app.focused_window(2).test_button
		button.hover()
		self.assertTrue(button.is_hovered())

	def test_click(self):
		# TODO: revise this to really test?
		button = self.app.focused_window(2).test_button
		button.click()
		self.assertTrue(button.is_hovered())

	def test_double_click(self):
		# TODO: revise this to really test?
		button = self.app.focused_window(2).test_button
		button.double_click()
		self.assertTrue(button.is_hovered())

	def test_right_click(self):
		# TODO: revise this to really test?
		button = self.app.focused_window(2).test_button
		button.right_click()
		self.assertTrue(button.is_hovered())


def suite():
	return unittest.TestLoader().loadTestsFromTestCase(ButtonTestCase)

if __name__ == "__main__":
	unittest.TextTestRunner(verbosity=2).run(suite())