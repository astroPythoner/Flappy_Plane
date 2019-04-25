import pygame
from os import path, listdir

# Bildschrimgröße
WIDTH = 480 * 2
HEIGHT = 320 * 2
FPS = 60

# Pygame initialisieren und Fenster aufmachen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy!")
clock = pygame.time.Clock()

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.7

# Konstanten für Art des Spielendes und die Tastenarten
BEFORE_FIRST_GAME = "before first game"  # Beim Start drücken vor dem ersten Spiel
START_GAME = "start"  # Vor jedem Spiel um de Funktion new() in der Spielklasse aufzurufen
COUNTDOWN = "countdown"  # Countdown in den ersten drei Sekunden des Spiels
NEXT_GAME = "next game"  # Level geschafft
VERLOREN = "verloren"  # Gestorben

# Rochs hängen von oben oder unten
FROM_TOP = "from top"
FROM_BUTTON = "from button"

# Verschiedene Möglochkeiten, die Steine zu positionieren
TUNNEL = "tunnel"
VERSETZT = "versetzt"
GEGENUEBER = "gegenüber"
KURVE = "kurve"
ZENTRAL = "zentral"
FALLEND = "fallend"

# Power-Ups
STAR = "star"
MEDAL = "medal"

# Tasten
JUMP = "jump"
UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"
ESC = "escape"
ALL = "all"
START = "start"
XY = "xy"
X = "x"
AB = "ab"
B = "b"

# Standartfarben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_YELLOW = (235,185,0)
TEXT_RED = (255, 65, 0)
TEXT_GREEN = (120,170,70)
TEXT_COLOR = (70,70,110)

# finde passendste Schriftart zu arial.
font_name = pygame.font.match_font('arial')

# Lautstärke
game_music_volume = 0.8
game_sound_volume = 0.75

def load_graphics_from_file_array(file_array, dir, color_key=None, convert_aplha=False, as_dict=False):
    # Lädt alle Dateien des file_array's aus dem Pfad dir. Ein leeres file_array bedeutet alle Dateien des Pfades lesen.
    # Wenn color_key gesetzt ist wird dieser hinzugefügt.
    # Bei den Endgegner ist zudem eine alpha convert notwendig. Dazu convert_aplha auf True setzten.
    # Wenn as_dict True ist wird ein Dictionary mit Dateiname und dazu gehöriger Datei zurückgegeben.
    if file_array == []:
        file_array = [f for f in listdir(dir) if path.isfile(path.join(dir, f)) and f != '.DS_Store']

    if as_dict:
        return_images = {}
    else:
        return_images = []

    for img in file_array:
        if convert_aplha:
            loaded_img = pygame.image.load(path.join(dir, img)).convert_alpha()
        else:
            loaded_img = pygame.image.load(path.join(dir, img)).convert()

        if color_key != None:
            loaded_img.set_colorkey(color_key)
        if len(file_array) == 1:
            return loaded_img
        else:
            if as_dict:
                return_images[img] = loaded_img
            else:
                return_images.append(loaded_img)

    return return_images

# Dateipfade herausfinden
# Diese Pythondatei sollte im gleichen Ordner liegen wie der img Ornder mit den Grafiken und der snd Ordner mit den Tönen
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

background = load_graphics_from_file_array(["background.png"], img_dir)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

player_colors = ["Blue","Green","Red","Yellow"]
file_array = list("plane{}{}.png".format(color,num) for color in player_colors for num in range(1,4))
player_images = load_graphics_from_file_array(file_array, path.join(img_dir,"Planes"),BLACK, as_dict=True)

rock_colors = ["Dirt","Grass","Ice","Snow"]
file_array = list("rock{}{}.png".format(color,up_down) for color in rock_colors for up_down in ["","Down"])
rock_images = load_graphics_from_file_array(file_array,path.join(img_dir,"Rocks"),BLACK, as_dict=True)
file_array = list("ground{}{}.png".format(color,up_down) for color in rock_colors for up_down in ["","Down"])
ground_images = load_graphics_from_file_array(file_array,path.join(img_dir,"Rocks"), BLACK, as_dict=True)

fallende_felsen_warnung = load_graphics_from_file_array(["warnungsschild.png"],img_dir,(0,0,255))

powerup_images = load_graphics_from_file_array(["medalGold.png","starGold.png"],path.join(img_dir,"UI"),BLACK,as_dict=True)

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = load_graphics_from_file_array([filename],path.join(img_dir,"Explosions"),color_key=BLACK)
    explosion_anim['lg'].append(pygame.transform.scale(img, (75, 75)))
    explosion_anim['sm'].append(pygame.transform.scale(img, (32, 32)))
    filename = 'sonicExplosion0{}.png'.format(i)
    img = load_graphics_from_file_array([filename],path.join(img_dir,"Explosions"),color_key=BLACK)
    explosion_anim['player'].append(img)

#full_row_sound = pygame.mixer.Sound(path.join(snd_dir, 'full_row.wav'))
#full_row_sound.set_volume(game_sound_volume)

#pygame.mixer.music.load(path.join(snd_dir, 'Original - Tetris.ogg'))
#pygame.mixer.music.set_volume(game_music_volume)
#pygame.mixer.music.play(loops=-1)