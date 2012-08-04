from sikwidgets.window import Window
from sikwidgets.regiongroup import RegionGroup
from sikwidgets.overlay import Overlay

class Tasks(Window):
    def contains(self):
        self.tabs = RegionGroup().within(self, range(0, 3))
        self.applications_tab = self.button('applications_tab').within_region(self.tabs)
        self.processes_tab = self.button('processes_tab').within_region(self.tabs)
        self.processes_table = self.table('processes_table',
           columns=['image_name',
                    'user_name',
                    'cpu',
                    'memory',
                    'description'],
           row_height=14
           rows_per_page=19
        )