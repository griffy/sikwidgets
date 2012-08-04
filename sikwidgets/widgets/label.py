from sikwidgets.widgets.widget import Widget
from sikwidgets.widgets.widget import WidgetError

# TODO: is a label really a TextField, and my TextField is actually a TextInput?
class Label(Widget):
    required_states = ['enabled']
    optional_states = ['disabled', 'hovered']
