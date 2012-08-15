from sikwidgets.window import Window
from sikwidgets.region_group import RegionGroup

class TaskManagerWindow(Window):
    def contains(self):
        # the tabs region group is within the top third of the window
        self.tabs = RegionGroup().within(self, (1, 3))
        self.applications_tab = self.button('applications_tab').within_region(self.tabs)
        self.processes_tab = self.button('processes_tab').within_region(self.tabs)
        self.processes_table = self.table('processes_table',
           columns=['image_name',
                    'user_name',
                    'cpu',
                    'memory',
                    'description'],
           row_height=17,
           rows_per_page=15
        )