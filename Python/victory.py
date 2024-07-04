import pygame
import sys
import subprocess
from button import Button
from music_manager import music_manager  # Import the MusicManager

pygame.init()

# Screen configuration
SCREEN = pygame.display.set_mode((1280, 720)) # Set screen resolution
pygame.display.set_caption("Menu") # Set window title

# Load and adjust the background
BG = pygame.image.load("Python/pictures/fondoBlanco.jfif") # Load background image
BG = pygame.transform.scale(BG, (1280, 720)) # Scale background image to screen size

# Start the music only once
music_manager.start_music()

def get_font(size):
    """Returns the desired font in the specified size."""
    return pygame.font.Font("Python/pictures/enervate.ttf", size)  # Load custom font

def close_window_and_run_script(script_path):
    """Close the window and run the specified script."""
    pygame.quit()  # Quit pygame
    try:
        subprocess.run([sys.executable, script_path], check=True)  # Run script externally
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}") # Print error if script fails to run
    sys.exit() # Exit the program

def play():
    """Function for the 'Play' screen."""
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos() # Get mouse position

        SCREEN.fill("black") # Fill screen with black color

        PLAY_TEXT = get_font(45).render("Agradecimientos para los estudiantes 3T3.", True, "White")  # Render text
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))  # Position text
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)  # Display text on screen
        # Create 'Back' button

        PLAY_ENTER = Button(image=None, pos=(640, 460), 
                            text_input="Volver", font=get_font(75), base_color="White", hovering_color="Green")
        # Create 'Quit' button
        PLAY_SALIR = Button(image=None, pos=(640, 660), 
                            text_input="Salir", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_ENTER.changeColor(PLAY_MOUSE_POS)  # Change color of 'Back' button on hover
        PLAY_ENTER.update(SCREEN) # Update 'Back' button appearance on screen

        PLAY_SALIR.changeColor(PLAY_MOUSE_POS) # Change color of 'Quit' button on hover
        PLAY_SALIR.update(SCREEN) # Update 'Quit' button appearance on screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                music_manager.stop_music()  # Stop music before quitting
                pygame.quit()  # Quit pygame
                sys.exit() # Exit the program
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_ENTER.checkForInput(PLAY_MOUSE_POS):
                    close_window_and_run_script("Python/menu.py") # Run menu script on 'Back' button click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_SALIR.checkForInput(PLAY_MOUSE_POS):
                    pygame.quit() # Quit pygame
                    sys.exit()    # Exit the program

        pygame.display.update() # Update the display


def main_menu():
    """Function for the main menu"""
    while True:
        SCREEN.blit(BG, (0, 0)) # Display background image

        MENU_MOUSE_POS = pygame.mouse.get_pos() # Get mouse position

        MENU_TEXT = get_font(85).render("VICTORY, YOU ARE THE BEST", True, "#b68f40")   # Render menu text
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100)) # Position menu text
  # Create 'PLAY' button
        PLAY_BUTTON = Button(image=pygame.image.load("Python/pictures/fondo.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")
 # Create 'QUIT' button
        QUIT_BUTTON = Button(image=pygame.image.load("Python/pictures/fondo.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")

        SCREEN.blit(MENU_TEXT, MENU_RECT) # Display menu text on screen

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)  # Change button color on hover
            button.update(SCREEN) # Update button appearance on screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                music_manager.stop_music()   # Stop music before quitting
                pygame.quit() # Quit pygame
                sys.exit() # Exit the program
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()  # Switch to 'Play' screen on 'PLAY' button click
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    music_manager.stop_music()   # Stop music before quitting
                    pygame.quit() # Quit pygame
                    sys.exit()  # Exit the program

        pygame.display.update()  # Update the display

main_menu() # Run the main menu function
