import pygame
from pygame.locals import *
from random import *
import pyautogui # --> Nécessaire pour le click automatique de la fonction bot()


#Pour éviter que le son soit décalé par rapport au moment où on clique sur la tuile
pygame.mixer.pre_init(44100, -16, 2, 2048)  #--> pre_init(frequency=22050, size=-16, channels=2, buffersize=4096)
pygame.init()


largeur_fen = 400
longueur_fen = 600
# ---> Largeur et hauteur de la fenêtre

largeur_note = largeur_fen //4
longueur_note = longueur_fen//4
# ---> Largeur et hauteur des tuiles


# Images de fonds pour le menu et le game over
background0 = pygame.image.load("background0.jpg")
background1 = pygame.image.load("background1.jpg")

#https://cdn.pixabay.com/photo/2016/10/10/12/54/space-1728314_960_720.jpg : Background1 du gameover
#https://cdn.pixabay.com/photo/2017/01/27/19/08/soap-bubbles-2013992_960_720.jpg : Background0 du menu


#Couleurs
white = (255,255,255)
black = (0,0,0)
red = (210, 0, 0)
green = (0,179,0)
blue = (0,110,255)
bright_blue = (0,153,250)
bright_red = (230,25,50)
bright_green = (0,220,0)
grey = (125, 125,125)


fps = 60
vitesse = 2
score=0
fps_clock = pygame.time.Clock()
# --> gère le nombre d'images par seconde en créant un type object


affi_surface = pygame.display.set_mode((largeur_fen, longueur_fen))
#--> Initialise une fenêtre (écran) à afficher. pygame.display.set_mode(largeur,hauteur)
pygame.display.set_caption("Piano Tiles !") # Nom de la fenêtre


tile_sound = pygame.mixer.Sound("piano.wav")
lose_sound = pygame.mixer.Sound("fail.wav")
# --> Crée un nouveau type object son depuis un fichier

#Génère aléatoirement la position des touches
def positionAleatoire() :
    global position
    random = randint (0,3)
    valeurs = [0,largeur_note,largeur_fen//2,3*largeur_note]
    position = valeurs [random ]
    return position


#Génère les tuiles en utilisant positionAleatoire()
def initialise_jeu():
    global Notes
    global h
    h = 0
    Notes = []
    old_pos = -42
    for i in range(1000):
       h = h +  longueur_note
       pos = positionAleatoire()
       while pos == old_pos:
            pos = positionAleatoire()
       Notes.append([pos, -h, False])
       old_pos = pos


#Dessine les tuiles (rectangles)
def displayNotePiano(note):
    global rect_note
    rect_note = pygame.Rect(note[0], note[1], largeur_note, longueur_note)
    pygame.draw.rect(affi_surface, black, rect_note)



def displayNotesPiano():
    for note in Notes:
        displayNotePiano(note)


#Fait défiler les tuiles de haut en bas
def decaleNotesPiano():
    for note in Notes:
        if note[1]+ longueur_note + vitesse > longueur_fen :
            perdu()
        note[1] = note[1]+vitesse


# Permet de faire déplace automatiquement le curseur de la souris sur les tuiles et de cliquer automatiquement
def bot():
    for note in Notes:
       if note[1] > longueur_note // 4 :
               clic_x = note[0] + largeur_note//2
               clic_y = note[1] + longueur_note//2
               pygame.mouse.set_pos(clic_x, clic_y)
               pyautogui.click () # --> Clique gauche automatique de la souris


# Teste si le clique a touché une des tiles + augmentation de vitesse
def testClic (x,y) :
    global score
    global vitesse
    noteCliquee = False
    for note in Notes:
        if (x >= note[0]) and (x <= note[0] + largeur_note):
            if y >= note[1] and y <= (note[1] + longueur_note):
                score = score + 1
                vitesse = vitesse + 0.25
                Notes.remove(note)
                pygame.mixer.Sound.play(tile_sound)  # --> Joue le son do
                noteCliquee = True
    return noteCliquee


#Récupère la position lorsque la souris clique
def recupClic () :
    position = pygame.mouse.get_pos()
    return position



def quadrillage():
        #lignes horizontales
        horiz_line_up = [(0,longueur_note),(largeur_fen,longueur_note)]
        pygame.draw.lines(affi_surface,black,True,horiz_line_up)

        horiz_line_middle = [(0,longueur_fen//2),(largeur_fen,longueur_fen//2)]
        pygame.draw.lines(affi_surface,black,True,horiz_line_middle)

        horiz_line_bottom = [(0,3*longueur_note),(largeur_fen,3*longueur_note)]
        pygame.draw.lines(affi_surface,black,True,horiz_line_bottom)

        #ligne verticales
        verti_line_left = [(largeur_note,0),(largeur_note,longueur_fen)]
        pygame.draw.lines(affi_surface,black,True,verti_line_left)

        verti_line_middle = [(largeur_fen//2,0),(largeur_fen//2,longueur_fen)]
        pygame.draw.lines(affi_surface,black,True,verti_line_middle)

        verti_line_right = [(3*largeur_note,0),(3*largeur_note,longueur_fen)]
        pygame.draw.lines(affi_surface,black,True,verti_line_right)


# Utlisé pour générer le texte
def texteJeu(text,font,color):
    textSurface = font.render(text, True, color)  # --> Type object pour un texte (texte à afficher, anti-aliasing (moins pixellisé), couleur )
    return textSurface, textSurface.get_rect()



# Fonction pour générer des boutons interactics avec la souris, est mis en surbrillance lorsque la souris passe dessus
def button(msg,x,y,w,h,ic,ac,action): #--> fonction button (Message à afficher, coordonnées x et y, largeur w et longueur x, couleur normale, couleur de surbrillance, fonction à appeler)
    global mouse
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(affi_surface, ac,(x,y,w,h))

        if click[0] == 1:
            action()
    else:
        pygame.draw.rect(affi_surface,ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",30)
    text_surface, text_rectangle = texteJeu(msg, smallText, black)
    text_rectangle.center = ( (x+(w/2)), (y+(h/2)) )
    affi_surface.blit(text_surface, text_rectangle)
    
    
# Permet d'afficher du texte   
def message (x,y , texte, taille):
        largeText = pygame.font.SysFont("freesansbold.ttf",taille)
        text_surface, text_rectangle = texteJeu(texte, largeText, black)
        text_rectangle.center = (x,y)
        affi_surface.blit(text_surface, text_rectangle)  #--> blit(source, dest, area=None, special_flags = 0) -> Rect
    


# Fonction qui génère le menu. Le menu est codé comme un "jeu" à part entière.
def menuJeu():
    menu = True
    pygame.mixer.music.load('entertainer.mp3')
    # --> joue la musique en chargeant le fichier mp3
    pygame.mixer.music.play(-1)
    # --> play (5) jouera la musique 5 fois, play(-1) la joue indéfiniment.

    while menu:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

        affi_surface.blit(background0, [0, 0])  # Permet d'afficher un fond d'image sur l'écran
        message (largeur_fen//2, 90, "Piano Tiles!", 80)

        button("Jouer",34,460,125,75,blue,bright_blue, bouclejeu)
        button("Quitter",230,460,125,75,red,bright_red, pygame.quit)
        button("Bot",312,124,70,50,green,bright_green, boucleBot)


        pygame.display.update()


#Affiche l'écran de Game Over
def perdu():
    global score
    global vitesse

    pygame.mixer.Sound.play(lose_sound)

    affi_surface.blit(background1, [0, 0])
    message (largeur_fen//2, longueur_fen//2, "Game Over", 70)
    affi_score(score,135,340,white,50)

    pygame.display.update()

    pygame.time.wait(2000)   #Met un temps d'attente en millisecondes

    score=0
    vitesse= 2

    menuJeu()


#Permet d'afficher le score
def affi_score(count,x,y,color,width): #affi_score(corordonnées x et y, couleur, largeur du texte)
    font = pygame.font.Font(None, width)
    text = font.render("Score: "+str(count), True, color)
    affi_surface.blit(text,(x,y))


# Permet d'afficher l'interface du jeu, en appelant les fonctions liées à l'affichage du score en haut à droite, à l'affichage des tuiles et le quadrillage
def display():
    global score
    affi_surface.fill(white)
    quadrillage()
    displayNotesPiano()
    affi_score(score,0,0,grey,30)


# Fonction principale du jeu
def bouclejeu():
    pygame.mixer.music.stop()
    initialise_jeu()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicPos = recupClic()
                if testClic(clicPos[0],clicPos[1]) == False :
                    perdu()
        decaleNotesPiano()
        display()
        pygame.display.update()
        fps_clock.tick(fps)


# Fonction principale du jeu + fonction bot()
def boucleBot():
    pygame.mixer.music.stop()
    initialise_jeu()
    while True:
        bot()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicPos = recupClic()
                if testClic(clicPos[0],clicPos[1]) == False:
                    perdu()
        decaleNotesPiano()
        display()
        pygame.display.update()
        fps_clock.tick(fps)




menuJeu()
