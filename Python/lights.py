import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Inicializar Pygame y OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glEnable(GL_DEPTH_TEST)

# Configuración de la proyección y la vista
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)
glRotatef(0, 0, 0, 0)

# Configuración de la luz
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION, [5, 5, 5, 1])  # Posición de la luz
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 0, 1])  # Color difuso (blanco)
glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 0.5, 0, 1])  # Color especular (blanco)

# Materiales
glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1, 0.5, 0, 1])
glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
glMaterialf(GL_FRONT, GL_SHININESS, 50)

# Crear un cubo para visualizar la iluminación
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

    glRotatef(100, 9, 5, 5)  # Aumenta la velocidad de rotación
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Cube()
    pygame.display.flip()
    pygame.time.wait(10)
