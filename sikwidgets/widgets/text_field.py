from sikwidgets.widgets.widget import Widget
from sikwidgets.widgets.widget import WidgetError
from sikuli.Sikuli import Key, KeyModifier

# TODO: add a default_text parameter and a text attribute?
class TextField(Widget):
    required_states = ['enabled', 'focused']
    optional_states = ['disabled', 'hovered', 'invalid']

    # TODO: method that returns the length of a string in the textfield
    
    def type(self, text, modifiers=None, force_check=False):
        if self.exists(force_check):
            if not modifiers:
                self.region.type(text)
            else:
                self.region.type(text, modifiers)

    def append_text(self, text, modifiers=None, force_check=False):
        # put the cursor at the end
        self.type(Key.END, force_check=force_check)
        self.type(text, modifiers)

    def prepend_text(self, text, modifiers=None, force_check=False):
        # put the cursor at the beginning
        self.type(Key.HOME, force_check=force_check)
        self.type(text, modifiers)

    def set_text(self, text, modifiers=None, force_check=False):
        """ Types the given text into the text field, clearing previous """
        self.type('a', KeyModifier.CTRL, force_check)
        self.type(Key.BACKSPACE)  
        self.type(text, modifiers)

    def __setattr__(self, attr, val):
        """ Syntactic sugar method so that text can be
            'assigned' to the textfield to be typed. ie,

            username = TextField(...)
            username.text = "bob"
        """
        if attr != 'text':
            Widget.__setattr__(self, attr, val)
        else:
            self.set_text(val)
            