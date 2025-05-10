# Import
import pygame
import time
#import update

from Setting import maze_checker , tijd_van_bonus , zone1 , zone2 ,toegelaten_posities_speler , muurgrootte , refactor
from Setting import gebruikte_maze, walls, muurgrootte

#----------------------------------------------------------------------------------------------------------------------#

# speler
snelheid_speler = 5
radius_speler = 14
levens = 3

#----------------------------------------------------------------------------------------------------------------------#

# Klasse die de speler representeert en beweging/leven/overdracht regelt
class Speler:
    def __init__(self, x, y, scherm, kleur , straal, snelheid , toegelaten_posities , afbeelding = None):
        self.x, self.y = x, y
        self.scherm = scherm
        self.kleur = kleur
        self.straal = straal
        self.snelheid = snelheid
        self.toegelaten_posities = toegelaten_posities
        self.afbeelding = afbeelding

        self.startpositie = (x, y)
        self.levens = 3
        self.punten = 0
        self.timer = None
        self.timer_duur = None
        self.snelheid_standaard = snelheid  # Bewaar de normale snelheid
        self.snelheid_timer = None  # Start op None, wordt gevuld bij boost
        self.snelheid_duur = 5000
        self.break_walls = False  # power-up: muren kapot


        self.richting = None  # Toegevoegd: huidige richting ("UP", "DOWN", etc.)
        self.richting2 = "rechts"  # standaard richting voor pacman
        self.animatie_index = 0
        self.animatie_teller = 0
        self.eetcombo = 0

    def draw(self):
        if self.afbeelding:
            img = self.afbeelding[self.animatie_index]

            # Afbeelding roteren op basis van richting
            if self.richting2 == "rechts":
                rotated = img
            elif self.richting2 == "links":
                rotated = pygame.transform.flip(img, True, False)
            elif self.richting2 == "omhoog":
                rotated = pygame.transform.rotate(img, 90)
            elif self.richting2 == "omlaag":
                rotated = pygame.transform.rotate(img, -90)
            else:
                rotated = img  # fallback bij geen richting

            rect = rotated.get_rect(center=(self.x, self.y))
            self.scherm.blit(rotated, rect)
        else:
            # Fallback: gewone cirkel als geen afbeelding beschikbaar is
            pygame.draw.circle(self.scherm, self.kleur, (int(self.x), int(self.y)), self.straal)

    def update_animatie(self):
        self.animatie_teller += 1
        if self.animatie_teller % 5 == 0:
            self.animatie_index = (self.animatie_index + 1) % len(self.afbeelding)

    def Controleren(self, posities):
        for coordinaat_x, coordinaat_y in posities:
            if not maze_checker.is_valid(coordinaat_x, coordinaat_y, self.toegelaten_posities):
                return False
        return True

    def move(self,  snelheid_x, snelheid_y):

        # Richting bepalen (voor animatie)
        if snelheid_x > 0:
            self.richting2 = "rechts"
        elif snelheid_x < 0:
            self.richting2 = "links"
        elif snelheid_y < 0:
            self.richting2 = "omhoog"
        elif snelheid_y > 0:
            self.richting2 = "omlaag"

        nieuw_x, nieuw_y = self.x + snelheid_x ,  self.y + snelheid_y

        # Controleer of alle randen van de cirkel in toegelaten ruimte zitten
        te_controleren_posities = [
            (nieuw_x + self.straal, nieuw_y + self.straal),
            (nieuw_x + self.straal, nieuw_y - self.straal),
            (nieuw_x - self.straal, nieuw_y + self.straal),
            (nieuw_x - self.straal, nieuw_y - self.straal)
        ]

        # Power-up “muren kapot”: breek tile==31 als actief
        if self.break_walls:
            for coord_x, coord_y in te_controleren_posities:
                tx = int(coord_x // muurgrootte)
                ty = int(coord_y // muurgrootte)
                if gebruikte_maze[ty][tx] == 31:
                    # Vind de bijbehorende muur en start de breek-animatie
                    for wall in walls:
                        if wall.x == tx * muurgrootte and wall.y == ty * muurgrootte:
                            wall.start_break()  # ← animatie flag
                            break
                    gebruikte_maze[ty][tx] = 0
        geldig = True
        for coordinaat_x, coordinaat_y in te_controleren_posities:
            if not maze_checker.is_valid(coordinaat_x, coordinaat_y, toegelaten_posities_speler):
                geldig = False
                break
        if geldig:
            self.x = nieuw_x
            self.y = nieuw_y
            self.update_animatie()

    def patrol(self):
        keys = pygame.key.get_pressed()
        nieuw_x, nieuw_y = self.x + self.snelheid, self.y + self.snelheid
        te_controleren_posities = [
            (nieuw_x + self.straal, nieuw_y + self.straal),
            (nieuw_x + self.straal, nieuw_y - self.straal),
            (nieuw_x - self.straal, nieuw_y + self.straal),
            (nieuw_x - self.straal, nieuw_y - self.straal)
        ]

        # Update richting bij nieuwe toetsaanslagen
        if keys[pygame.K_DOWN]:
            nieuw_x, nieuw_y = self.x, self.y + self.snelheid
            te_controleren_posities = [(nieuw_x + self.straal, nieuw_y + self.straal), (nieuw_x - self.straal, nieuw_y + self.straal)]
            if self.Controleren(te_controleren_posities):
                self.richting = "DOWN"

        elif keys[pygame.K_UP]:
            nieuw_x, nieuw_y = self.x, self.y - self.snelheid
            te_controleren_posities = [(nieuw_x + self.straal, nieuw_y - self.straal), (nieuw_x - self.straal, nieuw_y - self.straal)]
            if self.Controleren(te_controleren_posities):
                self.richting = "UP"

        elif keys[pygame.K_LEFT]:
            nieuw_x, nieuw_y = self.x - self.snelheid, self.y
            te_controleren_posities = [(nieuw_x - self.straal, nieuw_y + self.straal), (nieuw_x - self.straal, nieuw_y - self.straal)]
            if self.Controleren(te_controleren_posities):
                self.richting = "LEFT"

        elif keys[pygame.K_RIGHT]:
            nieuw_x, nieuw_y = self.x + self.snelheid, self.y
            te_controleren_posities = [(nieuw_x + self.straal, nieuw_y + self.straal), (nieuw_x + self.straal, nieuw_y - self.straal)]
            if self.Controleren(te_controleren_posities):
                self.richting = "RIGHT"

        # Blijf bewegen in huidige richting
        if self.richting == "DOWN":
            self.move(0, self.snelheid)
        elif self.richting == "UP":
            self.move(0, -self.snelheid)
        elif self.richting == "LEFT":
            self.move(-self.snelheid, 0)
        elif self.richting == "RIGHT":
            self.move(self.snelheid, 0)

    def reset(self):
        self.x, self.y = self.startpositie

    def overdracht(self):
        if zone1 == None and zone2 == None:
            return
        else :
            if (self.x, self.y) == zone1:
                self.x, self.y = zone2
            elif (self.x, self.y) == zone2:
                self.x, self.y = zone1

    def start_eetmodus(self):
        self.timer = time.time()  # actieve eetmodus met echte tijd
        self.eetcombo = 0  # reset combo wanneer nieuwe modus start

    def eetmodus_actief(self):
        if self.timer is None:
            return False
        if time.time() - self.timer <= tijd_van_bonus:  # 30 seconden duren
            return True
        else:
            self.timer = None  # Zet terug naar None als tijd voorbij is
            return False

    def botsing(self, spook):
        spelerx1 = self.x - self.straal
        spelerx2 = self.x + self.straal
        spelery1 = self.y - self.straal
        spelery2 = self.y + self.straal

        x1 = spook.centerbalx - spook.straal + refactor
        x2 = spook.centerbalx + spook.straal - refactor
        y1 = spook.centerbaly - spook.straal + refactor
        y2 = spook.centerbaly + spook.straal - refactor

        return spelerx2 > x1 and spelerx1 < x2 and spelery2 > y1 and spelery1 < y2

    def check_collision(self, spook):
        speler_rect = pygame.Rect(self.x - self.straal + 3, self.y - self.straal + 3, (self.straal-4) * 2  , (self.straal-4) * 2 )
        return speler_rect.colliderect(spook.rect)

    def eetspook(self, spook):
        if self.eetmodus_actief() and self.check_collision(spook):
            self.eetcombo += 1
            punten = 50 * self.eetcombo  # Combo: 50, 100, 150, ...
            spook.reset()
            return punten
        return 0

    def toon_timer(self, scherm, font , x_positie, y_positie , kleur):
        if self.eetmodus_actief():
            resterende_tijd = max(0, int(tijd_van_bonus - (time.time() - self.timer)))
            tekst = font.render(f"Eetmodus: {resterende_tijd}s", True, kleur)  # Gele tekst
            scherm.blit(tekst, (x_positie, y_positie))  # Positie linksboven

    def start_timer(self, duur_in_seconden):
        self.timer = pygame.time.get_ticks()
        self.timer_duur = duur_in_seconden * 1000  # omzetten naar milliseconden

    def is_op_triggertegel(self, tegels):
        tegel_x = self.x // muurgrootte
        tegel_y = self.y // muurgrootte
        return (tegel_x, tegel_y) in tegels

    def activeer_snelheid(self, boost=2, duur=50000):
        self.snelheid += boost
        self.snelheid_timer = pygame.time.get_ticks()
        self.snelheid_duur = duur

    def update_snelheid(self):
        if self.snelheid_timer and pygame.time.get_ticks() - self.snelheid_timer > self.snelheid_duur:
            self.snelheid = self.snelheid_standaard
            self.snelheid_timer = None
