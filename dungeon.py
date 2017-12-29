#!/usr/bin/env python3

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from generator import DungeonGenerator
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.logger import Logger
from enum import Enum

class State(Enum):
    PAUSED=0
    ANIMATING=1
    DONE=5
    

class DungeonApp(App):
    '''
    '''
    generator = ObjectProperty(None)

    def reset(self, arg):
        self.state = State.ANIMATING
        self.generator.generate_rooms()
        

    def identify(self, arg):
        if self.state != State.ANIMATING:
            self.generator.identify_rooms()
            self.generator.center_rooms()
            
    def cull_rooms(self, arg):
        if self.state != State.ANIMATING:
            self.generator.identify_rooms(clear=True)
            self.generator.center_rooms()
        
    def hallways(self, arg):
        if self.state != State.ANIMATING:
            self.generator.build_hallways()
        
    def build(self):
        Window.size = (1024, 1024)
        
        self.state = State.PAUSED
        self.generator = DungeonGenerator(size=Window.size,
                                          size_hint=(.9,1))
        self.buttons = BoxLayout(orientation='horizontal', size_hint=(1,.1))

        self.btn0 = Button(text='Start', on_press=self.reset)
        self.btn1 = Button(text='Identify', on_press=self.identify)
        self.btn2 = Button(text='Cull', on_press=self.cull_rooms)
        self.btn3 = Button(text='Build Hallways', on_press=self.hallways)

        for btn in [self.btn0, self.btn1, self.btn2, self.btn3]:
            self.buttons.add_widget(btn)
            
        self.root = BoxLayout(orientation='vertical')
        self.root.add_widget(self.generator)
        self.root.add_widget(self.buttons)
            
        Clock.schedule_interval(self.update, 1/60.)
        
        return self.root

    
    def update(self, dt):
        '''
        '''

        for btn in [self.btn1, self.btn2, self.btn3]:
            btn.disabled = self.state is State.ANIMATING

        if self.state is State.PAUSED:
            return

        if self.state is State.ANIMATING:
            result = self.generator.spread_out_rooms(dt)
            if result:
                self.state = State.PAUSED
                self.generator.center_rooms()
            return


if __name__ == "__main__":
    
    DungeonApp().run()
