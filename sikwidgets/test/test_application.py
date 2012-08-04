import unittest
import os
import time
import shutil
from javax.swing import JFrame, JLabel, SpringLayout
from java.awt import Dimension, Robot
from sikwidgets.application import Application
from sikwidgets.window import Window

class ApplicationTestWindow(Window):
	def contains(self):
		self.test_label = self.label('test_label')

class ApplicationTestApp(Application):
	windows = [ApplicationTestWindow]

class ApplicationTestCase(unittest.TestCase):
	def setUp(self):
		Robot().mouseMove(800, 600)
		self.launch_app()
		self.app = ApplicationTestApp()

	def tearDown(self):
		self.frame.setVisible(False)
		self.frame.dispose()

	def launch_app(self):
		self.frame = JFrame("Test Window", defaultCloseOperation=JFrame.EXIT_ON_CLOSE)
		pane = self.frame.getContentPane()
		layout = SpringLayout()
		pane.setLayout(layout)
		label = JLabel("Test Label")
		pane.add(label)
		layout.putConstraint(SpringLayout.WEST, label, 20, SpringLayout.WEST, pane)
		layout.putConstraint(SpringLayout.NORTH, label, 20, SpringLayout.NORTH, pane)
		self.frame.pack()
		self.frame.setVisible(True)
		self.frame.setSize(800, 600)

	def test_init_window(self):
		window = self.app.init_window(ApplicationTestWindow)
		self.assertNotEqual(window, None)
		self.assertTrue(isinstance(window, ApplicationTestWindow))
		self.assertEqual((window.region.getW(), window.region.getH()), (800, 600))

	def test_create_image_folders(self):
		path = os.path.join('images', 'application_test_window', 'test_label')
		shutil.move(os.path.join(path, 'enabled.png'), os.path.join('images', '.enabled.png.tmp'))
		shutil.rmtree(os.path.join('images', 'application_test_window'))
		self.app.create_image_folders()
		self.assertTrue(os.path.exists(path))
		shutil.move(os.path.join('images', '.enabled.png.tmp'), os.path.join(path, 'enabled.png'))

	# TODO: test_capture_screenshots
	# TODO: test_open

	def test_find_focused_window(self):
		window = self.app.find_focused_window()
		self.assertNotEqual(window, None)
		self.assertTrue(isinstance(window, ApplicationTestWindow))

	def test_focused_window(self):
		before_time = time.time()
		window = self.app.focused_window(10)
		after_time = time.time()
		self.assertTrue(after_time >= before_time + 10)
		self.assertNotEqual(window, None)
		self.assertTrue(isinstance(window, ApplicationTestWindow))


def suite():
	return unittest.TestLoader().loadTestsFromTestCase(ApplicationTestCase)

if __name__ == "__main__":
	unittest.TextTestRunner(verbosity=2).run(suite())