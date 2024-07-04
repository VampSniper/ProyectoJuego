import pygame
import sys
import subprocess
from button import Button
from music_manager import music_manager  # Imports MusicManager

pygame.init()

# Screen configuration
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

# Load and scale the background image
BG = pygame.image.load("Python/pictures/cadejo1.jpg")
BG = pygame.transform.scale(BG, (1280, 720))

# Start the music once
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
# Fill the screen with black color
        SCREEN.fill("black")
# Render the play screen text
        PLAY_TEXT = get_font(45).render("You gonna enter to the RUN! game.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
   # Create the 'Start' button
        PLAY_ENTER = Button(image=None, pos=(640, 460), 
                            text_input="Start", font=get_font(75), base_color="White", hovering_color="Green")
 # Change the button color on hover and update it on the screen
        PLAY_ENTER.changeColor(PLAY_MOUSE_POS)
        PLAY_ENTER.update(SCREEN)
# Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                music_manager.stop_music()   # Stop the music before quitting
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_ENTER.checkForInput(PLAY_MOUSE_POS):
                    close_window_and_run_script("Python/main.py")

        pygame.display.update()  # Update the display

def options():
    """Función para la pantalla de 'Options'."""
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
# Fill the screen with white color
        SCREEN.fill("white")
# Render the options screen text
        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS for the music.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
# Create the 'Enter' button
        OPTIONS_ENTER = Button(image=None, pos=(640, 460), 
                            text_input="Enter", font=get_font(75), base_color="Black", hovering_color="Green")
# Change the button color on hover and update it on the screen
        OPTIONS_ENTER.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_ENTER.update(SCREEN)
# Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                music_manager.stop_music()   # Stop the music before quitting
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_ENTER.checkForInput(OPTIONS_MOUSE_POS):
                    close_window_and_run_script("Python/music.py")
 # Update the display
        pygame.display.update()

def main_menu():
    """Función para el menú principal."""
    while True:
        SCREEN.blit(BG, (0, 0)) # Blit the background image to the screen

        MENU_MOUSE_POS = pygame.mouse.get_pos()
# Render the main menu text
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
 # Create buttons for Play, Options, and Quit
        PLAY_BUTTON = Button(image=pygame.image.load("Python/pictures/fondo.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Python/pictures/fondo.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")
        QUIT_BUTTON = Button(image=pygame.image.load("Python/pictures/fondo.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")

        SCREEN.blit(MENU_TEXT, MENU_RECT)  # Blit the main menu text to the screen
 # Change button colors on hover and update them on the screen
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
 # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                music_manager.stop_music()  # Stop the music before quitting
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    music_manager.stop_music()  # Stop the music before quitting
                    pygame.quit()
                    sys.exit()

        pygame.display.update()  # Update the display

main_menu() # Run the main menu function
