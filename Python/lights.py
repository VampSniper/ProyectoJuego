import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# # Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glEnable(GL_DEPTH_TEST) # Enable depth buffer for 3D rendering

# Projection and view configuration
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0) # Set up camera perspective
glTranslatef(0.0, 0.0, -5) # Translate the scene on the z-axis for initial viewing
glRotatef(0, 0, 0, 0)  # Initial rotation (no rotation)

# Light configuration
glEnable(GL_LIGHTING)  # Enable lighting
glEnable(GL_LIGHT0) # Enable light 0
glLightfv(GL_LIGHT0, GL_POSITION, [5, 5, 5, 1])   # Set light position
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 0, 1])  # Set diffuse color of light (white)
glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 0.5, 0, 1])  # Set specular color of light (white)

# Materials
glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0.5, 0, 1])  # Set ambient and diffuse material
glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])  # Set specular color
glMaterialf(GL_FRONT, GL_SHININESS, 50) # Set shininess

# Create a cube for visualizing lighting
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
)

edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6),
)

def Cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glRotatef(100, 9, 5, 5)   # Increase rotation speed
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Cube()
    pygame.display.flip()
    pygame.time.wait(10)
