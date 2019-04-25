import pygame
import time
from joystickpins import JoystickPins, KeyboardStick
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

        # Explosion am Ende abwarten
        self.in_end_expl = False
        self.expl = None

        # Zum erstellen der Felsen benötigte Variablen
        self.last_rock_placing = pygame.time.get_ticks()
        self.current_rock_type = GEGENUEBER
        self.time_for_next_rock = 800
        self.rock_counter = 0
        self.rock_color = random.choice(rock_colors)

        # Geschwindigkeit mit der sich fallende Felsen und Boden bewegen
        self.speed = 10

        # Zum Testen des Spiels den Spieler unsterblich machen (True -> sterblich, False -> unsterblich)
        self.kill_able = True

        # Für den Countdown (in millisekunden)
        self.coutdown_start_time = 0

        # Für die Bewegung des Hintergrunds
        self.background_x = 0

        # Erreichtes
        self.collected_starts = 0

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

    def wait_for_single_multiplayer_selection(self):
        # Am Anfang, vor dem Spiel, wird zwischen Single und Multiplayer ausgewählt.
        # Links und Rechts wird zum Auswahl ändern benutzt, A oder B zum auswählen. Esc zum Spiel beenden
        self.find_josticks()
        selected = 1
        waiting = True
        last_switch = pygame.time.get_ticks()
        while waiting:
            clock.tick(FPS)
            self.show_on_screen(screen, self.game_status, selected)
            pygame.display.flip()
            # Quit-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if self.check_key_pressed(ESC):
                pygame.quit()
            # Auswahl ändern durch hochzählen von selected
            if self.check_key_pressed(LEFT) or self.check_key_pressed(RIGHT) or self.check_key_pressed(UP) or self.check_key_pressed(DOWN):
                if last_switch + 300 < pygame.time.get_ticks():
                    last_switch = pygame.time.get_ticks()
                    selected += 1
                    if selected > 1:
                        selected = 0
            # Auswahl getroffen
            if self.check_key_pressed(AB):
                # Single-palyer
                if selected == 1:
                    # Auswählen welcher Kontroller genommen werden soll, wenn Auswahl gepasst hat Spiel starten, sonst nochmals nach Kontrollern suchen und wieder zwischen Multi- und Singelplayer wählen lassen
                    if self.wait_for_joystick_confirm(screen, 1):
                        waiting = False
                        self.end_game = None
                        self.multiplayer = False
                # Multi-palyer
                elif selected == 0:
                    # Auswählen welche Kontroller genommen werden soll. Weitere Schritte wie beim Single-player
                    if self.wait_for_joystick_confirm(screen, 2):
                        waiting = False
                        self.end_game = None
                        self.multiplayer = True

    def wait_for_joystick_confirm(self, surf, num_joysticks):
        # Diese Funktion zeigt den Bilschirm an, auf dem die zu benutzenden Kontroller gewählt werden.
        # num_joysticks ist die Anzahl der zu wählenden Joysticks
        # Links und Rechts zum Auswahl ändern. A oder B zum Auswählen
        # X oder Y um zurück zur Multi- / Singleplayer auswahl zu kommen

        # Angeschlossene Kontroller finden
        self.find_josticks()

        # Auswahlbilschrimanzeigen
        self.show_on_screen(surf, None)
        self.draw_text(surf, "Wähle deine Kontroller", 32, WIDTH / 2, HEIGHT / 2.2)
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
            self.show_on_screen(surf, None)
            self.draw_text(surf, "Wähle deine Kontroller", 32, WIDTH / 2, HEIGHT / 2.2)
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

    def show_on_screen(self, surf, calling_reason, selected=None):
        self.draw_background(screen)

        # Je nach dem ob es um die Kontrollerauswahl geht ein anderen Text zeigen
        if calling_reason == START_GAME:
            self.draw_text(surf, "Flappy Plane", 32, WIDTH / 2, HEIGHT / 2.2)
            if selected == 0:
                self.draw_text(surf, "Multi player", 34, WIDTH / 2 + 100, HEIGHT / 1.8, color=TEXT_RED)
                self.draw_text(surf, "Single player", 25, WIDTH / 2 - 100, HEIGHT / 1.8 + 8)
            else:
                self.draw_text(surf, "Multi player", 25, WIDTH / 2 + 100, HEIGHT / 1.8 + 8)
                self.draw_text(surf, "Single player", 34, WIDTH / 2 - 100, HEIGHT / 1.8, color=TEXT_RED)

        # Standart Texte
        self.draw_text(surf, "Flappy!", 64, WIDTH / 2, HEIGHT / 6.5)
        self.draw_text(surf, "Drücke Start oder Leertaste zum Starten", 18, WIDTH / 2, HEIGHT * 4 / 5)
        self.draw_text(surf, "Drücke Start und Select oder Leertaste und Enter zum Beenden", 18, WIDTH / 2, HEIGHT * 4 / 5 + 23)

        if calling_reason == START_GAME:
            self.draw_text(surf, "A/D oder Joystick zum Auswahl ändern, Pfeiltaste oder A/B zum Auswählen", 20, WIDTH / 2, HEIGHT * 3 / 4)

    def show_end_game_info(self, surf, center_x, y):
        if self.game_status == NEXT_GAME or self.game_status == VERLOREN:
            self.draw_text(surf, "Flappy", 50, center_x, y)
            self.all_sprites.draw(screen)
        if self.game_status == VERLOREN:
            self.draw_text(surf, "Verloren!", 70, center_x, y+70, TEXT_RED)
        if not self.game_status == BEFORE_FIRST_GAME:
            self.draw_text(surf, "Start zum Nochmalspielen", 20, center_x, y + 185)
        else:
            self.draw_text(surf, "Start drücken um loszuspielen", 50, center_x, y + 120)
            self.draw_text(surf, "X/Y oder Pfeiltasten für Einstellungen", 50, center_x, y + 200)

        pygame.display.flip()
        time.sleep(0.5)

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

        self.game_status = START_GAME

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
        # Multiplayerauswahl
        self.wait_for_single_multiplayer_selection()
        self.game_status = BEFORE_FIRST_GAME
        screen.fill(BLACK)
        self.draw_background(screen)
        self.show_end_game_info(screen, WIDTH / 2, 20)
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

            # Skalen und Texte auf den Bildschirm malen
            self.all_sprites.draw(screen)
            self.draw_display()

            # Nachdem alles gezeichnet ist anzeigen
            pygame.display.flip()

    def new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.rocks = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()

        # neue Spieler
        player_color = random.choice(player_colors)
        self.player = Player(self,color=player_color)
        self.all_sprites.add(self.player)

        # Spielfeld
        self.rock_color = random.choice(rock_colors)
        ground1 = Ground(self, FROM_BUTTON,color=self.rock_color)
        self.all_sprites.add(ground1)
        self.rocks.add(ground1)
        ground2 = Ground(self, FROM_TOP,color=self.rock_color )
        self.all_sprites.add(ground2)
        self.rocks.add(ground2)

        # Spielfelderstell Variablen zurücksetzen
        self.last_rock_placing = pygame.time.get_ticks()
        self.current_rock_type = GEGENUEBER
        self.time_for_next_rock = 800
        self.rock_counter = 0

        # Spielwerte zurücksetzen
        self.running = True
        self.in_end_expl = False

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
                    höhe = (0.2 * self.rock_counter + 0.2) * (HEIGHT/2 - HEIGHT/6)
                else:
                    höhe = (0.2 * (-self.rock_counter+8) + 0.2) * (HEIGHT / 2 - HEIGHT / 6)
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
                höhe = 100
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
        if self.kill_able:
            hit_place = (-100, -100)
            hits = pygame.sprite.spritecollide(self.player, self.rocks, False)
            if len(hits) > 0:
                self.player.mask = pygame.mask.from_surface(self.player.image)
                for rock in self.rocks:
                    hit = pygame.sprite.collide_mask(self.player, rock)
                    if hit is not None:
                        hit_place = hit
                        self.expl = Explosion(self,(hit_place[0]+self.player.rect.centerx,hit_place[1]+self.player.rect.centery),"player")
                        self.all_sprites.add(self.expl)
                        self.in_end_expl = True

        # Überprüfen, ob der Spieler ein PowerUp gesammelt hat
        hits = pygame.sprite.spritecollide(self.player, self.power_ups, True)
        for hit in hits:
            if hit.type == STAR:
                self.collected_starts += 1

    def draw_display(self):
        # Bildschrim zeichnen
        if self.game_status == NEXT_GAME or self.game_status == VERLOREN:
            self.show_end_game_info(screen,WIDTH/2,180)
        elif self.game_status == COUNTDOWN:
            text = str(3-round((time.time() * 1000 - self.coutdown_start_time)/1000))
            self.draw_text(screen,text,150,WIDTH/2,HEIGHT/2,TEXT_YELLOW,"mitte")
            if time.time() * 1000 - self.coutdown_start_time >= 2000:
                self.game_status = None
        else:
            self.draw_text(screen, str(self.collected_starts), 60, 80, 20, TEXT_COLOR, "oben_mitte")

game = Game()
game.start_game()

pygame.quit()