import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

class OBJ:
    def __init__(self, filename, texture_file, position=(0, 0, 0), scale=(1, 1, 1)):
        self.vertices = []
        self.tex_coords = []
        self.faces = []
        self.position = position
        self.scale = scale
        self.texture_id = self.load_texture(texture_file)
        self.load_model(filename)
        self.calculate_dimensions()

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
                    face = []
                    for part in parts[1:]:
                        vals = part.split('/')
                        vertex_index = int(vals[0]) - 1
                        tex_coord_index = int(vals[1]) - 1 if len(vals) > 1 and vals[1] else -1
                        face.append((vertex_index, tex_coord_index))
                    self.faces.append(face)

    def calculate_dimensions(self):
        vertices = np.array(self.vertices)
        self.min_coords = vertices.min(axis=0)
        self.max_coords = vertices.max(axis=0)
        self.size = self.max_coords - self.min_coords
        print(f"Original size: {self.size}")

    def load_texture(self, texture_file):
        texture_surface = Image.open(texture_file)
        texture_data = texture_surface.tobytes("raw", "RGB", 0, -1)
        width, height = texture_surface.size

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture_id

    def render(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glScalef(*self.scale)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for vertex, tex_coord in face:
                if tex_coord != -1:
                    glTexCoord2fv(self.tex_coords[tex_coord])
                glVertex3fv(self.vertices[vertex])
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glTranslatef(0.0, 0.0, -5)
    
    obj = OBJ("Python/Modelos/obj/source/dog.obj", "Python/Modelos/Texturas/dog.tga.png")  # Replace with your OBJ file and texture paths

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        obj.render()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
