import os

from sikwidgets.widgets.widget import Widget
from sikwidgets.widgets.widget import WidgetError
from sikwidgets.widgets.button import Button
from sikwidgets import settings

class ScrollableWidget(Widget):
    def __init__(self, parent, name):
        Widget.__init__(self, parent, name)

        # create a virtual widget to hold our buttons
        # TODO: is it worth it to create a Scrollbar widget?
        self._scrollbar = Widget(self, "__scrollbar__")
        # create the 4 directional scrollbar buttons
        self._top_button = Button(self._scrollbar, "top")
        self._bottom_button = Button(self._scrollbar, "bottom")
        self._left_button = Button(self._scrollbar, "left")
        self._right_button = Button(self._scrollbar, "right")

    def capture_screenshots(self):
        # take screenshots of the scrollbar states
        self._top_button.capture_screenshots()
        self._bottom_button.capture_screenshots()
        self._left_button.capture_screenshots()
        self._right_button.capture_screenshots()

    def has_vertical_scrollbar(self):
        return (self._top_button.exists(force_check=True) and 
                self._bottom_button.exists(force_check=True))

    def has_horizontal_scrollbar(self):
        return (self._left_button.exists(force_check=True) and 
                self._right_button.exists(force_check=True))

    def is_scrollable(self):
        """ Although a widget could be scrollable, it may
            not actually be. First, check if scroll states 
            actually exist. Second, look for them in the
            current widget.

            It should be noted that this method checks if
            a widget is capable of being scrolled *at this
            moment in time*
        """
        return self.has_vertical_scrollbar() or self.has_horizontal_scrollbar()

    def scrollbar_at_top(self):
        if not self.has_vertical_scrollbar():
            return True
        return self._top_button.is_touching()

    def scrollbar_at_bottom(self):
        if not self.has_vertical_scrollbar():
            return True
        return self._bottom_button.is_touching()

    def scrollbar_at_left(self):
        if not self.has_horizontal_scrollbar():
            return True
        return self._left_button.is_touching()

    def scrollbar_at_right(self):
        if not self.has_horizontal_scrollbar():
            return True
        return self._right_button.is_touching()

    def scroll_up(self, amount=1):
        for i in range(amount):
            if self.scrollbar_at_top():
                # return how many we scrolled before 
                # reaching the top
                return i
            self._top_button.click()
        # we scrolled the full amount
        return amount

    def scroll_down(self, amount=1):
        for i in range(amount):
            if self.scrollbar_at_bottom():
                return i
            self._bottom_button.click()
        return amount

    def scroll_left(self, amount=1):
        for i in range(amount):
            if self.scrollbar_at_left():
                return i
            self._left_button.click()
        return amount

    def scroll_right(self, amount=1):
        for i in range(amount):
            if self.scrollbar_at_right():
                return i
            self._right_button.click()
        return amount
        
    def scroll_to_top(self):
        while self.scroll_up(): pass

    def scroll_to_bottom(self):
        while self.scroll_down(): pass

    def scroll_to_left(self):
        while self.scroll_left(): pass

    def scroll_to_right(self):
        while self.scroll_right(): pass

