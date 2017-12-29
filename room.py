
from kivy.uix.label import Label
from kivy.properties import (NumericProperty,
                             ReferenceListProperty,
                             ListProperty)
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.vector import Vector
from kivy.logger import Logger
from random import randint
from gridwidget import GridWidget

class Room(Label, GridWidget):

    max_dim = NumericProperty(10)
    v_x = NumericProperty(0)
    v_y = NumericProperty(0)
    area = NumericProperty(0)
    velocity = ReferenceListProperty(v_x, v_y)

    def __init__(self, grid=None, direction=None, **kwargs):
        super(Room, self).__init__(**kwargs)
        self.direction = (direction or randint(0,360))
        self.velocity = Vector(self.grid_unit,0).rotate(self.direction)
        self.size = (randint(2, self.max_dim) * self.grid_unit,
                     randint(2, self.max_dim) * self.grid_unit)
        self.area = self.size[0] * self.size[1]
        self.neighbors = set()
        self.bind(size=self._update_bbox,
                  pos=self._update_bbox,
                  grid_unit=self._update_bbox)

    @property
    def weight(self):
        return len(self.neighbors)

    def _update_bbox(self, instance, value):
        '''
        
        '''
        b = self.grid_unit * 2
        self.bmin = self.x - b, self.y - b
        self.bmax = self.right + b, self.top + b

    def collide_widgets(self, others):
        '''
        '''
        return any(self.collide_widget(w) for w in others if self is not w)
    
    def collide_widget(self, other, stop=True):
        '''
        '''

        pts = [ other.pos,
                other.center,
                (other.x, other.top),
                (other.right, other.top),
                (other.right, other.y) ]

        collided = any(Vector.in_bbox(p, self.bmin, self.bmax) for p in pts)
        
        if collided:
            dv = Vector(self.pos) - Vector(other.pos)
            
            self.v_x += int(dv.x) // self.grid_unit
            self.v_y += int(dv.y) // self.grid_unit
        
        if stop and not collided:
            self.velocity = (0,0)
            
        return collided

    def align_to_grid(self, grid=None):
        '''
        '''
        grid = grid or self.grid_unit
        
        self.pos = Vector(int(self.x)//grid,int(self.y)//grid) * grid

    def move(self, width, height):
        '''
        '''
 
        if self.right >= width or self.x <= 0:
            self.v_x *= -1
        if self.top >= height or self.y <= 0:
            self.v_y *= -1
        self.pos = Vector(self.velocity) + self.pos

    def friend(self, other):
        
        self.neighbors.add(other)
        other.neighbors.add(self)

    def unfriend(self, other):

        if other in self.neighbors and self in other.neighbors:
            self.neighbors.remove(other)
            other.neighbors.remove(self)

        
        

