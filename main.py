import math
import pygame as pg
import pygame.gfxdraw
import sys
import os
import subprocess

# Specifica il percorso della cartella
percorso_cartella = "./images"
# Ottieni la lista di tutti i file nella cartella
elenco_files = os.listdir(percorso_cartella)
# Filtra solo i file con estensione .png o .jpg
files_immagini = [file for file in elenco_files if file.lower().endswith((".png", ".jpg"))]

# Inizializza pg
pg.init()
# Ottieni le informazioni sul display
display_info = pg.display.Info()
# Creazione della finestra
screen = pg.display.set_mode((800, 600), pg.RESIZABLE)
pg.display.set_caption("Ruota della fortuna")
sfondo_colore = (255, 255, 255)

# Dimensioni e testo bottone
bottone_w, bottone_h = 100, 50
testo_bottone = "Ruota!"
font = pygame.font.SysFont(None, 30)

# Cerchio
raggio = 200
num_spicchi = len(files_immagini)
angolo_spicchio = (int) (360 / num_spicchi)

# Colori spicchi
colors = [
    (255, 0, 0),    # Rosso
    (0, 255, 0),    # Verde
    (0, 0, 255),    # Blu
    (255, 255, 0),  # Giallo
    (0, 255, 255),  # Azzurro
    (255, 0, 255),  # Magenta
    (128, 128, 128),  # Grigio
    (255, 128, 0),  # Arancione
    (0, 128, 255),  # Blu scuro
    (128, 0, 255),  # Viola
    (255, 128, 128),  # Rosa
    (128, 255, 0),  # Lime
    (128, 0, 0),    # Marrone
    (0, 128, 0),    # Verde scuro
    (0, 0, 128),    # Blu scuro
    (192, 192, 192),  # Argento
    (255, 255, 255),  # Bianco
    (0, 0, 0),    # Nero
    (255, 192, 203),  # Rosa chiaro
    (0, 255, 128),   # Verde chiaro
]

# Variabile per tracciare lo stato del mouse
mouse_premuto = False

# Variabili per la rotazione
angolo_rotazione = 1
velocita_rotazione = 0.0
smorzamento = 1.0

# Array per salvare i poligoni
vertici = []
#distanza = 0
open = False

# Carica l'immagine del triangolo
triangolo_img = pg.image.load("triangolo.png")
# Definisci le dimensioni desiderate per il triangolo
nuova_larghezza = 30
nuova_altezza = 50
# Ridimensiona l'immagine del triangolo
triangolo_img = pg.transform.scale(triangolo_img, (nuova_larghezza, nuova_altezza))

# Ciclo principale
while True:
    # Ottieni lo stato dei pulsanti del mouse
    mouse_button = pg.mouse.get_pressed()[0]

    # Per chiudere la finestra con escape
    for event in pg.event.get():
        # Chiude la finestra se viene premuto il pulsante di chiusura
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        # Chiude la finestra se viene premuto il tasto ESC
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
        # Verifica se il click è avvenuto all'interno di uno spicchio
        # calcolando la distanza tra il mouse e il vertice dello spicchio
        # diventerà deprecato appena il cazzo di triangolo funzionerà
        '''
        elif mouse_button:
            mouse_pos = pg.mouse.get_pos()
            for i, vertice in enumerate(vertici):
                _distanza = math.sqrt((vertice[0] - mouse_pos[0])**2 + (vertice[1] - mouse_pos[1])**2)
                if _distanza < distanza:
                     path = os.path.join(percorso_cartella, files_immagini[i])
                    subprocess.run(['start', os.path.abspath(path)], shell=True)
                    break
        '''

    if open and velocita_rotazione == 0.0:
        min_dist = sys.maxsize
        file_to_open = -1
        for i, vertice in enumerate(vertici):
            # per qualche oscura ragione qui ha i valori sbagiati di vertice[0] e vertice[1]
            _distanza = math.sqrt((triangolo_rect[0]-vertice[0])**2 + (triangolo_rect[1]-vertice[1])**2)
            if _distanza < min_dist:
                min_dist = _distanza
                file_to_open = i
        #print(f"File da aprire: {file_to_open}")
        path = os.path.join(percorso_cartella, files_immagini[file_to_open])
        subprocess.run(['start', os.path.abspath(path)], shell=True)
        open = False

    # Aggiorna posizioni relative alla dimensione della finestra
    w_width, w_height = pg.display.get_surface().get_size()
    bottone_x, bottone_y = (w_width // 2) - (bottone_w / 2), (w_height - 70)
    centro = (w_width//2, w_height//2)

    # Per far ruotare la ruota
    angolo_rotazione += velocita_rotazione
    velocita_rotazione *= smorzamento

    # Controlla la pressione del pulsante del mouse
    mouse_pos = pg.mouse.get_pos()
    bottone_rect = pg.Rect(bottone_x, bottone_y, bottone_w, bottone_h)

    # Pulisce la schermata
    screen.fill(sfondo_colore)

    if mouse_button and not mouse_premuto and bottone_rect.collidepoint(mouse_pos):
        if velocita_rotazione == 0.0:
            velocita_rotazione = 50.0
            smorzamento = 1.0
            testo_bottone = "Ferma!"
        else:
            smorzamento = 0.99
            testo_bottone = "Ruota!"
            open = True
        mouse_premuto = True
    elif not mouse_button:
        mouse_premuto = False
    
    vertici.clear()

    for i in range(num_spicchi):
        # Calcola gli angoli iniziale e finale per ciascuno spicchio
        start_angle = i * angolo_spicchio + angolo_rotazione
        end_angle = (i + 1) * angolo_spicchio + angolo_rotazione

        # Calcola i vertici approssimati del poligono rappresentante l'intero spicchio
        vertici_spicchio = [
            centro,
            (
                centro[0] + raggio * math.cos(math.radians(start_angle)),
                centro[1] + raggio * math.sin(math.radians(start_angle)),
            ),
            (
                centro[0] + raggio * math.cos(math.radians((start_angle + end_angle) / 2)),
                centro[1] + raggio * math.sin(math.radians((start_angle + end_angle) / 2)),
            ),
            (
                centro[0] + raggio * math.cos(math.radians(end_angle)),
                centro[1] + raggio * math.sin(math.radians(end_angle)),
            ),
        ]

        # Disegna il poligono approssimato rappresentante l'intero spicchio
        pg.draw.polygon(screen, colors[i%len(colors)], vertici_spicchio)
        vertici.append(vertici_spicchio[2])

        # Calcola solo la prima volta il raggio del cerchio per il click e la posizione del triangolo
        #if distanza == 0:
        #    distanza = math.sqrt((vertici_spicchio[2][0] - vertici_spicchio[3][0])**2 + (vertici_spicchio[2][1] - vertici_spicchio[3][1])**2)

        # Calcola il centro dell'angolo dello spicchio
        angolo_centrale = (i + 0.5) * angolo_spicchio
        centro_angolo = (
            centro[0] + raggio * 0.85 * pg.math.Vector2(1, 0).rotate(angolo_centrale + angolo_rotazione)[0],
            centro[1] + raggio * 0.85 * pg.math.Vector2(1, 0).rotate(angolo_centrale + angolo_rotazione)[1],
        )

        # Disegna il testo al centro dello spicchio
        testo = font.render(str(i), True, (0, 0, 0))
        text_rect = testo.get_rect(center=centro_angolo)
        screen.blit(testo, text_rect)
        triangolo_rect = triangolo_img.get_rect(center=(vertici_spicchio[0][0], vertici_spicchio[0][1]-raggio)) 
        screen.blit(triangolo_img, triangolo_rect)

    # Disegna il bottone
    pg.draw.rect(screen, (0,0,0), bottone_rect)
    testo_renderizzato = font.render(testo_bottone, True, (255, 255, 255))
    testo_rect = testo_renderizzato.get_rect(center=bottone_rect.center)
    screen.blit(testo_renderizzato, testo_rect)

    if abs(velocita_rotazione) < 0.01:
        velocita_rotazione = 0.0

    # Aggiorna la schermata
    pg.display.flip()