from sikuli.Sikuli import Region

def region_from_cells(parent_region, cells):
    """ Returns a child region based on the
        specified cells (out of 9 total) it
        is said to occupy within the parent
    """
    parent_width = parent_region.getW()
    parent_height = parent_region.getH()
    cell_width = parent_width / 3
    cell_height = parent_height / 3
    offset_x = (cells[0] % 3) * cell_width
    offset_y = (cells[0] / 3) * cell_height
    parent_loc = parent_region.getTopLeft()
    new_loc = parent_loc.offset(offset_x, offset_y)
    end_offset_x = cell_width + ((cells[-1] % 3) * cell_width)
    end_offset_y = cell_height + ((cells[-1] / 3) * cell_height)
    new_width = end_offset_x - offset_x
    new_height = end_offset_y - offset_y
    return Region(int(new_loc.getX()), 
                  int(new_loc.getY()),
                  int(new_width),
                  int(new_height))


# FIXME: rename this class
# FIXME: this class needs revised 
class RegionGroup(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.search_region = None
        if parent:
            self.within_region(parent)

    def within_region(self, region):
        """ Allows an exact region to be specified 
            as opposed to the "fuzzy" region generated
            by the within method
        """
        if hasattr(region, 'region') and region.region is not None:
            # a RegionGroup was passed in as opposed to a Region, and
            # it has an actual region that we've located. Use this
            # as our search region
            self.search_region = region.region
        elif hasattr(region, 'search_region') and region.search_region is not None:
            # a RegionGroup was passed in as opposed to a Region, and
            # it has a search region. Use this as our search region too.
            self.search_region = region.search_region
        else:
            # a standard Region was passed
            self.search_region = region
        return self

    # FIXME: change from the use of cells to an upper-left
    #        and bottom-right cell parameter to make it clearer
    #        Pass a tuple so it's just as pretty.
    def within(self, parent, cells):
        """ Takes a RegionGroup and derives a new,
            inner RegionGroup from it based on
            the given cells it will take up
        """
        return self.within_region(region_from_cells(parent.search_region, cells))

    def within_rect(self, x, y, width, height):
        """ Convenience method that creates a region based
            on the given parameters and assigns it
        """
        return self.within_region(Region(x, y, width, height))

    def inside(self, cells):
        return self.within(self, cells)