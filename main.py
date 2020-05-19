import pygame
import time
from math import sin
import __init__
try:
    from joystickpins import JoystickPins, KeyboardStick
except Exception:
    from joystickpins import joystickpins
    JoystickPins = joystickpins.JoystickPins
    KeyboardStick = joystickpins.KeyboardStick
from constants import *
from sprites import *

class Game():
    def __init__(self):
        self.game_status = START_GAME
        self.running = True
        screen.blit(background, background_rect)

        # Kontroller und Multiplayer
        self.multiplayer = False
        self.all_joysticks = []
        self.find_josticks()

        # Zum erstellen der Felsen benötigte Variablen
        self.last_rock_placing = pygame.time.get_ticks()
        self.current_rock_type = None
        self.time_for_next_rock = 800
        self.rock_counter = 0
        self.rock_color = random.choice(rock_colors)

        # Geschwindigkeit mit der sich fallende Felsen und Boden bewegen
        self.speed = 10

        # Zum Testen des Spiels den Spieler unsterblich machen (True -> sterblich, False -> unsterblich)
        self.kill_able = True

        # Level in dem sich das Spiel gerade befindet
        self.level = 1

        # Chance zur der ein Power-Up ein Schild ist und Dauer, wie lange man ein Schild hat
        self.schild_percent = 0.1
        self.schild_time = 5000
        self.schild = None
        self.max_schild_percent = 0.15 # Chance in Level 1
        self.min_schild_percent = 0.08 # Chance in Level 30, dazwischen linearer Zusammenhang

        # Eingesammele Sterne und benötigte Sterne um ins nächste Level zu kommen
        self.collected_stars = 0
        self.needed_stars = 20
        self.min_needed_stars = 20 # Benötigte Sterne in Level 1
        self.max_needed_stars = 50 # Benötigte Sterne in Level 30, dazwischen linearer Zusammenhang

        # Für den Countdown (in millisekunden)
        self.coutdown_start_time = 0

        # Für die Bewegung des Hintergrunds
        self.background_x = 0

        # Explosion am Ende abwarten
        self.in_end_expl = False
        self.expl = None

    def make_game_values_more_difficult(self):
        # Diese Funktion ändert Anzahl der benötigten Sterne und die Chance ein Schild zu bekommen in Abhängigkeit des Levels zwischen den jeweiligen min und max Werten
        # Bei Level 30 ist der Maxwert erreicht, dazwischen ist ein linearer Zsammenhang nach y= m*x +b
        m = (self.max_needed_stars-self.min_needed_stars)/(30-1)
        b = self.max_needed_stars - m * 30
        self.needed_stars = int(m * self.level + b)
        m = (self.min_schild_percent - self.max_schild_percent) / (30 - 1)
        b = self.min_schild_percent - m * 30
        self.schild_percent = m * self.level + b

    def find_josticks(self):
        # Knöpfe und Kontroller finden und Initialisieren
        self.all_joysticks = [JoystickPins(KeyboardStick())]
        for joy in range(pygame.joystick.get_count()):
            pygame_joystick = pygame.joystick.Joystick(joy)
            pygame_joystick.init()
            my_joystick = JoystickPins(pygame_joystick)
            self.all_joysticks.append(my_joystick)
            print("found_joystick: " + my_joystick.get_name())

    def draw_text(self, surf, text, size, x, y, color=TEXT_COLOR, rect_place="oben_mitte"):
        # Zeichnet den text in der color auf die surf.
        # x und y sind die Koordinaten des Punktes rect_place. rect_place kann "oben_mitte", "oben_links" oder "oben_rechts" sein.
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if rect_place == "oben_mitte":
            text_rect.midtop = (x, y)
        elif rect_place == "oben_links":
            text_rect.x = x
            text_rect.y = y
        elif rect_place == "oben_rechts":
            text_rect.topright = (x, y)
        elif rect_place == "mitte":
            text_rect.center = (x, y)
        elif rect_place == "mitte_links":
            text_rect.midleft = (x,y)
        surf.blit(text_surface, text_rect)

    def check_key_pressed(self, check_for=ALL, joystick_num="both"):
        # Überprüft ob die Taste(n) check_for gedrückt ist und achtet dabei auch auf Multi und Singleplayer.
        # Bei Multiplayer kann mit joystick_num zusätzlich mitgegeben werden welcher Kontroller gemeint ist.
        if self.multiplayer:
            if joystick_num == "both":
                for joystick in self.all_joysticks:
                    if check_for == JUMP:
                        if joystick.get_axis_up() or joystick.get_A() or joystick.get_B():
                            return True
                    if check_for == LEFT:
                        if joystick.get_axis_left() or joystick.get_shoulder_left():
                            return True
                    if check_for == RIGHT:
                        if joystick.get_axis_right() or joystick.get_shoulder_right():
                            return True
                    if check_for == UP:
                        if joystick.get_axis_up():
                            return True
                    if check_for == DOWN:
                        if joystick.get_axis_down():
                            return True
                    if check_for == ESC:
                        if joystick.get_select() and joystick.get_start():
                            return True
                    if check_for == START:
                        if joystick.get_start():
                            return True
                    if check_for == ALL:
                        if joystick.get_A() or joystick.get_B() or joystick.get_X() or joystick.get_Y() or joystick.get_start() or joystick.get_shoulder_left() or joystick.get_shoulder_right() or joystick.get_axis_left() or joystick.get_axis_right() or joystick.get_axis_up() or joystick.get_axis_down():
                            return True
                    if check_for == XY:
                        if joystick.get_X() or joystick.get_Y():
                            return True
                    if check_for == AB:
                        if joystick.get_A() or joystick.get_B():
                            return True
                    if check_for == X:
                        if joystick.get_X():
                            return True
                    if check_for == B:
                        if joystick.get_B():
                            return True
            else:
                if check_for == JUMP:
                    if self.all_joysticks[joystick_num].get_axis_up() or self.all_joysticks[joystick_num].get_A() or self.all_joysticks[joystick_num].get_B():
                        return True
                if check_for == LEFT:
                    if self.all_joysticks[joystick_num].get_axis_left() or self.all_joysticks[joystick_num].get_shoulder_left():
                        return True
                if check_for == RIGHT:
                    if self.all_joysticks[joystick_num].get_axis_right() or self.all_joysticks[joystick_num].get_shoulder_right():
                        return True
                if check_for == UP:
                    if self.all_joysticks[joystick_num].get_axis_up():
                        return True
                if check_for == DOWN:
                    if self.all_joysticks[joystick_num].get_axis_down():
                        return True
                if check_for == ESC:
                    if self.all_joysticks[joystick_num].get_select() and self.all_joysticks[joystick_num].get_start():
                        return True
                if check_for == START:
                    if self.all_joysticks[joystick_num].get_start():
                        return True
                if check_for == ALL:
                    if self.all_joysticks[joystick_num].get_A() or self.all_joysticks[joystick_num].get_B() or self.all_joysticks[joystick_num].get_X() or self.all_joysticks[joystick_num].get_Y()\
                        or self.all_joysticks[joystick_num].get_start() or self.all_joysticks[joystick_num].get_shoulder_left() or self.all_joysticks[joystick_num].get_shoulder_right() \
                        or self.all_joysticks[joystick_num].get_axis_left() or self.all_joysticks[joystick_num].get_axis_right() or self.all_joysticks[joystick_num].get_axis_up() \
                        or self.all_joysticks[joystick_num].get_axis_down():
                        return True
                if check_for == XY:
                    if self.all_joysticks[joystick_num].get_X() or self.all_joysticks[joystick_num].get_Y():
                        return True
                if check_for == AB:
                    if self.all_joysticks[joystick_num].get_A() or self.all_joysticks[joystick_num].get_B():
                        return True
                if check_for == X:
                    if self.all_joysticks[joystick_num].get_X():
                        return True
                if check_for == B:
                    if self.all_joysticks[joystick_num].get_B():
                        return True
        else:
            for joystick in self.all_joysticks:
                if check_for == JUMP:
                    if joystick.get_axis_up() or joystick.get_A() or joystick.get_B():
                        return True
                if check_for == LEFT:
                    if joystick.get_axis_left() or joystick.get_shoulder_left():
                        return True
                if check_for == RIGHT:
                    if joystick.get_axis_right() or joystick.get_shoulder_right():
                        return True
                if check_for == UP:
                    if joystick.get_axis_up():
                        return True
                if check_for == DOWN:
                    if joystick.get_axis_down():
                        return True
                if check_for == ESC:
                    if joystick.get_select() and joystick.get_start():
                        return True
                if check_for == START:
                    if joystick.get_start():
                        return True
                if check_for == ALL:
                    if joystick.get_A() or joystick.get_B() or joystick.get_X() or joystick.get_Y() or joystick.get_start() or joystick.get_shoulder_left() or joystick.get_shoulder_right() or joystick.get_axis_left() or joystick.get_axis_right() or joystick.get_axis_up() or joystick.get_axis_down():
                        return True
                if check_for == XY:
                    if joystick.get_X() or joystick.get_Y():
                        return True
                if check_for == AB:
                    if joystick.get_A() or joystick.get_B():
                        return True
                if check_for == X:
                    if joystick.get_X():
                        return True
                if check_for == B:
                    if joystick.get_B():
                        return True
        return False

    def wait_for_joystick_confirm(self, surf, num_joysticks):
        # Diese Funktion zeigt den Bilschirm an, auf dem die zu benutzenden Kontroller gewählt werden.
        # num_joysticks ist die Anzahl der zu wählenden Joysticks
        # Links und Rechts zum Auswahl ändern. A oder B zum Auswählen
        # X oder Y um zurück zur Multi- / Singleplayer auswahl zu kommen

        # Angeschlossene Kontroller finden
        self.find_josticks()

        # Auswahlbilschrimanzeigen
        self.show_on_screen(surf, None, False, with_waiting=False,diyplay_flip=False)
        self.draw_text(surf, "Wähle deinen Kontroller", 32, WIDTH / 2, HEIGHT / 2.2)
        for controller in self.all_joysticks:
            self.draw_text(surf, controller.get_name(), 28, WIDTH / 2 - 10, HEIGHT / 1.9 + 35 * self.all_joysticks.index(controller), rect_place="oben_rechts")
        pygame.display.flip()
        # warten, um zu verhindern, dass noch versehetlich Tasten auf einem falschem Kontroller gedrückt sind.
        time.sleep(0.5)

        # Auswahl starten
        selected_controllers = []
        selected_controller_num = 0
        last_switch = pygame.time.get_ticks()
        while len(selected_controllers) < num_joysticks:
            clock.tick(FPS)
            # Bildschrimzeichnen
            self.show_on_screen(surf, None, False, with_waiting=False, diyplay_flip=False)
            self.draw_text(surf, "Wähle deinen Kontroller", 32, WIDTH / 2, HEIGHT / 2.2)
            # Jeden gefundenen Kontroller zut Auswahl stellen
            for controller in self.all_joysticks:
                if self.all_joysticks.index(controller) == selected_controller_num:
                    self.draw_text(surf, controller.get_name(), 30, WIDTH / 2 - 10, HEIGHT / 1.9 + 35 * self.all_joysticks.index(controller), rect_place="oben_rechts", color=TEXT_RED)
                else:
                    self.draw_text(surf, controller.get_name(), 28, WIDTH / 2 - 10, HEIGHT / 1.9 + 35 * self.all_joysticks.index(controller), rect_place="oben_rechts")
                if controller in selected_controllers:
                    self.draw_text(surf, "bestätigt", 18, WIDTH / 2 + 10, HEIGHT / 1.9 + 8 + 35 * self.all_joysticks.index(controller), color=TEXT_GREEN, rect_place="oben_links")
                else:
                    self.draw_text(surf, "nicht bestätigt", 18, WIDTH / 2 + 10, HEIGHT / 1.9 + 8 + 35 * self.all_joysticks.index(controller), rect_place="oben_links")
            pygame.display.flip()
            # Quit-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if self.check_key_pressed(ESC):
                pygame.quit()
            # Auswahl ändern
            if (self.check_key_pressed(LEFT) or self.check_key_pressed(UP)) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                selected_controller_num -= 1
                if selected_controller_num < 0:
                    selected_controller_num = 0
            if (self.check_key_pressed(RIGHT) or self.check_key_pressed(DOWN)) and last_switch + 300 < pygame.time.get_ticks():
                last_switch = pygame.time.get_ticks()
                selected_controller_num += 1
                if selected_controller_num >= len(self.all_joysticks):
                    selected_controller_num = len(self.all_joysticks) - 1
            # Auswahl getroffen
            if self.check_key_pressed(AB):
                if self.all_joysticks[selected_controller_num] not in selected_controllers:
                    selected_controllers.append(self.all_joysticks[selected_controller_num])
            # Zurück zur Multi- / Singleplayer auswahl
            if self.check_key_pressed(XY):
                return False
        # Wenn genug Kontroller gewählt wurden stimmt die Auswahl. Es wrid True zurückgegeben
        if len(selected_controllers) == num_joysticks:
            self.all_joysticks = selected_controllers
            return True
        # Wenn die Auswahl nicht stimmt wird False zurückgegeben
        else:
            return False

    def show_on_screen(self, surf, calling_reason, with_selection=False, with_waiting=True, diyplay_flip=True):
        # Auf dem Bildschirm die Texte zeigen, die zwischen den Levels stehen.
        # Wenn with_waiting wird hier gewartet bis Start dedrückt wird.

        surf.blit(background, background_rect)

        # Je nach Art des SPielendes ein anderen Text zeigen
        if calling_reason == VERLOREN:
            self.all_sprites.draw(screen)
            self.draw_text(surf, "Verloren", 32, WIDTH / 2, HEIGHT / 2.2)
            self.draw_text(surf, "Versuche es gleich nochmal", 28, WIDTH / 2, HEIGHT / 1.8)
        elif calling_reason == NEXT_GAME:
            self.all_sprites.draw(screen)
            self.draw_text(surf, "Gewonnen", 32, WIDTH / 2, HEIGHT / 2.2)
            self.draw_text(surf, "Schaffst du das nächste Level auch?", 28, WIDTH / 2, HEIGHT / 1.8)
        elif calling_reason == BEFORE_FIRST_GAME:
            self.draw_text(surf, "Flappy Plane!", 32, WIDTH / 2, HEIGHT / 2.2)
        elif calling_reason == START_GAME:
            self.draw_text(surf, "Flappy Plane!", 32, WIDTH / 2, HEIGHT / 2.2)

        # Standart Texte
        self.draw_text(surf, "FLAPPY!", 64, WIDTH / 2, HEIGHT / 6.5)
        self.draw_text(surf, "Level: " + str(self.level), 45, WIDTH / 2, HEIGHT / 3.5)
        self.draw_text(surf, "Drücke Start oder Leertaste zum Starten", 18, WIDTH / 2, HEIGHT * 4 / 5)
        self.draw_text(surf, "Drücke Start und Select oder Leertaste und Enter zum Beenden", 18, WIDTH / 2, HEIGHT * 4 / 5 + 23)
        # Bei Multi- / Singleplayer auswahl steht wird der erste Text gezeigt, ansonten der normale
        if with_selection:
            self.draw_text(surf, "A/D oder Joystick zum Auswahl ändern, Pfeiltaste oder A/B zum auswählen", 20, WIDTH / 2, HEIGHT * 3 / 4)
        else:
            self.draw_text(surf, "A/B oder W auf der Tastatur zum hüpfen. Sterne einsammeln um Level zu schaffen", 20, WIDTH / 2, HEIGHT * 3 / 4)

        # Auf Diplay anzeigen
        if diyplay_flip:
            pygame.display.flip()

        # wenn_waiting hier auf Tastendruck von Start warten
        last_switch = pygame.time.get_ticks()
        if with_waiting:
            waiting = True
            while waiting:
                clock.tick(FPS)
                # Quit-events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                # mit Start geht's weiter
                if self.check_key_pressed(START):
                    waiting = False
                # Links und Rechts zum erhöhen oder verringern des Levels
                if self.check_key_pressed(LEFT) and last_switch + 300 < pygame.time.get_ticks():
                    last_switch = pygame.time.get_ticks()
                    self.level -= 1
                    if self.level < 1:
                        self.level = 1
                    self.make_game_values_more_difficult()
                    waiting = False
                    self.show_on_screen(surf, calling_reason, with_selection, with_waiting, diyplay_flip)
                if self.check_key_pressed(RIGHT) and last_switch + 300 < pygame.time.get_ticks():
                    last_switch = pygame.time.get_ticks()
                    self.level += 1
                    self.make_game_values_more_difficult()
                    waiting = False
                    self.show_on_screen(surf, calling_reason, with_selection, with_waiting, diyplay_flip)

    def show_game_info_and_bars(self, surf, x, y):
        # Zeichnet Infos zum aktuellem Spielstand
        # oben links aktuelles level
        self.draw_text(surf, str(self.level), 60, x, y, TEXT_COLOR, "oben_links")
        # rechts am Rand, wie weit man in diesem Level schon ist
        BAR_LENGTH = 20
        BAR_HEIGHT = HEIGHT - 100
        fill = (self.collected_stars / self.needed_stars) * BAR_HEIGHT
        if fill < 0:
            fill = 0
        if fill > BAR_HEIGHT:
            fill = BAR_HEIGHT
        outline_rect = pygame.Rect(x + 5, y + 75, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x + 5, y + 75 + BAR_HEIGHT - fill, BAR_LENGTH, fill)
        pygame.draw.rect(surf, [PLAYER_BLUE,PLAYER_GREEN,PLAYER_RED,PLAYER_YELLOW][player_colors.index(self.player.color)], fill_rect)
        pygame.draw.rect(surf, BLACK, outline_rect, 3)
        self.draw_text(surf, str(self.needed_stars), 25, x + 30, y + 75, TEXT_COLOR, "mitte_links")
        self.draw_text(surf, str(self.collected_stars), 25, x + 30, y + 75 + BAR_HEIGHT - fill, TEXT_COLOR, "mitte_links")

    def draw_background(self, surf):
        # Draw the background
        #  _____________
        # |             |
        # | Background  |
        # |_____________|
        #       WIDTH   \-> rel_x

        rel_x = self.background_x % WIDTH
        surf.blit(background, (rel_x - WIDTH, 0))
        # If Background doesn't cover the whole screen draw an other background to fill it
        if rel_x < WIDTH:
            surf.blit(background, (rel_x, 0))

        # If playing move the background
        if self.game_status == None and not self.in_end_expl:
            self.background_x -= 1

    ########## Hier startet das eigentliche Spiel ##########
    def start_game(self):
        # Kontrollerauswahl
        self.wait_for_joystick_confirm(screen,1)
        self.show_on_screen(screen, BEFORE_FIRST_GAME)
        self.game_status = START_GAME

        # Dauerschleife des Spiels
        while self.running:
            # Ist das Spiel aus irgendeinem Grund zu Ende, ist also game_over nicht None, werden alle Spieler, Gegner und Meteoriten erstellt und das Spiel gestartet
            if self.game_status == START_GAME:
                # Alles auf das neue Spiel vorbereiten, wie z.B. neue Farben, neuer Spieler, Spielfelderstellvariablen zurücksetzten, ...
                self.new()
                # In Countdownmudos wechseln und Coutndowntimer starten
                self.game_status = COUNTDOWN
                self.coutdown_start_time = time.time() * 1000
                self.countdown_text = None

            # Bilschirm leeren
            screen.fill(BLACK)
            self.draw_background(screen)

            # Auf Bildschirmgeschwindigkeit achten
            clock.tick(FPS)

            # Eingaben zum Verlassen des Spiels checken
            if self.check_key_pressed(ESC):
                self.running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Neue Felsen erstellenw
            if self.game_status == None and not self.in_end_expl:
                self.create_new_rocks_and_power_ups()

            # Bewegungen der Sprites asuführen
            self.all_sprites.update()

            # Nach Kollisionen suchen
            if self.game_status == None and not self.in_end_expl:
                self.detect_and_react_collisions()

            # Wenn die Endexplosion vorbei ist endet das Spiel
            if self.in_end_expl and not self.expl.alive():
                self.game_status = VERLOREN

            # Wenn genug Sterne eingesammelt wurden endet das Spiel
            if self.collected_stars >= self.needed_stars:
                won_sound.play()
                self.game_status = NEXT_GAME
                self.level += 1

            # Skalen und Texte auf den Bildschirm malen
            self.all_sprites.draw(screen)
            self.draw_display()

            # Nachdem alles gezeichnet ist anzeigen
            pygame.display.flip()

    def new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.rocks = pygame.sprite.Group()
        self.grounds = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()

        # neue Spieler
        player_color = random.choice(player_colors)
        self.player = Player(self,color=player_color)
        self.all_sprites.add(self.player)

        # Oben und Unten am Spielfeld den Boden bzw. die Decke platzieren
        self.rock_color = random.choice(rock_colors)
        ground1 = Ground(self, FROM_BUTTON,color=self.rock_color)
        self.all_sprites.add(ground1)
        self.rocks.add(ground1)
        self.grounds.add(ground1)
        ground2 = Ground(self, FROM_TOP,color=self.rock_color)
        self.all_sprites.add(ground2)
        self.rocks.add(ground2)
        self.grounds.add(ground2)

        # Spielfelderstell Variablen zurücksetzen
        self.last_rock_placing = pygame.time.get_ticks()
        self.current_rock_type = GEGENUEBER
        self.time_for_next_rock = 800
        self.rock_counter = 0

        # Spielwerte zurücksetzen
        self.running = True
        self.in_end_expl = False
        self.collected_stars = 0

        # Spielvaraiblen (also Chance ein Schild zu bekommen und benötigte Sterne) an das Level anpassen
        self.make_game_values_more_difficult()

    def create_new_rocks_and_power_ups(self):
        new_rock = None
        if self.current_rock_type == GEGENUEBER or self.current_rock_type == VERSETZT:
            if self.last_rock_placing < pygame.time.get_ticks() - self.time_for_next_rock:
                self.last_rock_placing = pygame.time.get_ticks()
                höhe = int(random.randrange(int(60 + HEIGHT / 3), int(HEIGHT - 60 - HEIGHT / 3)))
                new_rock = Rock(self, random.choice([FROM_BUTTON,FROM_TOP]), höhe = höhe, type = self.current_rock_type, color = self.rock_color, start_x = WIDTH)
                self.time_for_next_rock = random.randrange(500,1000) + [GEGENUEBER,VERSETZT].index(self.current_rock_type) * 850
                self.rock_counter += 1
                if self.rock_counter >= 12:
                    self.current_rock_type = random.choice([TUNNEL,KURVE,ZENTRAL,FALLEND])
                    if self.current_rock_type == FALLEND:
                        self.all_sprites.add(Warnungsschild(self))
                    self.rock_counter = 0
                    self.time_for_next_rock = 1250
        elif self.current_rock_type == TUNNEL:
            if self.last_rock_placing < pygame.time.get_ticks() - self.time_for_next_rock:
                self.last_rock_placing = pygame.time.get_ticks()
                if self.rock_counter <= 4:
                    höhe = (0.2 * self.rock_counter + 0.2) * (HEIGHT/2 - HEIGHT/7)
                else:
                    höhe = (0.2 * (-self.rock_counter+8) + 0.2) * (HEIGHT / 2 - HEIGHT / 7)
                new_rock = Rock(self, FROM_BUTTON, höhe = höhe, type = self.current_rock_type, color = self.rock_color, start_x = WIDTH)
                self.time_for_next_rock = 300
                self.rock_counter += 1
                if self.rock_counter >= 8:
                    self.current_rock_type = random.choice([VERSETZT,GEGENUEBER,KURVE,ZENTRAL,FALLEND])
                    if self.current_rock_type == FALLEND:
                        self.all_sprites.add(Warnungsschild(self))
                    self.rock_counter = 0
                    self.time_for_next_rock = 1250
        elif self.current_rock_type == KURVE:
            if self.last_rock_placing < pygame.time.get_ticks() - self.time_for_next_rock:
                self.last_rock_placing = pygame.time.get_ticks()
                # Sinuskurve der Funktion a⋅sin(b⋅x)+c
                a = ((HEIGHT - HEIGHT / 3) - (HEIGHT / 3)) / 2  # Streckung in y-Richtung
                b = 1.5  # Periodendauer (Streckung in x-Richtung)
                c = (HEIGHT / 3) + a  # Verschiebung nach oben
                höhe = (a * sin(b * self.rock_counter) + c) - HEIGHT/6
                new_rock = Rock(self, FROM_BUTTON, höhe = höhe, type = self.current_rock_type, color = self.rock_color, start_x = WIDTH)
                self.time_for_next_rock = 400
                self.rock_counter += 1
                if self.rock_counter >= 20:
                    self.current_rock_type = random.choice([TUNNEL,VERSETZT,GEGENUEBER,ZENTRAL,FALLEND])
                    if self.current_rock_type == FALLEND:
                        self.all_sprites.add(Warnungsschild(self))
                    self.rock_counter = 0
                    self.time_for_next_rock = 1250
        elif self.current_rock_type == ZENTRAL:
            if self.last_rock_placing < pygame.time.get_ticks() - self.time_for_next_rock:
                self.last_rock_placing = pygame.time.get_ticks()
                höhe = random.randrange(30,int(HEIGHT/2 - HEIGHT/3))
                new_rock = Rock(self, FROM_BUTTON, höhe = höhe, type = self.current_rock_type, color = self.rock_color, start_x = WIDTH)
                self.time_for_next_rock = random.randrange(400,800)
                self.rock_counter += 1
                if self.rock_counter >= 15:
                    self.current_rock_type = random.choice([TUNNEL,VERSETZT,GEGENUEBER,KURVE,FALLEND])
                    if self.current_rock_type == FALLEND:
                        self.all_sprites.add(Warnungsschild(self))
                    self.rock_counter = 0
                    self.time_for_next_rock = 1250
        elif self.current_rock_type == FALLEND:
            if self.last_rock_placing < pygame.time.get_ticks() - self.time_for_next_rock:
                self.last_rock_placing = pygame.time.get_ticks()
                höhe = int(random.randrange(int(60 + HEIGHT / 3), int(HEIGHT - 60 - HEIGHT/3)))
                new_rock = Rock(self, FROM_TOP, höhe = höhe, type = self.current_rock_type, color = self.rock_color, start_x = WIDTH)
                self.time_for_next_rock = random.randrange(250,500)
                self.rock_counter += 1
                if self.rock_counter >= 10:
                    self.current_rock_type = random.choice([TUNNEL,VERSETZT,GEGENUEBER,KURVE,ZENTRAL])
                    self.rock_counter = 0
                    self.time_for_next_rock = 1250
        if new_rock != None:
            self.all_sprites.add(new_rock)
            self.rocks.add(new_rock)

    def detect_and_react_collisions(self):
        # Überprüfen, ob der Spieler gegen ein Felsen geknallt ist
        if self.kill_able and not self.player.has_shield:
            hits = pygame.sprite.spritecollide(self.player, self.rocks, False)
            if len(hits) > 0:
                self.player.mask = pygame.mask.from_surface(self.player.image)
                for rock in self.rocks:
                    hit = pygame.sprite.collide_mask(self.player, rock)
                    if hit is not None:
                        hit_place = hit
                        player_die_sound.play()
                        self.expl = Explosion(self,(hit_place[0]+self.player.rect.centerx,hit_place[1]+self.player.rect.centery),"player")
                        self.all_sprites.add(self.expl)
                        self.in_end_expl = True

        # Überprüfen, ob der Spieler ein PowerUp gesammelt hat
        hits = pygame.sprite.spritecollide(self.player, self.power_ups, True)
        for hit in hits:
            if hit.type == STAR:
                star_sound.play()
                self.collected_stars += 1
            elif hit.type == MEDAL:
                shield_sound.play()
                self.player.start_shield()

    def draw_display(self):
        # Bildschrim zeichnen
        if self.game_status == NEXT_GAME or self.game_status == VERLOREN:
            self.show_on_screen(screen,self.game_status)
            self.game_status = START_GAME
        elif self.game_status == COUNTDOWN:
            self.show_game_info_and_bars(screen, 10, 2)
            self.countdown_text = str(3-round((time.time() * 1000 - self.coutdown_start_time)/1000))
            self.draw_text(screen,self.countdown_text,150,WIDTH/2,HEIGHT/2,TEXT_YELLOW,"mitte")
            if time.time() * 1000 - self.coutdown_start_time >= 2000:
                self.game_status = None
        else:
            self.show_game_info_and_bars(screen,10,2)

game = Game()
game.start_game()

pygame.quit()