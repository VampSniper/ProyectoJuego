import pygame
from pygame.locals import *
import sys
import subprocess
from music_manager import music_manager
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from camera import Camera
from movimientos import handle_events, handle_mouse

music_manager.start_music()

def close_window_and_run_script(script_path):
    """Cierra la ventana y ejecuta el script especificado."""
    pygame.quit()
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")
    sys.exit()

def load_texture(path):
    texture_surface = pygame.image.load(path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    glEnable(GL_TEXTURE_2D)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture

def draw_axes(length):
    glBegin(GL_LINES)
    
    # Eje X - Rojo
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(length, 0.0, 0.0)

    # Eje Y - Verde
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, length, 0.0)

    # Eje Z - Azul
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, length)

    glEnd()

def pared(x, y, z, lA, lB, lC):
    return [
        #x  y  z
        ((x+lA), y, z), ((x+lA), (y+lC), z), (x, (y+lC), (z+lB)), (x, y, (z+lB)),
    ]


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Cuidado con el cadejo")
    
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    
    #display = (800, 600)
    #pygame.display.set_mode(screen, DOUBLEBUF | OPENGL)
    #gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    #glTranslatef(0.0, 0.0, -5)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    camera = Camera((0.25, 0.25, 0.25))
    camera.rot = [135.0, 0.0]
    pos_enemigo = [9.25, 0.25, 9.25]
    c = 0

    superficie = load_texture('Python/Modelos/Texturas/cesped_copy.png')
    cerca = load_texture('Python/Modelos/pictures/cerca2.jpg')
    cadejo = load_texture('Python/Modelos/pictures/cadejo1.jpg')
    #texture = load_texture('Modelos/Texturas/Madera.png')

    #Cargar objeto 3D
    #obj = OBJ('Modelos/obj/HotDog/hotdog.obj')
    lC = 1
    lA, lB = 5, 0
    paredA = pared(0,0,0,lA,lB,lC)
    lA, lB = 0, 9
    paredB = pared(0,0,0,lA,lB,lC)
    lA, lB = 5, 0
    paredC = pared(0,0,9,lA,lB,lC)
    lA, lB = 0, 9
    paredD = pared(5,0,0,lA,lB,lC)
    piso = [
        #x  y  z
        (5, 0, 0), (0, 0, 0), (0, 0, 9), (5, 0, 9),
    ]
    gen = paredA+paredB+paredC+paredD

    lC = 1
    lab0 = pared(1,0,1,1,0,lC)
    lab1 = pared(2,0,1,0,1,lC)
    lab2 = pared(2,0,2,2,0,lC)
    lab3 = pared(3,0,0,0,2,lC)
    lab4 = pared(4,0,1,0,1,lC)
    lab5 = pared(0,0,2,1,0,lC)
    lab6 = pared(1,0,2,0,1,lC)
    lab7 = pared(1,0,5,1,0,lC)
    lab8 = pared(1,0,4,0,1,lC)
    lab9 = pared(1,0,4,1,0,lC)
    lab10 = pared(2,0,3,0,1,lC)
    lab11 = pared(2,0,3,1,0,lC)
    lab12 = pared(3,0,3,0,1,lC)
    lab13 = pared(3,0,4,1,0,lC)
    lab14 = pared(4,0,3,0,2,lC)
    lab15 = pared(3,0,5,1,0,lC)
    lab16 = pared(3,0,5,0,1,lC)
    lab17 = pared(4,0,6,0,1,lC)
    lab18 = pared(3,0,7,1,0,lC)
    lab19 = pared(3,0,7,0,1,lC)
    lab20 = pared(3,0,8,1,0,lC)
    lab21 = pared(4,0,8,0,1,lC)
    lab22 = pared(1,0,8,0,1,lC) 
    lab23 = pared(1,0,8,1,0,lC)
    lab24 = pared(2,0,7,0,1,lC)
    lab25 = pared(1,0,7,1,0,lC)
    lab26 = pared(1,0,6,0,1,lC)
    lab27 = pared(1,0,6,1,0,lC)

    laberinto = lab0 + lab1 + lab2 + lab3 + lab4 + lab5 + lab6 + lab7 + lab8 + lab9 + lab10 + lab11 + lab12 + lab13 + lab14 + lab15 + lab16 + lab17 + lab18 + lab19 + lab20 + lab21 + lab22 + lab23 + lab24 + lab25 + lab26 + lab27

    tex_coords = (
        (1, 1), (1, 0), (0, 0), (0, 1),
    )

    clock = pygame.time.Clock()
    running = True

    pygame.mouse.set_pos(screen.get_width() // 2, screen.get_height() // 2)  # Centrar el cursor al inicio
    pygame.mouse.set_visible(False)  # Ocultar el cursor

    #print(vertices)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close_window_and_run_script("Python/menu.py")
            handle_mouse(camera, event)

        handle_events(camera)
        pygame.mouse.set_pos(screen.get_width() // 2, screen.get_height() // 2)

        # Obtener la posición del cursor
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        camera.rotate(mouse_dx * 0.2, mouse_dy * 0.2)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBindTexture(GL_TEXTURE_2D, cerca)

        camera.update()

        
        #pos_enemigo, c = it_follows_you(camera.pos, pos_enemigo, 25, c)

        # Dibujar ejes
        #draw_axes(2.0)

        glBegin(GL_QUADS)
        for i in range(0, len(gen), 4):
            for j in range(4):
                glTexCoord2f(tex_coords[j][0], tex_coords[j][1])
                glVertex3fv(gen[i + j])
        glEnd()

        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBindTexture(GL_TEXTURE_2D, superficie)

        glBegin(GL_QUADS)
        for i in range(0, len(piso), 4):
            for j in range(4):
                glTexCoord2f(tex_coords[j][0], tex_coords[j][1])
                glVertex3fv(piso[i + j])
        glEnd()

        glBindTexture(GL_TEXTURE_2D, cerca)

        glBegin(GL_QUADS)
        for i in range(0, len(laberinto), 4):
            for j in range(4):
                glTexCoord2f(tex_coords[j][0], tex_coords[j][1])
                glVertex3fv(laberinto[i + j])
        glEnd()

        # Renderizar el modelo
        #obj.render()

        posicion = [0,0,3]

        if (camera.pos[0] < 0):
            aux = camera.rot
            camera = Camera(((camera.pos[0] + 0.25), camera.pos[1], camera.pos[2]))
            camera.rot = aux
            #print("Posición de la cámara:", camera.pos)
        elif (camera.pos[2] < 0):
            aux = camera.rot
            camera = Camera((camera.pos[0], camera.pos[1], (camera.pos[2]+0.25)))
            camera.rot = aux
            #print("Posición de la cámara:", camera.pos)
        elif (camera.pos[0] > 5):
            aux = camera.rot
            camera = Camera(((camera.pos[0]-0.25), camera.pos[1], camera.pos[2]))
            camera.rot = aux
            #print("Posición de la cámara:", camera.pos)
        elif (camera.pos[2] > 9):
            aux = camera.rot
            camera = Camera((camera.pos[0], camera.pos[1], (camera.pos[2]-0.25)))
            camera.rot = aux
            #print("Posición de la cámara:", camera.pos)
        #print("Posición de la cámara:", camera.pos[0])
        #print("Posición de la cámara:", camera.pos[1])
        #print("Posición de la cámara:", camera.pos[2])
        #print(camera.rot)

        pygame.display.flip()
        clock.tick(60)

    pygame.mouse.set_visible(True)  # Mostrar el cursor al salir
    pygame.quit()

if __name__ == "__main__":
    main()