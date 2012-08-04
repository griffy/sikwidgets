import unittest
from java.awt import Dimension
from javax.swing import JFrame
from javax.swing import JMenuBar, JMenu, JMenuItem, JCheckBoxMenuItem
from javax.swing import SpringLayout
from javax.swing import JTabbedPane, JPanel
from javax.swing import JButton
from javax.swing import JCheckBox
from javax.swing import JComboBox
from javax.swing import JLabel
from javax.swing import JList, JScrollPane
from javax.swing import JRadioButton, ButtonGroup
from javax.swing import JSpinner, SpinnerListModel
from javax.swing import JTextField
from javax.swing import JTree
from javax.swing.tree import DefaultMutableTreeNode
from javax.swing import JTable

def build_window(self):
	self.frame = JFrame("Test Window", defaultCloseOperation=JFrame.EXIT_ON_CLOSE)
	
	# add menu bar
	self.menu_bar = JMenuBar()
	self.menu = JMenu("Test Menu")
	self.menu_bar.add(self.menu)
	self.menu_item = JMenuItem("Test Button")
	self.menu.add(self.menu_item)
	self.submenu = JMenu("Test Submenu")
	self.menu.add(self.submenu)
	self.menu_checkbox = JCheckBoxMenuItem("Test Checkbox")
	self.menu.add(self.menu_checkbox)
	self.submenu_menu_item = JMenuItem("Test Submenu Button")
	self.submenu.add(self.submenu_menu_item)
	self.frame.setJMenuBar(self.menu_bar)

	layout = SpringLayout()

	# set layout on main pane
	self.main_pane = self.frame.getContentPane()
	self.main_pane.setLayout(layout)

	# add tabs and subpanes
	self.tabbed_pane = JTabbedPane()
	self.main_pane.add(self.tabbed_pane)
	self.pane1 = JPanel(layout)
	self.pane1.setPreferredSize(Dimension(750, 500))
	self.pane2 = JPanel(layout)
	self.tabbed_pane.addTab("Test Tab 1", self.pane1)
	self.tabbed_pane.addTab("Test Tab 2", self.pane2)

	# add button
	self.button = JButton("Test Button")
	self.button.setMaximumSize(Dimension(50, 30))
	self.button.setFocusable(False)
	self.pane1.add(self.button)
	layout.putConstraint(SpringLayout.WEST, self.button, 20, SpringLayout.WEST, self.pane1)
	layout.putConstraint(SpringLayout.NORTH, self.button, 20, SpringLayout.NORTH, self.pane1)
	
	# add checkbox
	self.checkbox = JCheckBox("Test Checkbox")
	self.checkbox.setMaximumSize(Dimension(50, 30))
	self.checkbox.setFocusable(False)
	self.pane1.add(self.checkbox)
	layout.putConstraint(SpringLayout.WEST, self.checkbox, 20, SpringLayout.EAST, self.button)
	layout.putConstraint(SpringLayout.NORTH, self.checkbox, 20, SpringLayout.NORTH, self.pane1)
	
	# add combobox
	self.combobox = JComboBox(["Test Item 1", 
							   "Test Item 2", 
							   "Test Item 3", 
							   "Test Item 4", 
							   "Test Item 5"])
	self.combobox.setMaximumSize(Dimension(50, 30))
	self.combobox.setFocusable(False)
	self.pane1.add(self.combobox)
	layout.putConstraint(SpringLayout.WEST, self.combobox, 20, SpringLayout.EAST, self.checkbox)
	layout.putConstraint(SpringLayout.NORTH, self.combobox, 20, SpringLayout.NORTH, self.pane1)
	
	# add label
	self.label = JLabel("Test Label")
	self.label.setToolTipText("Test Tooltip")
	self.pane1.add(self.label)
	layout.putConstraint(SpringLayout.WEST, self.label, 20, SpringLayout.EAST, self.combobox)
	layout.putConstraint(SpringLayout.NORTH, self.label, 20, SpringLayout.NORTH, self.pane1)
	
	# add list
	self.list = JList(["Test Item 1",
					   "Test Item 2",
					   "Test Item 3",
					   "Test Item 4",
					   "Test Item 5",
					   "Test Item 6",
					   "Test Item 7",
					   "Test Item 8",
					   "Test Item 9",
					   "Test Item 10"])
	self.list.setLayoutOrientation(JList.VERTICAL)
	self.list.setVisibleRowCount(5)
	self.list_pane = JScrollPane(self.list)
	self.pane1.add(self.list_pane)
	layout.putConstraint(SpringLayout.WEST, self.list_pane, 20, SpringLayout.WEST, self.pane1)
	layout.putConstraint(SpringLayout.NORTH, self.list_pane, 20, SpringLayout.SOUTH, self.button)
	
	# add radio buttons
	self.radio_button1 = JRadioButton("Test RadioButton 1")
	self.radio_button2 = JRadioButton("Test RadioButton 2")
	self.radio_group = ButtonGroup()
	self.radio_group.add(self.radio_button1)
	self.radio_group.add(self.radio_button2)
	self.pane1.add(self.radio_button1)
	self.pane1.add(self.radio_button2)
	layout.putConstraint(SpringLayout.WEST, self.radio_button1, 20, SpringLayout.EAST, self.list_pane)
	layout.putConstraint(SpringLayout.NORTH, self.radio_button1, 20, SpringLayout.SOUTH, self.checkbox)
	layout.putConstraint(SpringLayout.WEST, self.radio_button2, 20, SpringLayout.EAST, self.radio_button1)
	layout.putConstraint(SpringLayout.NORTH, self.radio_button2, 20, SpringLayout.SOUTH, self.checkbox)
	
	# add spinner
	self.spinner = JSpinner(SpinnerListModel([
		"Test Item 1",
		"Test Item 2",
		"Test Item 3",
		"Test Item 4",
		"Test Item 5"])
	)
	self.pane1.add(self.spinner)
	layout.putConstraint(SpringLayout.WEST, self.spinner, 20, SpringLayout.WEST, self.pane1)
	layout.putConstraint(SpringLayout.NORTH, self.spinner, 20, SpringLayout.SOUTH, self.list_pane)
	
	# add textfield
	self.text_field = JTextField(20)
	self.text_field_label = JLabel("Text Field")
	self.pane1.add(self.text_field)
	self.pane1.add(self.text_field_label)
	layout.putConstraint(SpringLayout.WEST, self.text_field_label, 20, SpringLayout.EAST, self.spinner)
	layout.putConstraint(SpringLayout.NORTH, self.text_field_label, 20, SpringLayout.SOUTH, self.list_pane)
	layout.putConstraint(SpringLayout.WEST, self.text_field, 3, SpringLayout.EAST, self.text_field_label)
	layout.putConstraint(SpringLayout.NORTH, self.text_field, 20, SpringLayout.SOUTH, self.list_pane)
	
	# add tree
	self.tree_top_node = DefaultMutableTreeNode("Test Node A")
	self.tree_mid_node1 = DefaultMutableTreeNode("Test Node 1")
	self.tree_mid_node2 = DefaultMutableTreeNode("Test Node 2")
	self.tree_bottom_node = DefaultMutableTreeNode("Test Node a")
	self.tree_top_node.add(self.tree_mid_node1)
	self.tree_top_node.add(self.tree_mid_node2)
	self.tree_mid_node1.add(self.tree_bottom_node)
	self.tree = JTree(self.tree_top_node)
	self.tree.setShowsRootHandles(True)
	self.tree_pane = JScrollPane(self.tree)
	self.tree_pane.setPreferredSize(Dimension(150, 150))
	self.pane1.add(self.tree_pane)
	layout.putConstraint(SpringLayout.WEST, self.tree_pane, 20, SpringLayout.WEST, self.pane1)
	layout.putConstraint(SpringLayout.NORTH, self.tree_pane, 20, SpringLayout.SOUTH, self.spinner)
	
	# add table to second pane
	self.table_columns = ["Test Col 1",
					      "Test Col 2",
					      "Test Col 3",
					      "Test Col 4",
					      "Test Col 5"]
	self.table_data = [
		["Test Cell 1", "Test Cell 2", "Test Cell 3", "Test Cell 4", "Test Cell 5"],
		["Test Cell 6", "Test Cell 7", "Test Cell 8", "Test Cell 9", "Test Cell 10"],
		["Test Cell 1", "Test Cell 2", "Test Cell 3", "Test Cell 4", "Test Cell 5"],
		["Test Cell 6", "Test Cell 7", "Test Cell 8", "Test Cell 9", "Test Cell 10"],
		["Test Cell 0", "Test Cell 1", "Test Cell 2", "Test Cell 3", "Test Cell 4"],
		["Test Cell 1", "Test Cell 2", "Test Cell 3", "Test Cell 4", "Test Cell 5"],
		["Test Cell 6", "Test Cell 7", "Test Cell 8", "Test Cell 9", "Test Cell 10"],
		["Test Cell 1", "Test Cell 2", "Test Cell 3", "Test Cell 4", "Test Cell 5"],
		["Test Cell 6", "Test Cell 7", "Test Cell 8", "Test Cell 9", "Test Cell 10"],
		["Test Cell 11", "Test Cell 12", "Test Cell 13", "Test Cell 14", "Test Cell 15"]
	]
	self.table = JTable(self.table_data, self.table_columns)
	self.table.setPreferredScrollableViewportSize(Dimension(300, 200))
	self.table.setAutoResizeMode(JTable.AUTO_RESIZE_OFF)
	self.table_pane = JScrollPane(self.table)
	self.pane2.add(self.table_pane)
	layout.putConstraint(SpringLayout.WEST, self.table_pane, 20, SpringLayout.WEST, self.pane2)
	layout.putConstraint(SpringLayout.NORTH, self.table_pane, 20, SpringLayout.NORTH, self.pane2)
	
	self.frame.pack()
	self.frame.setVisible(True)
	self.frame.setSize(800, 600)

class TestCase(unittest.TestCase):
	def launch_app(self):
		build_window(self)