import pygame
import sys
import subprocess
from button import Button
from music_manager import music_manager  # Importar el MusicManager

pygame.init()

# Configuración de la pantalla
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

# Cargar y ajustar el fondo
BG = pygame.image.load("Python/pictures/cadejo1.jpg")
BG = pygame.transform.scale(BG, (1280, 720))

# Iniciar la música solo una vez
music_manager.start_music()

def get_font(size):
    """Devuelve la fuente deseada en el tamaño especificado."""
    return pygame.font.Font("Python/pictures/enervate.ttf", size)

def close_window_and_run_script(script_path):
    """Cierra la ventana y ejecuta el script especificado."""
    pygame.quit()
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")
    sys.exit()

def play():
    """Función para la pantalla de 'Play'."""
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("You gonna enter to the RUN! game.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_ENTER = Button(image=None, pos=(640, 460), 
                            text_input="Start", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_ENTER.changeColor(PLAY_MOUSE_POS)
        PLAY_ENTER.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                music_manager.stop_music()  # Detener la música antes de salir
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_ENTER.checkForInput(PLAY_MOUSE_POS):
                    close_window_and_run_script("Python/main.py")

        pygame.display.update()

def options():
    """Función para la pantalla de 'Options'."""
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS for the music.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_ENTER = Button(image=None, pos=(640, 460), 
                            text_input="Enter", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_ENTER.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_ENTER.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                music_manager.stop_music()  # Detener la música antes de salir
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_ENTER.checkForInput(OPTIONS_MOUSE_POS):
                    close_window_and_run_script("Python/music.py")

        pygame.display.update()

def main_menu():
    """Función para el menú principal."""
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Python/pictures/fondo.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Python/pictures/fondo.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")
        QUIT_BUTTON = Button(image=pygame.image.load("Python/pictures/fondo.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                music_manager.stop_music()  # Detener la música antes de salir
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    music_manager.stop_music()  # Detener la música antes de salir
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
