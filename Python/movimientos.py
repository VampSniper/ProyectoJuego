# movimientos.py

import pygame

def handle_events(camera):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera.move('forward', 0.025)
    if keys[pygame.K_s]:
        camera.move('backward', 0.025)
    if keys[pygame.K_a]:
        camera.move('left', 0.025)
    if keys[pygame.K_d]:
        camera.move('right', 0.025)
    #if keys[pygame.K_SPACE]:
    #    camera.move('up', 0.1)
    #if keys[pygame.K_LSHIFT]:
    #    camera.move('down', 0.1)

def handle_mouse(camera, event):
    if event.type == pygame.MOUSEMOTION:
        dx, dy = event.rel
        camera.rotate(dx * 0.2, dy * 0.2)

def hide_cursor():
    pygame.mouse.set_visible(False)

def show_cursor():
    pygame.mouse.set_visible(True)
