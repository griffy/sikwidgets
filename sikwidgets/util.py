import re
import os
import shutil
from java.awt import Robot
from sikuli.Sikuli import SCREEN, Settings, Env, Location

# http://stackoverflow.com/a/1176023
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')
def to_snakecase(name):
    name = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', name).lower()

# http://stackoverflow.com/a/4304114
def _lower_camelcase(seq):
    it = iter(seq)
    for word in it:
        yield word.lower()
        if word.isalnum(): 
            break
    for word in it:
        yield word.capitalize()

def to_camelcase(name):
    return ''.join(_lower_camelcase(word if word else '_' for word in name.split('_')))

def to_pascalcase(name):
    new_name = to_camelcase(name)
    if len(new_name) == 1:
        new_name = new_name.capitalize()
    elif len(new_name) > 1:
        new_name = new_name[0].capitalize() + new_name[1:]
    return new_name

def sample_size(pop_size, z, p, interval):
    n0 = ((z * z) * p * (1 - p)) / (interval * interval)
    n = n0 / (1 + (n0 - 1) / pop_size)
    return n

def target_offset_region(region, offset):
    if not offset:
        return region
    # return an offset from the top-left
    return region.getTopLeft().right(offset[0]).below(offset[1])

def capture_screenshot(name, path, widget=None):
    accepted = False
    while not accepted:
        if widget:
            print "Preparing to select '%s' state of '%s'" % (name, str(widget))
        else:
            print "Preparing to select '%s' region" % name
        raw_input("Press enter when ready!")
        temp_uri = SCREEN.capture("Select '%s' region" % name)
        if not temp_uri:
            print "Unable to save screenshot!"
            response = raw_input("Would you like to try again? ")
            if not response.startswith('y'):
                accepted = True
        else:
            accepted = True
            dest_uri = os.path.join(path, "%s.png" % name)
            shutil.move(temp_uri, dest_uri)

def move_mouse(loc):
    Robot().mouseMove(loc.x, loc.y)

def hide_mouse(func):
    def wrapped(*args, **kwargs):
        original_location = Env.getMouseLocation()
        original_move_delay = Settings.MoveMouseDelay
        Settings.MoveMouseDelay = 0
        move_mouse(Location(SCREEN.getW()-1, SCREEN.getH()-1))
        result = func(*args, **kwargs)
        move_mouse(original_location)
        Settings.MoveMouseDelay = original_move_delay
        return result
    return wrapped

def clicks_per_widget(widget_size, pixels_per_scroll):
    num_clicks = 1
    if pixels_per_scroll != widget_size:
        # FIXME
        # very naively calculate how many clicks we need to
        # do to scroll a widget at a time
        if pixels_per_scroll < widget_size:
            num_clicks *= widget_size / pixels_per_scroll
        else:
            num_clicks /= pixels_per_scroll / widget_size
    return num_clicks