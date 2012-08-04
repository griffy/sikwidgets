from sikwidgets.widgets.page import Page
from sikwidgets.widgets.radio_button import RadioButton
from sikwidgets.widgets.widget import WidgetError

# TODO: https://answers.launchpad.net/sikuli/+question/183688

class MenuButton(RadioButton): # a button that spawns a menu
	def click(self, offset=None):
		previously_selected = self.selected
		RadioButton.click(self, offset)
		if previously_selected:
			self.selected = False
			
# FIXME: what if a child button is clicked resulting in the menu disappearing?
class Menu(Page): pass
"""
	def __init__(self, parent, source_widget, name=None):
		Page.__init__(self, parent, source_widget, name)
		self.region_exists = False
		self.changed_regions = []
		self.parent.region.onChange(self.region_changed)
		self.parent.region.observe(background=True)

	def region_changed(self, event):
		if not self.source_widget.selected:
			return


	def appeared(self, event):
		self.region_exists = True
		self.changed_regions = event.changes

	def disappeared(self, event):
		self.region_exists = False
"""
#class ContextMenu(Menu): pass
# TODO: is there anything special about the context menu that can't
#       be handled by the regular menu class? location and the source
#       widget are the only things different that come to mind.

#       Or perhaps Menu should be the 'context menu', and DropDownMenu
#       inherits from it, placing it in a specific location?

# class DropDownMenu(Menu): pass



# Example usage:
#class ViewMenu(Menu):
#	class ToolbarsMenu(Menu):
#		def contains(self):
#			self.menu_bar_entry = self.checkbox()
#			# ...
#
#	def contains(self):
#		self.toolbars = self.button('toolbars')
#		self.toolbars_menu = self.menu(ToolbarsMenu, self.toolbars)
#
#class SomeWindow(Window):
#	def contains(self):
#       self.view_button = self.button('view_button', group=0, )
#		self.view_menu = self.menu(ViewMenu, self.view_button)
