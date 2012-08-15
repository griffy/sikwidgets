from sikwidgets.widgets.widget import Widget
from sikwidgets.widgets.widget import WidgetError

class ComboBox(Widget):
    required_states = ['enabled']
    optional_states = ['disabled', 'focused', 'hovered']

    def __init__(self):
    	self.title
    	self.value = Button(self, "__value__")