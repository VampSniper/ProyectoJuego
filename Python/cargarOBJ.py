import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class OBJ:
    def __init__(self, filename):
        self.vertices = []
        self.tex_coords = []
        self.faces = []
        self.load_model(filename)

    def load_model(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    parts = line.strip().split()
                    vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                    self.vertices.append(vertex)
                elif line.startswith('vt '):
                    parts = line.strip().split()
                    tex_coord = [float(parts[1]), float(parts[2])]
                    self.tex_coords.append(tex_coord)
                elif line.startswith('f '):
                    parts = line.strip().split()
                    face = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                    self.faces.append(face)

    def render(self):
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
        glEnd()

        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for vertex, tex_coord in zip(face, self.tex_coords):
                glTexCoord2fv(tex_coord)
                glVertex3fv(self.vertices[vertex])
        glEnd()