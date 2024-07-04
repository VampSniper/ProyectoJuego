import pygame
import random
from pygame.locals import *  # Import essential Pygame constants and functions
import sys  # Import system-specific parameters and functions
import subprocess  # Import subprocess for running external commands
from music_manager import music_manager  # Import custom music manager
from OpenGL.GL import *  # Import OpenGL functions
from OpenGL.GLU import *  # Import OpenGL Utility Library functions
import math  # Import math for mathematical functions
from camera import Camera  # Import custom Camera class
from movimientos import handle_events, handle_mouse  # Import custom event handlers
from cargarOBJ import OBJ  # Import custom OBJ loader

# Start the music using the custom music manager
music_manager.start_music()

def load_clouds (): # Define the function 'load_clouds'
    y = 5 # Set the y-coordinate to 5
    clouds = list()  # Initialize an empty list to store the cloud vertices
    costados = list() # Initialize an empty list to store the side vertices
    for i in range(0,20,1): # Loop 20 times, incrementing by 1 each time
        coord_x = random.randint(-2, 7) # Generate a random x-coordinate between -2 and 7
        coord_z = random.randint(-2, 11)  # Generate a random z-coordinate between -2 and 11
         # Add vertices for the bottom face of the cloud
        clouds += [
            #x  y  z
            ((coord_x+1), y, coord_z), (coord_x, y, coord_z), (coord_x, y, (coord_z+1)), ((coord_x+1), y, (coord_z+1)),
        ]
         # Add vertices for the top face of the cloud
        clouds += [
            #x  y  z
            ((coord_x+1), (y+1), coord_z), (coord_x, (y+1), coord_z), (coord_x, (y+1), (coord_z+1)), ((coord_x+1), (y+1), (coord_z+1)),
        ]
        # Add vertices for the front face of the side
        costados += [
            ((coord_x+1), y, coord_z), (coord_x, y, coord_z), (coord_x, (y+1), coord_z), ((coord_x+1), (y+1), coord_z),
        ]
        # Add vertices for the back face of the side
        costados += [
            ((coord_x+1), y, (coord_z+1)), (coord_x, y, (coord_z+1)), (coord_x, (y+1), (coord_z+1)), ((coord_x+1), (y+1), (coord_z+1)),
        ]
        # Add vertices for the right face of the side
        costados += [
            ((coord_x+1), y, (coord_z+1)), ((coord_x+1), y, coord_z), ((coord_x+1), (y+1), coord_z), ((coord_x+1), (y+1), (coord_z+1)),
        ]
        # Add vertices for the left face of the side
        costados += [
            (coord_x, y, (coord_z+1)), (coord_x, y, coord_z), (coord_x, (y+1), coord_z), (coord_x, (y+1), (coord_z+1)),
        ]
    return clouds, costados

def close_window_and_run_script(script_path):
    """Cierra la ventana y ejecuta el script especificado."""
    pygame.quit() # Quit Pygame
    try:
        subprocess.run([sys.executable, script_path], check=True)  # Run the script
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")  # Print error if script fails
    sys.exit()  # Exit the program

def load_texture(path):
     # Load the texture image
    texture_surface = pygame.image.load(path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
    width = texture_surface.get_width()
    height = texture_surface.get_height()
    
    # Enable 2D texture mapping

    glEnable(GL_TEXTURE_2D)
    texture = glGenTextures(1)  # Generate a new texture ID
    glBindTexture(GL_TEXTURE_2D, texture) # Bind the texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data) # Specify texture
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # Set texture wrapping
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) # Set texture filtering
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture # Return the texture ID

# Moves the enemy towards the player
def it_follows_you(pos_jugador, pos_enemigo, v, c, obj):
    pos_enemigo = list(pos_enemigo) # Ensure enemy_pos is a list
    #print(f"E: {pos_enemigo[0]} - J: {pos_jugador[0]} - DX: {pos_enemigo[0] - pos_jugador[0]}")
    if c <= v:
        c+=1  # Increment the counter 
        #print (c)
    else:
        c = 0 # Reset the counter
          # Determine direction towards the player
        if (pos_enemigo[0] - pos_jugador[0]) > 0:
            if (pos_enemigo[2] - pos_jugador[2]) > 0:
                if(pos_enemigo[0] - pos_jugador[0] < 0.25) and (pos_enemigo[2] - pos_jugador[2] < 0.25):
                    #print("atrapado")
                    close_window_and_run_script("Python/muerte.py") #Close and run the death script 
                    pos_enemigo = pos_jugador
                else:
                    if pos_enemigo[0] - pos_jugador[0] < 0.25:
                        obj.set_rotation((0, 180, 0))
                        pos_enemigo[0] = pos_jugador[0]
                        pos_enemigo[2] -= 0.25
                    elif pos_enemigo[2] - pos_jugador[2] < 0.25:
                        obj.set_rotation((0, 270, 0))
                        pos_enemigo[2] = pos_jugador[2]
                        pos_enemigo[0] -= 0.25
                    else:
                        obj.set_rotation((0, 225, 0))
                        pos_enemigo[0] -= 0.25
                        pos_enemigo[2] -= 0.25
                #print(f" + + E: {pos_enemigo[0]} , {pos_enemigo[2]} - J: {pos_jugador[0]} , {pos_jugador[2]} - DXY: {pos_enemigo[0] - pos_jugador[0]} , {pos_enemigo[2] - pos_jugador[2]}")
            elif (pos_enemigo[2] - pos_jugador[2]) < 0:
                if(pos_enemigo[0] - pos_jugador[0] < 0.25) and (pos_enemigo[2] - pos_jugador[2] > -0.25):
                    #print("atrapado")
                    close_window_and_run_script("Python/muerte.py")
                    pos_enemigo = pos_jugador
                else:
                    if pos_enemigo[0] - pos_jugador[0] < 0.25:
                        obj.set_rotation((0, 360, 0))
                        pos_enemigo[0] = pos_jugador[0]
                        pos_enemigo[2] += 0.25
                    elif pos_enemigo[2] - pos_jugador[2] > -0.25:
                        obj.set_rotation((0, 270, 0))
                        pos_enemigo[2] = pos_jugador[2]
                        pos_enemigo[0] -= 0.25
                    else:
                        obj.set_rotation((0, 315, 0))
                        pos_enemigo[0] -= 0.25
                        pos_enemigo[2] += 0.25
                #print(f" + - E: {pos_enemigo[0]} , {pos_enemigo[2]} - J: {pos_jugador[0]} , {pos_jugador[2]} - DXY: {pos_enemigo[0] - pos_jugador[0]} , {pos_enemigo[2] - pos_jugador[2]}")
            else:
                if(pos_enemigo[0] - pos_jugador[0] < 0.25) and (pos_enemigo[2] - pos_jugador[2] > -0.25):
                    #print("atrapado")
                    close_window_and_run_script("Python/muerte.py")
                    pos_enemigo = pos_jugador
                else:
                    if pos_enemigo[0] - pos_jugador[0] < 0.25:
                        print("XD1")
                        pos_enemigo[0] = pos_jugador[0]
                    else:
                        print("XD2")
                        pos_enemigo[0] -= 0.25
                #print(f" + N/A E: {pos_enemigo[0]} , {pos_enemigo[2]} - J: {pos_jugador[0]} , {pos_jugador[2]} - DXY: {pos_enemigo[0] - pos_jugador[0]} , {pos_enemigo[2] - pos_jugador[2]}")
        elif (pos_enemigo[0] - pos_jugador[0]) < 0:
            if (pos_enemigo[2] - pos_jugador[2]) > 0:
                if(pos_enemigo[0] - pos_jugador[0] > -0.25) and (pos_enemigo[2] - pos_jugador[2] < 0.25):
                    #print("atrapado")
                    close_window_and_run_script("Python/muerte.py")
                    pos_enemigo = pos_jugador
                else:
                    if pos_enemigo[0] - pos_jugador[0] > -0.25:
                        obj.set_rotation((0, 180, 0))
                        pos_enemigo[0] = pos_jugador[0]
                        pos_enemigo[2] -= 0.25
                    elif pos_enemigo[2] - pos_jugador[2] < 0.25:
                        obj.set_rotation((0, 90, 0))
                        pos_enemigo[2] = pos_jugador[2]
                        pos_enemigo[0] += 0.25
                    else:
                        obj.set_rotation((0, 135, 0))
                        pos_enemigo[0] += 0.25
                        pos_enemigo[2] -= 0.25
                #print(f" - + E: {pos_enemigo[0]} , {pos_enemigo[2]} - J: {pos_jugador[0]} , {pos_jugador[2]} - DXY: {pos_enemigo[0] - pos_jugador[0]} , {pos_enemigo[2] - pos_jugador[2]}")
            elif (pos_enemigo[2] - pos_jugador[2]) < 0:
                if(pos_enemigo[0] - pos_jugador[0] > -0.25) and (pos_enemigo[2] - pos_jugador[2] > -0.25):
                    #print("atrapado")
                    close_window_and_run_script("Python/muerte.py")
                    pos_enemigo = pos_jugador
                else:
                    if pos_enemigo[0] - pos_jugador[0] > -0.25:
                        obj.set_rotation((0, 0, 0))
                        pos_enemigo[0] = pos_jugador[0]
                        pos_enemigo[2] += 0.25
                    elif pos_enemigo[2] - pos_jugador[2] > -0.25:
                        obj.set_rotation((0, 90, 0))
                        pos_enemigo[2] = pos_jugador[2]
                        pos_enemigo[0] += 0.25
                    else:
                        obj.set_rotation((0, 45, 0))
                        pos_enemigo[0] += 0.25
                        pos_enemigo[2] += 0.25
                #print(f" - - E: {pos_enemigo[0]} , {pos_enemigo[2]} - J: {pos_jugador[0]} , {pos_jugador[2]} - DXY: {pos_enemigo[0] - pos_jugador[0]} , {pos_enemigo[2] - pos_jugador[2]}")
            else:
                if(pos_enemigo[0] - pos_jugador[0] > -0.25) and (pos_enemigo[2] - pos_jugador[2] > -0.25):
                    #print("atrapado")
                    close_window_and_run_script("Python/muerte.py")
                    pos_enemigo = pos_jugador
                else:
                    if pos_enemigo[0] - pos_jugador[0] > -0.25:
                        pos_enemigo[0] = pos_jugador[0]
                    else:
                        pos_enemigo[0] += 0.25
                #print(f" - - E: {pos_enemigo[0]} , {pos_enemigo[2]} - J: {pos_jugador[0]} , {pos_jugador[2]} - DXY: {pos_enemigo[0] - pos_jugador[0]} , {pos_enemigo[2] - pos_jugador[2]}")
        else:
            if (pos_enemigo[2] - pos_jugador[2]) > 0:
                if(pos_enemigo[0] - pos_jugador[0] > -0.25) and (pos_enemigo[2] - pos_jugador[2] < 0.25):
                    #print("atrapado")
                    close_window_and_run_script("Python/muerte.py")
                    pos_enemigo = pos_jugador
                else:
                    if pos_enemigo[0] - pos_jugador[0] > -0.25:
                        obj.set_rotation((0, 180, 0))
                        pos_enemigo[0] = pos_jugador[0]
                        pos_enemigo[2] -= 0.25
                    elif pos_enemigo[2] - pos_jugador[2] < 0.25:
                        obj.set_rotation((0, 90, 0))
                        pos_enemigo[2] = pos_jugador[2]
                        pos_enemigo[0] += 0.25
                    else:
                        obj.set_rotation((0, 135, 0))
                        pos_enemigo[0] += 0.25
                        pos_enemigo[2] -= 0.25
                #print(f" - + E: {pos_enemigo[0]} , {pos_enemigo[2]} - J: {pos_jugador[0]} , {pos_jugador[2]} - DXY: {pos_enemigo[0] - pos_jugador[0]} , {pos_enemigo[2] - pos_jugador[2]}")
            elif (pos_enemigo[2] - pos_jugador[2]) < 0:
                if(pos_enemigo[0] - pos_jugador[0] > -0.25) and (pos_enemigo[2] - pos_jugador[2] > -0.25):
                    #print("atrapado")
                    close_window_and_run_script("Python/muerte.py")
                    pos_enemigo = pos_jugador
                else:
                    if pos_enemigo[0] - pos_jugador[0] > -0.25:
                        obj.set_rotation((0, 360, 0))
                        pos_enemigo[0] = pos_jugador[0]
                        pos_enemigo[2] += 0.25
                    elif pos_enemigo[2] - pos_jugador[2] > -0.25:
                        obj.set_rotation((0, 90, 0))
                        pos_enemigo[2] = pos_jugador[2]
                        pos_enemigo[0] += 0.25
                    else:
                        obj.set_rotation((0, 45, 0))
                        pos_enemigo[0] += 0.25
                        pos_enemigo[2] += 0.25
                #print(f" - - E: {pos_enemigo[0]} , {pos_enemigo[2]} - J: {pos_jugador[0]} , {pos_jugador[2]} - DXY: {pos_enemigo[0] - pos_jugador[0]} , {pos_enemigo[2] - pos_jugador[2]}")
            else:
                #print("atrapado")
                close_window_and_run_script("Python/muerte.py")
                pos_enemigo = pos_jugador
    return pos_enemigo, c

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

def labBin(archivo):
    with open(archivo, 'r') as file:
        lineas = file.readlines()
        a = [[0 for _ in range(19)] for _ in range(11)]
        for i in range(0, 11, 1):
            if i < len(lineas):
                b = ''.join(lineas[i][j] for j in range(1, 57, 3))  # Saltear columnas de por medio

                for j in range(min(19, len(b))):
                    a[i][j] = b[j]
    return a


def Cube():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    
    # Configures Lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    light_position = [1.0, 1.0, 1.0, 0.0]  # Light Position
    light_diffuse = [1.0, 1.0, 1.0, 1.0]   # Light color
    light_specular = [1.0, 1.0, 1.0, 1.0]  # Specular light color
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    vertices = (
    (1, 21, -1),  
    (1, 23, -1),  
    (-1, 23, -1), 
    (-1, 21, -1), 
    (1, 21, 1),   
    (1, 23, 1),   
    (-1, 21, 1),  
    (-1, 23, 1), 
)
    vertices_ajustados = tuple(
    (x, y + 15, z - 5)
    for x, y, z in vertices
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

    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices_ajustados[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices_ajustados[vertex])
    glEnd()


def main():
    pygame.init()  # Initialize Pygame
    screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL) # Set up display
    pygame.display.set_caption("Cuidado con el cadejo")
    
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (800 / 600), 0.1, 50.0)  # Set up OpenGL perspective projection
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_TEXTURE_2D)
    glTranslatef(0.0, 0.0, -5)

    camera = Camera((0.25, 0.5, 0.25))  # Initialize the camera
    camera.rot = [135.0, 0.0]
    #pos_enemigo = [4.25, 0.25, 8.25]
    cam = [0, 0]
    posCam = [0.25,0.25]
    c = 0
    anchoAA = [10,8,6,4,2,0]
    largoAA = [1,3,5,7,9,11,13,15,17]
    anchoAB = [9,7,5,3,1]
    largoBB = [0,2,4,6,8,10,12,14,16,18]

 # Load textures
    superficie = load_texture('Python/Modelos/pictures/skybox_bosque_abajo.jpg')
    cerca = load_texture('Python/Modelos/pictures/skybox_bosque_atras.jpg')
    victory = load_texture('Python/Modelos/pictures/victoria1.jpg')
    tex_clouds = load_texture('Python/Modelos/pictures/victoria1.jpg')
    #cadejo = load_texture('Python/Modelos/pictures/cadejo1.jpg')
    #texture = load_texture('Modelos/Texturas/Madera.png')
#Loads 3D object
    obj = OBJ("Python/Modelos/obj/source/dog.obj", "Python/Modelos/Texturas/dog.tga.png")

    
    #obj = OBJ('Modelos/obj/HotDog/hotdog.obj')
    
    # Load and initialize walls
    lC = 1
    lA, lB = 5, 0
    paredA = pared(0,0,0,lA,lB,lC)
    lA, lB = 0, 9
    paredB = pared(0,0,0,lA,lB,lC)
    lA, lB = 2, 0
    paredC = pared(0,0,9,lA,lB,lC)
    lA, lB = 0, 9
    paredD = pared(5,0,0,lA,lB,lC)
    lA, lB = 2, 0
    paredE = pared(3,0,9,lA,lB,lC)

    lA, lB = 1, 0
    paredV = pared(2,0,9,lA,lB,lC)

# Define floor vertices

    piso = [
        #x  y  z
        (5, 0, 0), (0, 0, 0), (0, 0, 9), (5, 0, 9),
    ]
    # Combine all walls into a single list
    gen = paredA+paredB+paredC+paredD+paredE
    
    # Load and initialize labyrinth walls
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

# Combine all labyrinth walls into a single list

    laberinto = lab0 + lab1 + lab2 + lab3 + lab4 + lab5 + lab6 + lab7 + lab8 + lab9 + lab10 + lab11 + lab12 + lab13 + lab14 + lab15 + lab16 + lab17 + lab18 + lab19 + lab20 + lab21 + lab22 + lab23 + lab24 + lab25 + lab26 + lab27
# Define texture coordinates

    tex_coords = (
        (1, 1), (1, 0), (0, 0), (0, 1),
    )

    clock = pygame.time.Clock() 
    running = True

    pygame.mouse.set_pos(screen.get_width() // 2, screen.get_height() // 2)    # Center the cursor at start
    pygame.mouse.set_visible(False)   # Hide the cursor

    #print(vertices)
    
    # 0 = empty, 1 = wall, 2 = player location, 3 = enemy location
    # Initially all are either 0 or 1 (binary maze)
    archivo = 'Python/labBin.txt'
    atravesar = labBin(archivo)
    
    clouds, costados = load_clouds ()
    #print(clouds)
    
    rotation_angle = 0
    
    # Game loop
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

        # Obtain cursor position
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        camera.rotate(mouse_dx * 0.2, mouse_dy * 0.2)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clears the screen and set up the camera

        camera.update()

        glPushMatrix()
        glRotatef(100, 9, 5, 5)  # Adjust cube rotation
        Cube()
        glPopMatrix()

        obj.render()

        obj.position, c = it_follows_you(camera.pos, obj.position, 15, c, obj)

        # Update rotation of object
        #rotation_angle += 20
        #obj.set_rotation((0, rotation_angle, 0))

        # Draw Axes
        #draw_axes(15.0)
        

        glBindTexture(GL_TEXTURE_2D, cerca) # Bind the 'cerca' texture for use

        glBegin(GL_QUADS)  # Begin drawing quadrilaterals
        for i in range(0, len(gen), 4): # Loop through the vertices of the 'gen' array in steps of 4
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

        glBindTexture(GL_TEXTURE_2D, victory) # Bind the 'victory' texture for use

        glBegin(GL_QUADS) # Begin drawing quadrilaterals
        for i in range(0, len(paredV), 4): # Loop through the vertices of the 'paredV' array in steps of 4
            for j in range(4):# For each set of 4 vertices
                glTexCoord2f(tex_coords[j][0], tex_coords[j][1]) # Specify the texture coordinates for the current vertex
                glVertex3fv(paredV[i + j]) # Specify the position of the current vertex
        glEnd()  # End drawing quadrilaterals
        
        glBindTexture(GL_TEXTURE_2D, tex_clouds)  # Bind the 'tex_clouds' texture for use

        glBegin(GL_QUADS) # Begin drawing quadrilaterals
        for i in range(0, len(clouds), 4):  # Loop through the vertices of the 'clouds' array in steps of 4
            for j in range(4):# For each set of 4 vertices
                glTexCoord2f(tex_coords[j][0], tex_coords[j][1]) # Specify the texture coordinates for the current vertex
                glVertex3fv(clouds[i + j]) # Specify the position of the current vertex
        glEnd() # End drawing quadrilaterals

        glBegin(GL_QUADS) # Begin drawing quadrilaterals
        for i in range(0, len(costados), 4): # Loop through the vertices of the 'costados' array in steps of 4
            for j in range(4): # For each set of 4 vertices
                glTexCoord2f(tex_coords[j][0], tex_coords[j][1]) # Specify the texture coordinates for the current vertex
                glVertex3fv(costados[i + j]) # Specify the position of the current vertex
        glEnd() # End drawing quadrilaterals

        # Renders model
        #obj.render()

        posicion = [0,0,3]
# Check if camera is within a specific range to trigger victory condition
        if (camera.pos[0] > 2 and camera.pos[0] < 3) and (camera.pos[2] > 9):
            #print("victory")
            close_window_and_run_script("Python/victory.py")

        if (round(camera.pos[0]) - camera.pos[0]) > 0: # Check if the camera is on the upper side of the block
            if (round(camera.pos[2]) - camera.pos[2]) > 0:     # Check if the camera is on the left side of the block
                if (round(camera.pos[2])-1) != cam[1]:
                    if ((round(camera.pos[2]) - 1) - cam[1]) < 0:      # Check if the camera has moved to a new block on the left side
                        print("Cambio hacia la izquierda arriba")
                         # Check if the camera can move through
                        #print(f"{(anchoAB[round(camera.pos[0]) - 1])} - {(largoBB[round(camera.pos[2])])}")
                        print((atravesar[(anchoAB[round(camera.pos[0]) - 1])][(largoBB[round(camera.pos[2])])]))
                        if ((atravesar[(anchoAB[round(camera.pos[0]) - 1])][(largoBB[round(camera.pos[2])])]) == "0"):
                            print("pasa")
                            cam[1] = round(camera.pos[2]) - 1
                        else:
                            print("no pasa")
                            camera.pos[0] = posCam[0]
                            camera.pos[2] = posCam[1]
                if (round(camera.pos[0]) - 1) != cam[0]:
                    if ((round(camera.pos[0]) - 1) - cam[0]) < 0:
                        print("Cambio hacia abajo (CAD)")
                        #print(atravesar[(anchoAA[(round(camera.pos[0]))])][(largoAA[round(camera.pos[2]) - 1])])
                        if((atravesar[(anchoAA[(round(camera.pos[0]))])][(largoAA[round(camera.pos[2]) - 1])]) == "0"):
                            print("pasa")
                            cam[0] = round(camera.pos[0]) - 1
                        else:
                            print("no pasa")
                            camera.pos[0] = posCam[0]
                            camera.pos[2] = posCam[1]
            else: #Its on the right side
                if (round(camera.pos[2])) != cam[1]:
                    if ((round(camera.pos[2])) - cam[1]) > 0:
                        print("Cambio hacia la derecha arriba")
                        #print(f"{(anchoAB[round(camera.pos[0]) - 1])} - {(largoBB[round(camera.pos[2])])}")
                        print((atravesar[(anchoAB[round(camera.pos[0]) - 1])][(largoBB[round(camera.pos[2])])]))
                        if ((atravesar[(anchoAB[round(camera.pos[0]) - 1])][(largoBB[round(camera.pos[2])])]) == "0"):
                            print("pasa")
                            cam[1] = round(camera.pos[2])
                            #print(f"{cam[1]} - {round(camera.pos[2]) - 1}")
                        else:
                            print("no pasa")
                            camera.pos[0] = posCam[0]
                            camera.pos[2] = posCam[1]
                if (round(camera.pos[0]) - 1) != cam[0]:
                    if ((round(camera.pos[0]) - 1) - cam[0]) < 0:
                        print("Cambio hacia abajo (CAI)")
                        #print(atravesar[(anchoAA[(round(camera.pos[0]))])][(largoAA[round(camera.pos[2])])])
                        if((atravesar[(anchoAA[(round(camera.pos[0]))])][(largoAA[round(camera.pos[2])])]) == "0"):
                            print("pasa")
                            print(f"A: {cam[0]} - {cam[1]}")
                            cam[0] = round(camera.pos[0]) - 1
                            #cam[1] = round(camera.pos[2]) - 1
                            print(f"B: {cam[0]} - {cam[1]}")
                        else:
                            print("no pasa")
                            camera.pos[0] = posCam[0]
                            camera.pos[2] = posCam[1]
        else: # The camera is on the bottom part of the block
            #print(round(camera.pos[2]) - camera.pos[2])
            if (round(camera.pos[2]) - camera.pos[2]) > 0: #Right side of the block
                if (round(camera.pos[2])-1) != cam[1]:
                    if ((round(camera.pos[2])-1) - cam[1]) < 0:
                        print("Cambio hacia la izquierda abajo")
                        #print(f"{(anchoAB[round(camera.pos[0]) - 1])} - {(largoBB[round(camera.pos[2])])}")
                         # Check if the camera can move through
                        print((atravesar[(anchoAB[round(camera.pos[0])])][(largoBB[round(camera.pos[2])])]))
                        if ((atravesar[(anchoAB[round(camera.pos[0])])][(largoBB[round(camera.pos[2])])]) == "0"):
                            print("pasa")
                            cam[1] = round(camera.pos[2]) - 1
                        else:
                            print("no pasa")
                            camera.pos[0] = posCam[0]
                            camera.pos[2] = posCam[1]
                if (round(camera.pos[0])) != cam[0]:
                    if ((round(camera.pos[0])) - cam[0]) > 0:
                        print("Cambio hacia arriba (CAD)")
                        #print(atravesar[(anchoAA[(round(camera.pos[0]))])][(largoAA[round(camera.pos[2])-1])])
                        if (atravesar[(anchoAA[(round(camera.pos[0]))])][(largoAA[round(camera.pos[2])-1])] == "0"):
                            print("pasa")
                            #print(f"A: {cam[0]} - {cam[1]}")
                            cam[0] = round(camera.pos[0])
                            #cam[1] = round(camera.pos[2])
                            #print(f"B: {cam[0]} - {cam[1]}")
                        else:
                            print("no pasa")
                            camera.pos[0] = posCam[0]
                            camera.pos[2] = posCam[1]
            else:
                if (round(camera.pos[2])) != cam[1]:
                    if ((round(camera.pos[2])) - cam[1]) > 0:
                        print("Cambio hacia la derecha abajo")
                        #print(f"{(anchoAB[round(camera.pos[0]) - 1])} - {(largoBB[round(camera.pos[2])])}")
                        
                        # Check if the camera can move through
                        print((atravesar[(anchoAB[round(camera.pos[0])])][(largoBB[round(camera.pos[2])])]))
                        if ((atravesar[(anchoAB[round(camera.pos[0])])][(largoBB[round(camera.pos[2])])]) == "0"):
                            print("pasa")
                            cam[1] = round(camera.pos[2])
                        else:
                            print("no pasa")
                            camera.pos[0] = posCam[0]
                            camera.pos[2] = posCam[1]
                            # Check if the camera has moved to a new block above
                if (round(camera.pos[0])) != cam[0]:
                    if ((round(camera.pos[0])) - cam[0]) > 0:
                        print("Cambio hacia arriba (CAI)")
                        #print(atravesar[(anchoAA[(round(camera.pos[0]))])][(largoAA[round(camera.pos[2])])])
                         # Check if the camera can move through
                        if (atravesar[(anchoAA[(round(camera.pos[0]))])][(largoAA[round(camera.pos[2])])] == "0"):
                            print("pasa")
                            #print(f"A: {cam[0]} - {cam[1]}")
                            cam[0] = round(camera.pos[0])
                            #cam[1] = round(camera.pos[2])
                            #print(f"B: {cam[0]} - {cam[1]}")
                        else:
                            print("no pasa")
                            camera.pos[0] = posCam[0]
                            camera.pos[2] = posCam[1]
        
        #print(cam)
# Update camera position
        posCam[0] = camera.pos[0]
        posCam[1] = camera.pos[2]
# Constrain camera within defined boundaries
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
# Update the display
        pygame.display.flip()
        clock.tick(60) # Cap the frame rate at 60 FPS

    pygame.mouse.set_visible(True)  # show cursor at exit
    pygame.quit()
if  __name__== "__main__":
    main()
    