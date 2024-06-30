# camera.py

import pygame
from math import cos, sin, radians  
from OpenGL.GL import *

class Camera:
    def __init__(self, pos=(0, 0, 0)):
        self.pos = list(pos)
        self.rot = [0, 0]  # rotación en x, y
    
    def update(self):
        glLoadIdentity()
        glRotatef(self.rot[1], 1, 0, 0)
        glRotatef(self.rot[0], 0, 1, 0)
        glTranslatef(-self.pos[0], -self.pos[1], -self.pos[2])

    def move(self, direction, amount):
        if direction == 'forward':
            self.pos[0] += amount * sin(radians(self.rot[0]))
            self.pos[2] += amount * -cos(radians(self.rot[0]))
        if direction == 'backward':
            self.pos[0] -= amount * sin(radians(self.rot[0]))
            self.pos[2] -= amount * -cos(radians(self.rot[0]))
        if direction == 'left':
            self.pos[0] -= amount * cos(radians(self.rot[0]))
            self.pos[2] += amount * -sin(radians(self.rot[0]))
        if direction == 'right':
            self.pos[0] += amount * cos(radians(self.rot[0]))
            self.pos[2] -= amount * -sin(radians(self.rot[0]))
        #if direction == 'up':
        #    self.pos[1] += amount
        #if direction == 'down':
        #    self.pos[1] -= amount

    def rotate(self, dx, dy):
        self.rot[0] += dx
        self.rot[1] += dy
        if self.rot[1] > 90:
            self.rot[1] = 90
        elif self.rot[1] < -90:
            self.rot[1] = -90
