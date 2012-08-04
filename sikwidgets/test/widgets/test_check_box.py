import unittest
import os
import time
import shutil
from java.awt import Dimension, Robot
from sikuli.Sikuli import Match
from sikwidgets.application import Application
from sikwidgets.window import Window
from sikwidgets.test.test_case import TestCase

# TODO: take screenshots of focused and disabled states
class CheckBoxTestWindow(Window):
	def contains(self):
		self.test_check_box = self.check_box('test_check_box', target_offset=(10, 10))

class CheckBoxTestApp(Application):
	windows = [CheckBoxTestWindow]

class CheckBoxTestCase(TestCase):
	def setUp(self):
		Robot().mouseMove(800, 600)
		self.launch_app()
		self.app = CheckBoxTestApp()

	def tearDown(self):
		self.frame.setVisible(False)
		self.frame.dispose()

	def test___init__(self):
		check_box = self.app.focused_window(2).test_check_box
		self.assertTrue(hasattr(check_box, 'is_checked'))
		self.assertTrue(hasattr(check_box, 'is_unchecked'))
		self.assertTrue(hasattr(check_box, 'is_checked_and_disabled'))
		self.assertTrue(hasattr(check_box, 'is_unchecked_and_disabled'))
		self.assertTrue(hasattr(check_box, 'is_checked_and_focused'))
		self.assertTrue(hasattr(check_box, 'is_unchecked_and_focused'))
		self.assertTrue(hasattr(check_box, 'is_checked_and_hovered'))
		self.assertTrue(hasattr(check_box, 'is_unchecked_and_hovered'))

	def test_is_checked(self):
		check_box = self.app.focused_window(2).test_check_box
		check_box.check()
		self.assertTrue(check_box.is_checked())

	def test_is_unchecked(self):
		check_box = self.app.focused_window(2).test_check_box
		check_box.uncheck()
		self.assertTrue(check_box.is_unchecked())

	def test_is_checked_and_disabled(self):
		check_box = self.app.focused_window(2).test_check_box
		check_box.check()
		self.check_box.setEnabled(False)
		self.frame.getContentPane().revalidate()
		self.frame.getContentPane().repaint()
		self.assertTrue(check_box.is_checked_and_disabled())

	def test_is_unchecked_and_disabled(self):
		check_box = self.app.focused_window(2).test_check_box
		check_box.uncheck()
		self.check_box.setEnabled(False)
		self.frame.getContentPane().revalidate()
		self.frame.getContentPane().repaint()
		self.assertTrue(check_box.is_unchecked_and_disabled())

	def test_is_checked_and_focused(self):
		check_box = self.app.focused_window(2).test_check_box
		check_box.check()
		self.check_box.setFocusable(True)
		self.frame.getContentPane().revalidate()
		self.frame.getContentPane().repaint()
		self.assertTrue(check_box.is_checked_and_focused())

	def test_is_unchecked_and_focused(self):
		check_box = self.app.focused_window(2).test_check_box
		check_box.uncheck()
		self.check_box.setFocusable(True)
		self.frame.getContentPane().revalidate()
		self.frame.getContentPane().repaint()
		self.assertTrue(check_box.is_unchecked_and_focused())

	def test_is_checked_and_hovered(self):
		check_box = self.app.focused_window(2).test_check_box
		check_box.check()
		self.assertTrue(check_box.is_checked_and_hovered())

	def test_is_unchecked_and_hovered(self):
		check_box = self.app.focused_window(2).test_check_box
		check_box.uncheck()
		self.assertTrue(check_box.is_unchecked_and_hovered())

	def test___str__(self):
		expected_name = os.path.join('check_box_test_window', 'test_check_box')
		check_box = self.app.focused_window(2).test_check_box
		self.assertEqual(str(check_box), expected_name)

	def test_image_folder(self):
		expected_path = os.path.abspath(os.path.join('images', 'check_box_test_window', 'test_check_box'))
		check_box = self.app.focused_window(2).test_check_box
		self.assertEqual(check_box.image_folder(), expected_path)

	def test_create_image_folder(self):
		check_box = self.app.focused_window(2).test_check_box
		self.assertFalse(check_box.create_image_folder())

		path = os.path.join('images', 'check_box_test_window', 'test_check_box')
		shutil.move(os.path.join(path, 'checked.png'), os.path.join('images', '.checked.png.tmp'))
		shutil.move(os.path.join(path, 'unchecked.png'), os.path.join('images', '.unchecked.png.tmp'))
		shutil.move(os.path.join(path, 'checked_and_disabled.png'), os.path.join('images', '.checked_and_disabled.png.tmp'))
		shutil.move(os.path.join(path, 'unchecked_and_disabled.png'), os.path.join('images', '.unchecked_and_disabled.png.tmp'))
		shutil.move(os.path.join(path, 'checked_and_focused.png'), os.path.join('images', '.checked_and_focused.png.tmp'))
		shutil.move(os.path.join(path, 'unchecked_and_focused.png'), os.path.join('images', '.unchecked_and_focused.png.tmp'))
		shutil.move(os.path.join(path, 'checked_and_hovered.png'), os.path.join('images', '.checked_and_hovered.png.tmp'))
		shutil.move(os.path.join(path, 'unchecked_and_hovered.png'), os.path.join('images', '.unchecked_and_hovered.png.tmp'))
		shutil.rmtree(os.path.join('images', 'check_box_test_window', 'test_check_box'))
		self.assertTrue(check_box.create_image_folder())
		self.assertTrue(os.path.exists(path))
		shutil.move(os.path.join('images', '.checked.png.tmp'), os.path.join(path, 'checked.png'))
		shutil.move(os.path.join('images', '.unchecked.png.tmp'), os.path.join(path, 'unchecked.png'))
		shutil.move(os.path.join('images', '.checked_and_disabled.png.tmp'), os.path.join(path, 'checked_and_disabled.png'))
		shutil.move(os.path.join('images', '.unchecked_and_disabled.png.tmp'), os.path.join(path, 'unchecked_and_disabled.png'))
		shutil.move(os.path.join('images', '.checked_and_focused.png.tmp'), os.path.join(path, 'checked_and_focused.png'))
		shutil.move(os.path.join('images', '.unchecked_and_focused.png.tmp'), os.path.join(path, 'unchecked_and_focused.png'))
		shutil.move(os.path.join('images', '.checked_and_hovered.png.tmp'), os.path.join(path, 'checked_and_hovered.png'))
		shutil.move(os.path.join('images', '.unchecked_and_hovered.png.tmp'), os.path.join(path, 'unchecked_and_hovered.png'))

	def test_find_states(self):
		check_box = self.app.focused_window(2).test_check_box
		state_map = check_box.find_states(check_box.image_folder())
		self.assertTrue('checked' in state_map)
		self.assertTrue('unchecked' in state_map)
		self.assertTrue('checked_and_disabled' in state_map)
		self.assertTrue('unchecked_and_disabled' in state_map)
		self.assertTrue('checked_and_focused' in state_map)
		self.assertTrue('unchecked_and_focused' in state_map)
		self.assertTrue('checked_and_hovered' in state_map)
		self.assertTrue('unchecked_and_hovered' in state_map)

	def test_load_states(self):
		check_box = self.app.focused_window(2).test_check_box
		check_box.load_states()
		self.assertTrue('checked' in check_box.states)
		self.assertTrue('unchecked' in check_box.states)
		self.assertTrue('checked_and_disabled' in check_box.states)
		self.assertTrue('unchecked_and_disabled' in check_box.states)
		self.assertTrue('checked_and_focused' in check_box.states)
		self.assertTrue('unchecked_and_focused' in check_box.states)
		self.assertTrue('checked_and_hovered' in check_box.states)
		self.assertTrue('unchecked_and_hovered' in check_box.states)

	def test_exists(self):
		check_box = self.app.focused_window(2).test_check_box
		self.assertTrue(check_box.exists())
		self.frame.getContentPane().remove(self.check_box)
		self.frame.getContentPane().revalidate()
		self.frame.getContentPane().repaint()
		self.assertTrue(check_box.exists())
		self.assertFalse(check_box.exists(force_check=True))

	def test_find(self):
		check_box = self.app.focused_window(2).test_check_box
		match = check_box.find()
		self.assertNotEqual(match, None)
		self.assertTrue(match, isinstance(match, Match))
		self.frame.getContentPane().remove(self.check_box)
		self.frame.getContentPane().revalidate()
		self.frame.getContentPane().repaint()
		self.assertNotEqual(check_box.find(), None)
		self.assertEqual(check_box.find(force_check=True), None)

	def test_hover(self):
		check_box = self.app.focused_window(2).test_check_box
		check_box.hover()
		self.assertTrue(check_box.is_checked_and_hovered() or 
						check_box.is_unchecked_and_hovered())

	def test_check(self):
		check_box = self.app.focused_window(2).test_check_box
		check_box.check()
		self.assertTrue(check_box.is_checked())


def suite():
	return unittest.TestLoader().loadTestsFromTestCase(CheckBoxTestCase)

if __name__ == "__main__":
	unittest.TextTestRunner(verbosity=2).run(suite())