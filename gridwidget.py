
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty
from kivy.logger import Logger
from kivy.graphics import Line, Rectangle, Color

class GridWidget(Widget):
    '''
    '''
    grid_unit = NumericProperty(11)
    foreground = ListProperty([1,1,1,1])
    background = ListProperty([0,0,0,1])

    vlines = ListProperty([])
    hlines = ListProperty([])
    
    def __init__(self, grid_unit=11,
                 foreground=None,
                 background=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.grid_unit = grid_unit
        self.foreground = foreground or self.foreground
        self.background = background or self.background
        self.bg = Color(self.background)
        self.fg = Color(self.foreground)
        self.canvas.before.add(self.bg)
        self.canvas.add(self.fg)
        self.bind(size=self._resize)
        self.bind(grid_unit=self._resize)
        self.bind(pos=self._move)
        self.bind(foreground=self._foreground)
        self.bind(background=self._background)

    def _foreground(self, instance, value):

        self.fg.rgba = self.foreground

    def _background(self, instance, value):
        
        self.bg.rgba = self.background

    def _resize(self, instance, value):
        '''
        '''

        for l in self.vlines:
            self.canvas.remove(l)
        for l in self.hlines:
            self.canvas.remove(l)

        vdim = (self.width // self.grid_unit) + 1
        hdim = (self.height // self.grid_unit) + 1
        vsz = (1, self.height+1)
        hsz = (self.width+1, 1)
            
        self.vlines = [Rectangle(size=vsz) for _ in range(int(vdim))]
        self.hlines = [Rectangle(size=hsz) for _ in range(int(hdim))]

        for l in self.vlines:
            self.canvas.add(l) 
        for l in self.hlines:
            self.canvas.add(l)

        self._move(self, None)
        


    def _move(self, instance, value):
        '''
        '''

        for i, l in enumerate(self.vlines):
            l.pos = self.x + (self.grid_unit * i), self.y

        for i, l in enumerate(self.hlines):
            l.pos = self.x, self.y + (self.grid_unit * i)        
            


        
                

        
                
