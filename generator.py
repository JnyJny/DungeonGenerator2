

from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle, Bezier
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.label import Label
from kivy.vector import Vector
from kivy.logger import Logger
from kivy.clock import Clock

from room import Room
from random import randint
from scipy.spatial import Delaunay
from collections import deque, defaultdict
from itertools import combinations


class DungeonGenerator(Widget):
    
    grid = NumericProperty(11)
    n_rooms = NumericProperty(40)
    rooms = ListProperty([])
    hallways = ListProperty([])
    
    def __init__(self, rooms=None, **kwargs):
        super(DungeonGenerator, self).__init__(**kwargs)
        self.n_rooms = (rooms or self.n_rooms)


    def generate_rooms(self, n_rooms=None, clear=True):
        '''
        '''
        
        n_rooms = (n_rooms or self.n_rooms)
        
        if clear:
            self.canvas.clear()
            self.clear_widgets()
            self.rooms = []
            self.edges = []
            self.hallways = []
        
        for n in range(n_rooms):
            r = Room(text=f'{n}',
                     grid_unit=self.grid)
            self.rooms.append(r)
            self.add_widget(r)
            
        self.move_rooms(self.center)

        
    def spread_out_rooms(self, dt):
        '''
        '''
        
        if self.rooms_in_motion():
            self.collide_rooms()
            self.move_rooms()
            return False
        return True


    def identify_rooms(self, top=20, clear=False):
        '''
        '''

        if len(self.rooms) <= top:
            return True

        self.rooms = sorted(self.rooms,
                            key=lambda v:v.area,
                            reverse=True)

        for i,room in enumerate(self.rooms):
            if i < top: 
                room.background = [0,1,0,0.5]
                room.foreground = [0,1,0,1]
            else:
                room.background = [1,0,0,0.5]
                room.foreground = [1,0,0,1]

        if clear:
            self.clear_widgets(self.rooms[top:])
            self.rooms = self.rooms[:top]
        
        return True
    

    def align_rooms_to_grid(self, grid=None):
        '''
        '''

        grid = grid or self.grid
        
        for room in self.rooms:
            room.align_to_grid(grid)

    def rooms_in_motion(self):
        '''
        '''
        for room in self.rooms:
            if room.v_x or room.v_y:
                return True
        return False

    def collide_rooms(self):
        '''
        '''
        for room in self.rooms:
            room.collide_widgets(self.rooms)

    def move_rooms(self, pos=None):
        '''
        '''
        
        if pos:
            for room in self.rooms:
                room.pos = pos
            return

        for room in self.rooms:
            room.move(self.width, self.height)

    def centroid_of_rooms(self):
        '''
        '''
        Cx,Cy = 0,0
        n = len(self.rooms)
        for room in self.rooms:
            Cx += room.x
            Cy += room.y
        return  (Cx / n, Cy / n)

    def center_rooms(self, pos=None):
        '''
        '''
        
        pos = (pos or self.center)
        self.align_rooms_to_grid()
        c = self.centroid_of_rooms()
        dx = abs(c[0] - pos[0])
        dy = abs(c[1] - pos[1])
        for room in self.rooms:
            room.pos = Vector(room.pos) + (dx,dy)

    def triangulate_rooms(self):
        '''
        '''

        tris = Delaunay([room.center for room in self.rooms])
            
        for t in tris.simplices:
            for a,b in combinations([self.rooms[i] for i in t], 2):
                a.neighbors.add(b)
                b.neighbors.add(a)
                self.edges.append(Line(points=(a.center,b.center)))
                self.canvas.add(self.edges[-1])
        for room in self.rooms:
            Logger.info(f'Triangulate: room {room.text} weight {room.weight}')
                

    def prune_edges(self, clear=False):
        '''
        '''
        Logger.info(f'Prune:')

            

    def build_hallways(self):
        '''
        '''
        Logger.info(f'Hallways:')
        return False


