# Import
import pygame
import random

from Setting import muurgrootte , zone1 , zone2 , gebruikte_maze, a_star

#----------------------------------------------------------------------------------------------------------------------#

# Vijand
snelheid_monster = 2
snelheid_monster_2 = 2

#----------------------------------------------------------------------------------------------------------------------#



# Klasse voor vijanden (spoken), met AI gedrag per type
class Spook:
    def __init__(self, x, y, scherm, afbeelding, snelheid, type , toegelaten_posities_vijand , actief):
        self.scherm = scherm
        self.afbeelding = afbeelding
        self.snelheid = snelheid
        self.type = type
        self.toegelaten_posities_vijand = toegelaten_posities_vijand

        self.oorspronkelijke_type = type

        # Check op geldige positie
        if x is None or y is None:
            self.x, self.y = 0, 0
            self.rect = self.afbeelding.get_rect(center=(0, 0))
            self.actief = False  # automatisch niet actief als positie ongeldig is
            self.initial_state = (0, 0)
        else:
            self.x, self.y = x, y
            self.rect = self.afbeelding.get_rect(center=(self.x, self.y))
            self.actief = actief
            self.initial_state = (x, y)

        self.pad = []
        self.doel_index = 0

    def draw(self):
        if not self.actief :
            return
        else :
            self.rect.center = (self.x, self.y)
            self.scherm.blit(self.afbeelding, self.rect)

    def volg_pad(self):
        if self.doel_index < len(self.pad):
            doel_x, doel_y = self.pad[self.doel_index]
            dx = doel_x - self.x
            dy = doel_y - self.y
            afstand = (dx**2 + dy**2) ** 0.5
            if afstand < self.snelheid:
                self.x, self.y = doel_x, doel_y
                self.doel_index += 1
            else:
                self.x += self.snelheid * dx / afstand
                self.y += self.snelheid * dy / afstand

    def patrol(self, speler, extra_speler=None):
        if not self.actief:
            return

        else:
            afstand_tot_speler = ((self.x - speler.x) ** 2 + (self.y - speler.y) ** 2) ** 0.5
            dichtbij = afstand_tot_speler < 2 * muurgrootte

            if self.doel_index >= len(self.pad):
                target = (speler.x, speler.y)  # default fallback target

                if self.type == "blinky":
                    # Soort 1: direct volgen
                    target = (speler.x, speler.y)

                elif self.type == "pinky":
                    # Soort 2: volgt met offset, tenzij dichtbij
                    if dichtbij:
                        target = (speler.x, speler.y)
                    else:
                        dx, dy = 0, 0
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_UP]:
                            dy = -4 * muurgrootte
                        elif keys[pygame.K_DOWN]:
                            dy = 4 * muurgrootte
                        elif keys[pygame.K_LEFT]:
                            dx = -4 * muurgrootte
                        elif keys[pygame.K_RIGHT]:
                            dx = 4 * muurgrootte
                        target = (speler.x + dx, speler.y + dy)

                elif self.type == "inky":
                    # Soort 3: onnauwkeurig volgen
                    if dichtbij:
                        # Slecht gedrag bij nabijheid
                        target = (speler.x + 3 * muurgrootte, speler.y + 3 * muurgrootte)
                    else:
                        dx, dy = 0, 0
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_UP]:
                            dy = -2 * muurgrootte
                        elif keys[pygame.K_DOWN]:
                            dy = 2 * muurgrootte
                        elif keys[pygame.K_LEFT]:
                            dx = -2 * muurgrootte
                        elif keys[pygame.K_RIGHT]:
                            dx = 2 * muurgrootte
                        projected = (speler.x + dx, speler.y + dy)

                        if extra_speler:
                            vx = projected[0] - extra_speler.x
                            vy = projected[1] - extra_speler.y
                            target = (extra_speler.x + 2 * vx, extra_speler.y + 2 * vy)
                        else:
                            target = projected

                elif self.type == "clyde":
                    # Soort 4: bang gedrag, vlucht tenzij ver weg
                    if dichtbij:
                        # Slechte reactie: trekt slecht naar speler
                        target = (speler.x + random.choice([-1, 1]) * muurgrootte,
                                  speler.y + random.choice([-1, 1]) * muurgrootte)
                    elif afstand_tot_speler > 160:
                        target = (speler.x, speler.y)
                    else:
                        target = (1 * muurgrootte, 17 * muurgrootte)

                elif self.type == "vlucht":
                    # Soort 5: altijd vluchten, geen dichtbij-check
                    vx = self.x - speler.x
                    vy = self.y - speler.y
                    lengte = (vx ** 2 + vy ** 2) ** 0.5 or 1
                    offset_x = random.randint(-2 * muurgrootte, 2 * muurgrootte)
                    offset_y = random.randint(-2 * muurgrootte, 2 * muurgrootte)
                    schaal = 2 * muurgrootte  # minder ver, minder slim
                    target_x = self.x + int((vx / lengte) * schaal) + offset_x
                    target_y = self.y + int((vy / lengte) * schaal) + offset_y
                    target = (target_x, target_y)

                # Pad berekenen
                self.pad = a_star(gebruikte_maze, (self.x, self.y), target, muurgrootte,
                                  self.toegelaten_posities_vijand)

                if not self.pad:
                    # fallback random doel
                    target = (random.choice(range(29)) * muurgrootte, random.choice(range(19)) * muurgrootte)
                    self.pad = a_star(gebruikte_maze, (self.x, self.y), target, muurgrootte,
                                      self.toegelaten_posities_vijand)

                self.doel_index = 0

            self.volg_pad()

    def reset(self):
        self.x, self.y = self.initial_state
        self.pad = []  # Leeg pad bij reset
        self.doel_index = 0  # Zorg dat hij bij volgende patrol direct een nieuw pad berekent

    def overdracht(self):
        if (self.x, self.y) == zone1:
            self.x, self.y = zone2
        elif (self.x, self.y) == zone2:
            self.x, self.y = zone1

    def verander_type(self, nieuw_type):
        self.type = nieuw_type

    def oorspronkelijk_type(self):
        self.type = self.oorspronkelijke_type

    def removeposities(self, lijstmetposities, index):
        if index in lijstmetposities:
            lijstmetposities.remove(index)

    def appendposities(self,lijstmetposities, index):
        if index not in lijstmetposities:
            lijstmetposities.append(index)

    def zet_actief(self, waarde: bool):
        self.actief = waarde