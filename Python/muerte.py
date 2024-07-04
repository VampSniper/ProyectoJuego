import pygame
import sys
import subprocess
from button import Button # Import Button class from button.py file
from music_manager import music_manager  # Import MusicManager instance from music_manager.py

pygame.init()

# Screen configuration
SCREEN = pygame.display.set_mode((1280, 720))  # Set screen size
pygame.display.set_caption("Menu") # Set window title

# Load and scale the background image
BG = pygame.image.load("Python/pictures/fondoBlanco.jfif")
BG = pygame.transform.scale(BG, (1280, 720))

# Start playing music
music_manager.start_music()

def get_font(size):
    """Returns the desired font at the specified size."""
    return pygame.font.Font("Python/pictures/enervate.ttf", size)

def close_window_and_run_script(script_path):
    """Close the window and execute the specified script."""
    pygame.quit()
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")
    sys.exit()

def play():
    """Function for the 'Play' screen."""
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos() # Get current mouse position

        SCREEN.fill("black") # Fill the screen with black color
# Render text for acknowledgments
        PLAY_TEXT = get_font(45).render("Agradecimientos para los estudiantes 3T3.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260)) # Position text in the center
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)  # Draw text on the screen
 # Create 'Return' button
        PLAY_ENTER = Button(image=None, pos=(640, 460), 
                            text_input="Volver", font=get_font(75), base_color="White", hovering_color="Green")
        
        PLAY_SALIR = Button(image=None, pos=(640, 660), 
                            text_input="Salir", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_ENTER.changeColor(PLAY_MOUSE_POS) # Change button color on hover
        PLAY_ENTER.update(SCREEN)  # Update button appearance on screen
# Create 'Exit' button
        PLAY_SALIR.changeColor(PLAY_MOUSE_POS)  # Change button color on hover
        PLAY_SALIR.update(SCREEN) # Update button appearance on screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                music_manager.stop_music()   # Stop music before quitting
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_ENTER.checkForInput(PLAY_MOUSE_POS):
                    close_window_and_run_script("Python/menu.py")  # Run menu script on button click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_SALIR.checkForInput(PLAY_MOUSE_POS):
                    pygame.quit()
                    sys.exit()     # Quit pygame and exit program

        pygame.display.update()  # Update the display


def main_menu():
    """Function for the main menu."""
    while True:
        SCREEN.blit(BG, (0, 0)) # Draw background image on screen

        MENU_MOUSE_POS = pygame.mouse.get_pos() # Get current mouse position
# Render main menu text
        MENU_TEXT = get_font(85).render("DERROTA, VUELVELO A INTENTAR SI QUIERES GANAR", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))  # Position text in the center of the screen
# Create 'PLAY' button
        PLAY_BUTTON = Button(image=pygame.image.load("Python/pictures/fondo.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")

        # Create 'QUIT' button
        QUIT_BUTTON = Button(image=pygame.image.load("Python/pictures/fondo.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")

        SCREEN.blit(MENU_TEXT, MENU_RECT) # Draw text on the screen

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS) # Change button color on hover
            button.update(SCREEN) # Update button appearance on screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                music_manager.stop_music() # Stop music before quitting
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play() # Switch to 'Play' screen on button click
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    music_manager.stop_music()  # Stop music before quitting
                    pygame.quit()
                    sys.exit()

        pygame.display.update() # Update the display

main_menu() #  Run the main menu function
