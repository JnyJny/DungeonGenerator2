from kivy.uix.widget import Widget
from kivy.logger import Logger
from kivy.graphics import Color, Line
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from gridwidget import GridWidget

class Hallway(Widget):

    A = ListProperty()
    B = ListProperty()
    C = ListProperty()
    D = ListProperty()
    hue = NumericProperty(0)

    def __init__(self, src_room=None, dst_room=None, **kwargs):
        super(Hallway, self).__init__(**kwargs)
        self.src_id = int(src_room.text)
        self.dst_id = int(dst_room.text)
        self.hue = self.src_id / 50
        Logger.info(f'Hallway init: {self.key}')
        self.A = src_room.center
        self.B = src_room.center_x, dst_room.center_y
        self.C = dst_room.center
        self.D = dst_room.center_x, src_room.center_y

    @property
    def key(self):
        try:
            return self._key
        except AttributeError:
            pass
        self._key = ' -> '.join(map(str,sorted([self.src_id,self.dst_id])))
        return self._key
    
    def __del__(self):
        Logger.info(f'Hallway.del: {self.key}')

        

        
        
