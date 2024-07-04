# camera.py

import pygame
from math import cos, sin, radians    # Import trigonometric functions for rotation
from OpenGL.GL import * # Import OpenGL functions

class Camera:
    def __init__(self, pos=(0, 0, 0)):
        self.pos = list(pos) # Initialize camera position
        self.rot = [0, 0]  # Initialize rotation angles in x and y axes
    
    def update(self):  # Update the OpenGL camera view
        glLoadIdentity() # Reset the current matrix
        glRotatef(self.rot[1], 1, 0, 0) # Rotate around x-axis
        glRotatef(self.rot[0], 0, 1, 0) # Rotate around y-axis
        glTranslatef(-self.pos[0], -self.pos[1], -self.pos[2]) # Translate to camera position

    def move(self, direction, amount): # Move the camera in specified direction by specified amount
        if direction == 'forward':
            self.pos[0] += amount * sin(radians(self.rot[0])) # Move forward along x-axis
            self.pos[2] += amount * -cos(radians(self.rot[0])) # Move forward along z-axis
        if direction == 'backward':
            self.pos[0] -= amount * sin(radians(self.rot[0]))  # Move backward along x-axis
            self.pos[2] -= amount * -cos(radians(self.rot[0])) # Move backward along z-axis
        if direction == 'left':
            self.pos[0] -= amount * cos(radians(self.rot[0])) # Move left along x-axis
            self.pos[2] += amount * -sin(radians(self.rot[0]))  # Move left along z-axis
        if direction == 'right':
            self.pos[0] += amount * cos(radians(self.rot[0])) # Move right along x-axis
            self.pos[2] -= amount * -sin(radians(self.rot[0])) # Move right along z-axis
            # Uncomment the following lines if you want to enable vertical movement
        #if direction == 'up':
        #    self.pos[1] += amount
        #if direction == 'down':
        #    self.pos[1] -= amount

    def rotate(self, dx, dy):
        # Rotate the camera by the specified angles
        self.rot[0] += dx # Rotate around y-axis
        self.rot[1] += dy # Rotate around x-axis
        if self.rot[1] > 90:
            self.rot[1] = 90 # Limit rotation angle to prevent flipping
        elif self.rot[1] < -90:
            self.rot[1] = -90 # Limit rotation angle to prevent flipping
