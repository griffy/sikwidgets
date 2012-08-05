import sys
import os
import optparse

from sikwidgets.util import to_pascalcase, capture_screenshot

def generate_project(name):
	if os.path.isdir(name):
		print "A folder by that name already exists. Quitting..."
		return

	# create project folder structure
	os.makedirs(name)
	os.makedirs(os.path.join(name, "images"))
	make_module(name, "windows")

	# create file templates
	create_window(name)
	create_app(name)

def save_screenshot(name):
	if name.count(',') > 0:
		names = name.split(',')
		for name in names:
			save_screenshot(name)
	else:
		path = os.path.split(name)
		if len(path) > 1:
			capture_screenshot(path[-1], os.path.join(*path[:-1]))
		else:
			capture_screenshot(name)

# TODO: add ability to capture regions as well
def capture(target_uri):
	app = None
	window = None
	widget = None

	target_parts = target_uri.split('/')
	if len(target_parts) >= 1:
		# load the app
		class_name = to_pascalcase(target_parts[0])
		app_class = get_class(target_parts[0], class_name)
		app = app_class()
		app.open()
		if not app:
			print "Unable to load '%s' app" % class_name
			return

		if len(target_parts) >= 2:
			# load the window (from within app)
			class_name = to_pascalcase(target_parts[1])
			for window_class in app.windows:
				if window_class.__name__ == class_name:
					window = app.init_window(window_class)
					break
			if not window:
				print "Unable to load '%s' window" % class_name
				return

			if len(target_parts) >= 3:
				# load the widget (from within window)
				widget_name = target_parts[2]
				for widget_instance in window.widgets:
					if widget_instance.name == widget_name:
						widget = widget_instance
						break
				if not widget:
					print "Unable to load '%s' widget" % widget_name
					return

				parent_widget = widget
				for i in range(3, len(target_parts)):
					# load the widget (from within widget)
					widget_name = target_parts[i]
					for widget_instance in widget.widgets:
						if widget_instance.name == widget_name:
							widget = widget_instance
							break
					if widget == parent_widget:
						print "Unable to load '%s' widget" % widget_name
						return

				widget.capture_screenshots()
			else:
				window.capture_screenshots()
		else:
			app.capture_screenshots()

# TODO: add block comments describing what can be done
def create_app(name):
	f = open(os.path.join(name, "%s.py" % name), "w")

	f.write("from sikwidgets.application import Application\n")
	f.write("from windows.%s_window import %sWindow\n" % (name, to_pascalcase(name)))
	f.write("\n")
	f.write("class %s(Application):\n" % to_pascalcase(name))
	f.write("\topen_cmd = ''\n")
	f.write("\twindows = [%sWindow]\n" % to_pascalcase(name))

	f.close()

# TODO: add block comments describing what can be done
def create_window(name):
	windows_path = os.path.join(name, "windows")
	f = open(os.path.join(windows_path, "%s_window.py" % name), "w")

	f.write("from sikwidgets.window import Window\n")
	f.write("from sikwidgets.region_group import RegionGroup\n")
	f.write("\n")
	f.write("class %sWindow(Window):\n" % to_pascalcase(name))
	f.write("\tdef contains(self):\n")
	f.write("\t\tpass")

	f.close()

def make_module(path, name):
	filepath = os.path.join(path, name)
	os.makedirs(filepath)
	f = open(os.path.join(filepath, "__init__.py"), "w")
	f.close()

def get_class(module_name, class_name):
	sys.path.append(os.getcwd())
	module = __import__(module_name)
	return getattr(module, class_name)


if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option('-n', '--new', 
					  dest='new_project',
	                  help='Generates the scaffolding for a new sikwidgets project')
	parser.add_option('-c', '--capture', 
		              dest='capture_target',
					  help='Lets you take screenshots of various windows and widgets in your project')
	parser.add_option('-s', '--screenshot',
					  dest='screenshot_name',
					  help='Saves a single screenshot of a selected region to the given name')
	args = vars(parser.parse_args()[0])

	if args['new_project'] is not None:
		generate_project(args['new_project'])
	elif args['capture_target'] is not None:
		capture(args['capture_target'])
	elif args['screenshot_name'] is not None:
		save_screenshot(args['screenshot_name'])