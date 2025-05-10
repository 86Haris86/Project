# Import
import pygame

#from Setting import interval
interval = 5


#----------------------------------------------------------------------------------------------------------------------#

# Checkt  of de vijand/Speler op de 'tegel' mag gaan
class MazeChecker:
    def __init__(self, maze, afmeting):
        self.maze = maze
        self.afmeting = afmeting

    def is_valid(self, x, y , toegelaten_posities):
        kol = x // self.afmeting
        rij = y // self.afmeting
        if self.maze[rij][kol] in toegelaten_posities:
            return True
        return False

#----------------------------------------------------------------------------------------------------------------------#

# Maze inlezen (29x19)
def maze_van_bestand(bestand):
    document = []
    file = open(bestand, 'r')
    for lijn in file:
        lijn = lijn.strip().split()
        lijn = [int(cijfer) for cijfer in lijn]
        document.append(lijn)
    file.close()
    return document

#----------------------------------------------------------------------------------------------------------------------#

# nakijken of er een botsing is tussen een speler en spook
def check_collision2(speler, spook):
    # Maak een rechthoek voor de speler op basis van zijn positie en straal
    speler_rect = pygame.Rect(speler.x - speler.radius, speler.y - speler.radius, speler.radius * 2, speler.radius * 2)

    # Controleer of de speler's rechthoek botst met de rechthoek van het spook
    if speler_rect.colliderect(spook.rect):
        return True  # Als er een botsing is, retourneer True
    else:
        return False  # Als er geen botsing is, retourneer False

#----------------------------------------------------------------------------------------------------------------------#

# Checkt of speler en spook: leeuwen etc voila botsen met elkaar
def check_collision(speler, spook):
    speler_rect = pygame.Rect(speler.x - speler.radius, speler.y - speler.radius , speler.radius-interval, speler.radius+interval)
    return speler_rect.colliderect(spook.rect)

#----------------------------------------------------------------------------------------------------------------------#

# Teken hartjes linksboven misschien later voor elk niveau iets anders
def toon_levens(screen, levens):
    hart_afbeelding = pygame.image.load("LEVEL 3/hart1.png")
    hart_afbeelding = pygame.transform.scale(hart_afbeelding, (25, 25))
    for i in range(levens):
        screen.blit(hart_afbeelding, (10 + i * 35, 10))
    # de functie algemener maken

#----------------------------------------------------------------------------------------------------------------------#

def herstart_spel(speler, spoken, levens):
    # Verlies levens (of pas aan naar 1 per collision als je dat liever hebt)
    speler.levens -= levens
    speler.reset()

    for spook in spoken:
        spook.reset()
        spook.pad = []  # leeg oud pad
        spook.doel_index = 0  # index terug op 0
        spook.zet_actief(False)  # deactivate monster
        # breng het monster weer terug achter de deur
        spook.appendposities(toegelaten_posities_vijand, deur_van_spoken)

    pygame.time.delay(1000)

#----------------------------------------------------------------------------------------------------------------------#