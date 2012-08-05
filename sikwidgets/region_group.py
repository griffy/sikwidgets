from sikuli.Sikuli import Region

def region_from_cells(parent_region, top_left_cell, bottom_right_cell):
    """ Returns a child region based on the
        specified cells (out of 9 total) it
        is said to occupy within the parent

        Example:
            region_from_cells(region, 1, 9)

            the returned region would be the same
            as the original.

            region_from_cells(region, 4, 9)

            the returned region would be the bottom
            two-thirds of the original region, since
            the first three cells are not occupied.
    """
    # convert the cells to a 0-index for easier computing
    top_left_cell -= 1
    bottom_right_cell -= 1
    parent_width = parent_region.getW()
    parent_height = parent_region.getH()
    cell_width = parent_width / 3
    cell_height = parent_height / 3
    start_offset_x = (top_left_cell % 3) * cell_width
    start_offset_y = (top_left_cell / 3) * cell_height
    parent_loc = parent_region.getTopLeft()
    new_loc = parent_loc.offset(start_offset_x, start_offset_y)
    end_offset_x = cell_width + ((bottom_right_cell % 3) * cell_width)
    end_offset_y = cell_height + ((bottom_right_cell / 3) * cell_height)
    new_width = end_offset_x - start_offset_x
    new_height = end_offset_y - start_offset_y
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

    def within(self, parent, cells):
        """ Takes a RegionGroup and derives a new,
            inner RegionGroup from it based on
            the given cells it will take up
        """
        return self.within_region(region_from_cells(parent.search_region, *cells))

    def within_rect(self, x, y, width, height):
        """ Convenience method that creates a region based
            on the given parameters and assigns it
        """
        return self.within_region(Region(x, y, width, height))

    def inside(self, cells):
        return self.within(self, cells)