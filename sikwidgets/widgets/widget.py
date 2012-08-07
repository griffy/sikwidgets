import os
import types

from sikuli.Sikuli import Location, FindFailed, Env

from sikwidgets.region_group import RegionGroup
from sikwidgets.util import capture_screenshot, hide_mouse, target_offset_region
from sikwidgets import settings

REGION_FUZZY_FACTOR = 25

class WidgetError(Exception): pass

# TODO
#               Should last_state be removed? Also, .region is really
#               a Match object at the moment. Fix this, or leave it?
#
#               All state checkers should be 'forced'
#               by default and therefore have no force_check parameter.
#               Instead, hover, click, etc. methods will use the 'cached'
#               region because they only care about a location, not the
#               underlying image.
#
#               Also, I added an offset named parameter to the methods
#               that click and hover over a region. This -should- work,
#               but it needs to be tested. Update checkboxes to use this.
#

# TODO: should widgets have a focused AND selected state? ie, a tab is 
#       selected, but it doesn't have the rectangular 'focus' thing around it.

# TODO: Should widgets have events that can be listened for by others?
#       eg, a Menu listens for on_click events of all non-menu-buttons,
#       and decides it doesn't exist if one of them fires
#      
#       Or is this too much state to be carrying around?

# FIXME: find a better place for this...
def gen_is_state_method(state):
    def is_state_method(self):
        return self == state # calls __eq__
    # for all state methods but hovered, we want
    # to hide the mouse pointer so it doesn't affect
    # the image
    # FIXME: this seems hacky
    if state != 'hovered':
        return hide_mouse(is_state_method)
    return is_state_method

class Widget(RegionGroup):
    """ Base class of all GUI elements/components.
        
        Provides helper methods for commonly called
        functions
    """
    required_states = []
    optional_states = []

    def __init__(self, parent, name=None, target_offset=None):
        RegionGroup.__init__(self, parent)
        self.region = None
        self.name = name
        self.target_offset = target_offset
        self.load_states()
        self.add_state_methods()
        self.last_state = None
        
    # FIXME: str() shouldn't return a URI.. use image_folder() method for this
    def __str__(self):
        if not self.name:
            return ""
        return os.path.join(str(self.parent), self.name.lower())

    def __eq__(self, state):
        """ Checks for a given state, either looking it
            up by a key or passing it directly.

            Note: This method is not cached (ie, force_check always True), 
                  but it will cache its result for other methods to use.
        """
        match = self.do_find(state)
        if match:
            # FIXME: should match be converted directly to a Region so we lose all
            # image info?
            self.region = match # Region(match)
            # save a slightly larger region for finding other state images as well
            self.search_region = self.region.nearby(REGION_FUZZY_FACTOR)
            self.last_state = state
            return True
        return False

    def image_folder(self):
        rel_path = os.path.join(settings.IMAGES_PATH, str(self))
        return os.path.abspath(rel_path)

    def create_image_folder(self):
        try:
            os.makedirs(self.image_folder())
        except os.error:
            return False
        return True
        
    def capture_screenshots(self):
        self.create_image_folder()

        # FIXME: check if has name before doing this? (ie, virtual widgets disallowed)
        response = raw_input("Capture screenshot(s) of '%s'? " % str(self))
        if not response.startswith('y'):
            return

        print "Required states: %s" % (', '.join(self.required_states))
        print "Optional states: %s" % (', '.join(self.optional_states))
        print "Existing states: %s" % (', '.join(self.states.keys()))

        states = raw_input("List the states, separated by commas, " +
                           "you would like to capture:\n").replace(' ', '').split(',')
        for state in states:
            capture_screenshot(state, self.image_folder(), widget=self)


    def find_states(self, path):
        self.create_image_folder()
        files = filter(lambda f: f.endswith('.png'), os.listdir(path))
        states = map(lambda f: f.split('.png')[0], files)
        for required_state in self.required_states:
            if required_state not in states:
                if settings.DEBUG:
                    print "required state '%s' for %s class not found at path: %s" % (required_state, 
                                                                                      self.__class__.__name__, 
                                                                                      path)
        state_map = {}
        for i, state in enumerate(states):
            state_map[state] = os.path.join(path, files[i])
        return state_map

    # TODO: should click_<state>, hover_<state>, etc. methods
    #       be added for free as well?
    def add_state_methods(self):
        if not self.name:
            # a nameless widget doesn't (can't) have state methods
            return
        """ Adds is_<state> methods to this instance for free """
        for state in self.states.keys():
            method_name = "is_%s" % state.lower()
            if settings.DEBUG:
                print "Adding %s method to %s class" % (method_name, self.__class__.__name__)
            method = types.MethodType(gen_is_state_method(state), self, self.__class__)
            setattr(self, method_name, method)
        # if an optional state was defined that wasn't in the
        # states list, add a method for it as well that always
        # returns false
        for optional_state in self.optional_states:
            if optional_state not in self.states:
                method_name = "is_%s" % optional_state.lower()
                if settings.DEBUG:
                    print "Adding %s method to %s class" % (method_name, self.__class__.__name__)
                method = types.MethodType((lambda self: False), self, self.__class__)
                setattr(self, method_name, method)

    def load_states(self):
        if not self.name:
            # a nameless widget doesn't (can't) have states
            return
        path = self.image_folder()
        if settings.DEBUG:
            print "Loading state images for '%s' (%s)" % (self.name, path)
        self.states = self.find_states(path)

    def exists(self, force_check=False):
        if not force_check and self.region:
            return True
        for state in self.states:
            if self == state:
                return True
        return False

    def find(self, force_check=False):
        if not self.exists(force_check):
            return None
        return self.region # FIXME: should this be a Match, or is Region enough?

    def hover(self, offset=None, force_check=False):
        if self.exists(force_check):
            offset = offset if offset is not None else self.target_offset
            self.region.hover(target_offset_region(self.region, offset))
        else:
            raise WidgetError("Unable to find widget to hover over: %s" % self.name)

    def click(self, offset=None, force_check=False):
        if self.exists(force_check):
            offset = offset if offset is not None else self.target_offset
            self.region.click(target_offset_region(self.region, offset))
        else:
            raise WidgetError("Unable to find widget to click on: %s" % self.name)

    def double_click(self, offset=None, force_check=False):
        if self.exists(force_check):
            offset = offset if offset is not None else self.target_offset
            self.region.doubleClick(target_offset_region(self.region, offset))
        else:
            raise WidgetError("Unable to find widget to double-click on: %s" % self.name)

    def right_click(self, offset=None, force_check=False):
        if self.exists(force_check):
            offset = offset if offset is not None else self.target_offset
            self.region.rightClick(target_offset_region(self.region, offset))
        else:
            raise WidgetError("Unable to find widget to right-click on: %s" % self.name)

    # TODO: make drag_to accept offset as named parameter and act much like 
    #       the above methods. Also, for drag_onto, use the target_offset of
    #       each widget implicitly.
    def drag_to(self, x, y, force_check=True):
        if self.exists(force_check):
            self.region.dragDrop(self.region, Location(x, y))
        else:
            raise WidgetError("Unable to find widget to drag: %s" % self.name)

    def drag_onto(self, widget, force_check=True):
        if not self.exists(force_check):
            raise WidgetError("Unable to find widget to drag: %s" % self.name)
        
        if not widget.exists(force_check):
            raise WidgetError("Unable to find widget to drop onto: %s" % widget.name)
        
        self.region.dragDrop(self.region, widget.region)

    # FIXME: The methods below are generic enough so as not to apply
    #        specifically to the instance or the instance's region.
    #        However, they usually do. Should they still be instance
    #        methods?
    def do(self, region, func_name, state, *args, **kwargs):
        """ Checks for the existence of the given state,
            and if it exists calls the given function with
            it as a parameter. Otherwise, it returns False
            as a safe way of indicating failure.
        """
        if settings.DEBUG:
            region.highlight(1)

        # FIXME: allow for this to be changed.
        # Use a timeout of half a second rather than
        # the default of 3
        region.setAutoWaitTimeout(0.5)

        func = getattr(region, func_name)
        if state in self.states:
            return func(self.states[state], *args, **kwargs)
        elif os.path.isfile(state):
            return func(state, *args, **kwargs)
        # FIXME: this is a hacky way of defaulting to OCR
        else:
            region_text = region.text().strip()
            if settings.DEBUG:
                print "Looking for '%s'" % state
                print "Detected '%s'" % region_text

            if region_text == state:
                if func_name == 'find':
                    return region
                elif func_name == 'exists':
                    return True
                else:
                    return func(region, *args, **kwargs)
            else:
                if func_name == 'exists':
                    return False
        return None

    # TODO: for the methods below, should parent.region be used as a secondary
    #       region to search if the first fails? It's possible that search_region
    #       could have become smaller due to finding a previous match, but now
    #       the new state image searched for is much larger and outside the
    #       fuzzy region, giving us a false negative.
    def do_find(self, state, *args, **kwargs):
        # since Find throws an exception if it fails, let's catch it and just
        # return None
        match = None
        try:
            match = self.do(self.search_region, 'find', state, *args, **kwargs)
        except FindFailed:
            pass
        return match

    def do_exists(self, state, *args, **kwargs):
        return self.do(self.search_region, 'exists', state, *args, **kwargs)

    def do_hover(self, state, *args, **kwargs):
        return self.do(self.search_region, 'hover', state, *args, **kwargs)

    def do_click(self, state, *args, **kwargs):
        return self.do(self.search_region, 'click', state, *args, **kwargs)

    def do_dragdrop(self, state, dest_region, *args, **kwargs):
        return self.do(self.search_region, 'dragDrop', state, dest_region, *args, **kwargs)

    def do_type(self, state, text, *args, **kwargs):
        return self.do(self.search_region, 'type', state, text, *args, **kwargs)