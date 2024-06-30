from tkinter import Button, Label, Tk, ttk, Frame, PhotoImage
import pygame
import random
import mutagen
import subprocess
import sys
from music_manager import music_manager  # Import music_manager

#def return to menu, cause we need to return to the menu.py if we need to play the game or quit the menu
def return_to_menu():
    ventana.destroy()
    try:
        subprocess.run([sys.executable, "Python/menu.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running menu.py: {e}")

lista = [i for i in range(50, 200, 10)]

#def the iniciar repruduccion, It is responsible for the animation that occurs when the .mp3 song starts.
def iniciar_reproduccion():
    global actualizar
    barra1['value'] = random.choice(lista)
    barra2['value'] = random.choice(lista)
    # (Repetir esto para las demás barras)

    time = pygame.mixer.music.get_pos()
    x = int(int(time) * 0.001)
    tiempo['value'] = x  # posición de la canción

    y = float(int(volumen.get()) * 0.1)
    music_manager.set_volume(y)  # Ajustar el volumen
    nivel['text'] = int(y * 100)

    audio = mutagen.File(music_manager.track_path)    
    log = audio.info.length
    minutos, segundos = divmod(log, 60)
    minutos, segundos = int(minutos), int(segundos)
    tt = minutos * 60 + segundos
    tiempo['maximum'] = tt  # tiempo total de la canción
    texto['text'] = f"{minutos}:{segundos:02d}"

    actualizar = ventana.after(100, iniciar_reproduccion)

    if x == tt:
        ventana.after_cancel(actualizar)
        texto['text'] = "00:00"
        detener_efecto()
        pygame.mixer.music.play()
        ventana.after(100, iniciar_reproduccion)

#start the music .mp3
def iniciar():
    music_manager.start_music()
    music_manager.set_volume(1.0)
    iniciar_reproduccion()

#go back the music
def retroceder():
    global pos,n
    if pos >0:
        pos = pos-1
    else:
         pos = 0
    cantidad['text'] = str(pos)+'/'+str(n)

#go to the next song, for the moment we use only one for the rest of the game, maybe we gonna put more
def adelantar():
	global pos, n

	if pos == n-1:
		pos = 0
	else:
		pos = pos + 1
	cantidad['text'] = str(pos)+'/'+str(n)

#is responsible for stopping the effects of the bars that are displayed
def detener_efecto():
	barra1['value'] = 50
	barra2['value'] = 60
	barra3['value'] = 70
	barra4['value'] = 80
	barra5['value'] = 90
	barra6['value'] = 100
	barra7['value'] = 90
	barra8['value'] = 80
	barra9['value'] = 70
	barra10['value'] = 60
	barra11['value'] = 60
	barra12['value'] = 70
	barra13['value'] = 80
	barra14['value'] = 90
	barra15['value'] = 100
	barra16['value'] = 90
	barra17['value'] = 80
	barra18['value'] = 70
	barra19['value'] = 60
	barra20['value'] = 50

#stop the song
def stop():
    music_manager.stop_music()
    ventana.after_cancel(actualizar)
    detener_efecto()
#pause the song
def pausa():
    pygame.mixer.music.pause()
    ventana.after_cancel(actualizar)
    detener_efecto()
#continue the song
def continuar():
    pygame.mixer.music.unpause()
    ventana.after(100, iniciar_reproduccion)
#The configuration is made of what it will say at the top of the window, 
#and the images that are the icons are also included.
ventana = Tk()
ventana.title('Configuración de Música')
ventana.iconbitmap('Python/pictures/icono.ico')
ventana.config(bg='black')
ventana.resizable(0, 0)

estilo = ttk.Style()
estilo.theme_use('clam')
estilo.configure("Vertical.TProgressbar", foreground='green2', background='green2', troughcolor='black',
                 bordercolor='black', lightcolor='green2', darkcolor='green2')

frame1 = Frame(ventana, bg='black', width=600, height=350)
frame1.grid(column=0, row=0, sticky='nsew')
frame2 = Frame(ventana, bg='black', width=600, height=50)
frame2.grid(column=0, row=1, sticky='nsew')

# Create vertical progress bars
barras = []
for i in range(20):
    barra = ttk.Progressbar(frame1, orient='vertical', length=300, maximum=300, style="Vertical.TProgressbar")
    barra.grid(column=i, row=0, padx=1)
    barras.append(barra)
    
(barra1, barra2, barra3, barra4, barra5, barra6, barra7, barra8, barra9, barra10,
 barra11, barra12, barra13, barra14, barra15, barra16, barra17, barra18, barra19, barra20) = barras

estilo1 = ttk.Style()
estilo1.theme_use('clam')
estilo1.configure("Horizontal.TProgressbar", foreground='red', background='black', troughcolor='DarkOrchid1',
                  bordercolor='#970BD9', lightcolor='#970BD9', darkcolor='black')

tiempo = ttk.Progressbar(frame2, orient='horizontal', length=390, mode='determinate', style="Horizontal.TProgressbar")
tiempo.grid(row=0, columnspan=8, padx=5)
texto = Label(frame2, bg='black', fg='green2', width=5)
texto.grid(row=0, column=8)

nombre = Label(frame2, bg='black', fg='red', width=55)
nombre.grid(column=0, row=1, columnspan=8, padx=5)
cantidad = Label(frame2, bg='black', fg='green2')
cantidad.grid(column=8, row=1)

imagen2 = PhotoImage(file='Python/pictures/play.png')
imagen3 = PhotoImage(file='Python/pictures/pausa.png')
imagen4 = PhotoImage(file='Python/pictures/repetir.png')
imagen5 = PhotoImage(file='Python/pictures/stop.png')
imagen6 = PhotoImage(file='Python/pictures/anterior.png')
imagen7 = PhotoImage(file='Python/pictures/adelante.png')

boton2 = Button(frame2, image=imagen2, bg='yellow', command=iniciar)
boton2.grid(column=1, row=2, pady=10)
boton3 = Button(frame2, image=imagen3, bg='red', command=stop)
boton3.grid(column=2, row=2, pady=10)
boton4 = Button(frame2, image=imagen4, bg='blue', command=pausa)
boton4.grid(column=3, row=2, pady=10)
boton5 = Button(frame2, image=imagen5, bg='green2', command=continuar)
boton5.grid(column=4, row=2, pady=10)
atras = Button(frame2, image=imagen6, bg='orange', command=retroceder)
atras.grid(column=5, row=2, pady=10)
adelante = Button(frame2, image=imagen7, bg='green', command=adelantar)
adelante.grid(column=6, row=2, pady=10)
return_button = Button(frame2, text="Return", command=return_to_menu, bg='blue', fg='white')
return_button.grid(column=7, row=3, pady=10)

volumen = ttk.Scale(frame2, to=10, from_=0, orient='horizontal', length=90, style='Horizontal.TScale')
volumen.grid(column=7, row=2)

style = ttk.Style()
style.configure("Horizontal.TScale", bordercolor='green2', troughcolor='black', background='green2',
                foreground='green2', lightcolor='green2', darkcolor='black')

nivel = Label(frame2, bg='black', fg='green2', width=3)
nivel.grid(column=8, row=2)

# Call the `start()` function at startup
iniciar()

ventana.mainloop()
