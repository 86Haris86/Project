# Import and initialize the pygame library
import pygame
import heapq
import time

# Initialisatie
pygame.init()

# scherm groter maken met 'a' om de score bij te schrijven
a = 50
font = pygame.font.SysFont(None, 36)

# Scherminstellingen
breedte = int(870)
hoogte = int(570 + a)
screen = pygame.display.set_mode([breedte, hoogte])

# Kleuren
WIT = (255, 255, 255)
BLAUW = (0, 0, 128)
ROOD = (255, 0, 0)
GROEN = (0, 255, 0)
GEEL = (255, 255, 0)
ZWART = (0, 0, 0)

# Tijd
tijd = pygame.time.Clock()
fps = 30
tijd_van_bonus = 10

# Grootte van muur en rand
muurgrootte = 30
balgrootte = 2
balgrootte1 = 4
refactor = 1  # zodat de bal niet bij x(bal) = x(item) verdwijnt maar een beetje later

# extra
    # speler
snelheid_speler = 5
radius_speler = 14
    #
snelheid_monster = 4


# strartposities
    # maze1
        #speler
maze1_speler_startpositie_x, maze1_speler_startpositie_y = 14 * muurgrootte + muurgrootte//2, 12 * muurgrootte + muurgrootte//2
        #vijanden
maze1_voorwerp1_startpositie_x, maze1_voorwerp1_startpositie_y = 12 * muurgrootte + muurgrootte//2 + 1 * muurgrootte//5, 10 * muurgrootte + muurgrootte//2
maze1_voorwerp2_startpositie_x, maze1_voorwerp2_startpositie_y = 13 * muurgrootte + muurgrootte//2 + 2 * muurgrootte//5, 10 * muurgrootte + muurgrootte//2
maze1_voorwerp3_startpositie_x, maze1_voorwerp3_startpositie_y = 14 * muurgrootte + muurgrootte//2 + 3 * muurgrootte//5, 10 * muurgrootte + muurgrootte//2
maze1_voorwerp4_startpositie_x, maze1_voorwerp4_startpositie_y = 15 * muurgrootte + muurgrootte//2 + 4 * muurgrootte//5, 10 * muurgrootte + muurgrootte//2
    # Overdrachtszones
y_positi_blok = (10-1) * muurgrootte + muurgrootte//2
maze1_zone1 = (1 * muurgrootte, y_positi_blok)
maze1_zone2 = (28 * muurgrootte, y_positi_blok)


# maze2
    # speler
maze2_speler_startpositie_x, maze2_speler_startpositie_y = 14 * muurgrootte + muurgrootte // 2, 9 * muurgrootte + muurgrootte // 2

    # vijanden
maze2_voorwerp1_startpositie_x, maze2_voorwerp1_startpositie_y = 1 * muurgrootte + 15, 1 * muurgrootte + 15
maze2_voorwerp2_startpositie_x, maze2_voorwerp2_startpositie_y = 18 * muurgrootte + 15, 1 * muurgrootte + 15
maze2_voorwerp3_startpositie_x, maze2_voorwerp3_startpositie_y = 1 * muurgrootte + 15, 18 * muurgrootte + 15
maze2_voorwerp4_startpositie_x, maze2_voorwerp4_startpositie_y = 18 * muurgrootte + 15, 18 * muurgrootte + 15


    # maze3
        # speler
maze3_speler_startpositie_x, maze3_speler_startpositie_y = 14 * muurgrootte + muurgrootte//2, 9 * muurgrootte + muurgrootte//2

        # vijanden
maze3_voorwerp1_startpositie_x, maze3_voorwerp1_startpositie_y = 1 * muurgrootte + 15, 1 * muurgrootte + 15
maze3_voorwerp2_startpositie_x, maze3_voorwerp2_startpositie_y = 27 * muurgrootte + 15, 1 * muurgrootte + 15
maze3_voorwerp3_startpositie_x, maze3_voorwerp3_startpositie_y = 1 * muurgrootte + 15, 10 * muurgrootte + 15
maze3_voorwerp4_startpositie_x, maze3_voorwerp4_startpositie_y = 27 * muurgrootte + 15, 10 * muurgrootte + 15
    # Overdrachtszones
y_positi_blok = (10-1) * muurgrootte + muurgrootte//2
zone1 = (1 * muurgrootte, y_positi_blok)
zone2 = (28 * muurgrootte, y_positi_blok)

#----------------------------------------------------------------------------------------------------------------------#

# Menu tonen
def toon_menu():
    achtergrond = pygame.image.load("achtergrond_savanne.png")
    achtergrond = pygame.transform.scale(achtergrond, (breedte, hoogte))
    font = pygame.font.SysFont(None, 75)
    knop_rect = pygame.Rect(breedte // 2 - 100, hoogte // 2 - 50, 200, 100)

    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if knop_rect.collidepoint(event.pos):
                    menu_running = False

        screen.blit(achtergrond, (0, 0))
        pygame.draw.rect(screen, GROEN, knop_rect)
        tekst = font.render("Start", True, ZWART)
        screen.blit(tekst, (knop_rect.x + 40, knop_rect.y + 25))

        pygame.display.flip()

toon_menu()

#----------------------------------------------------------------------------------------------------------------------#

# Muur-layout (1 = muur, 0 = leeg) (29x19)
def maze_van_bestand(bestand):
    document = []
    file = open(bestand, 'r')
    for lijn in file:
        lijn = lijn.strip().split()
        lijn = [int(cijfer) for cijfer in lijn]
        document.append(lijn)
    file.close()
    return document

maze1 = maze_van_bestand("maze1.txt")
maze2 = maze_van_bestand("maze2.txt")
maze3 = maze_van_bestand("maze3.txt")

# maze dat wordt gebruikt bij het runnen
gebruikte_maze = maze1


#----------------------------------------------------------------------------------------------------------------------#

class Plan:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# specifiek over de muren van de plan
class Muur(Plan):
    def __init__(self, x, y, scherm, afmeting, kleur= None, afbeelding=None):
        super().__init__(x, y)
        self.scherm = scherm
        self.afmeting = afmeting
        self.kleur = kleur
        self.afbeelding = afbeelding

        self.rect = pygame.Rect(x, y, afmeting, afmeting)

    def draw(self):
        if self.afbeelding:
            self.scherm.blit(self.afbeelding, self.rect)
        else:
            pygame.draw.rect(self.scherm, self.kleur, self.rect)

# Object Klassen
class Object1(Plan):
    def __init__(self,x, y, scherm, straal, kleur):
        super().__init__(x, y)
        self.scherm = scherm
        self.straal = straal
        self.kleur = kleur

        self.center = (x + muurgrootte // 2, y + muurgrootte // 2)
        self.centerbalx = x + muurgrootte // 2
        self.centerbaly = y + muurgrootte // 2

    def draw(self):
        pygame.draw.circle(self.scherm, self.kleur, self.center, self.straal)

    def botsing(self, personage):
        # parameters van de speler in rechthoekvorm
        spelerx1 = personage.x - personage.radius
        spelerx2 = personage.x + personage.radius
        spelery1 = personage.y - personage.radius
        spelery2 = personage.y + personage.radius
        # parameters object in rechthoekvorm
        x1 = self.centerbalx - self.straal + refactor
        x2 = self.centerbalx + self.straal - refactor
        y1 = self.centerbaly - self.straal + refactor
        y2 = self.centerbaly + self.straal - refactor
        # botsing nagaan
        if spelerx2 > x1 and spelerx1 < x2 and spelery2 > y1 and spelery1 < y2:
            return True
        return False

    def punten(self):
        return 2

class Object2(Plan):
    def __init__(self,x, y,scherm, straal, kleur):
        super().__init__(x, y)
        self.kleur = kleur
        self.scherm = scherm
        self.center = (x + muurgrootte // 2, y + muurgrootte // 2)
        self.centerbalx = x + muurgrootte // 2
        self.centerbaly = y + muurgrootte // 2
        self.straal = straal

    def draw(self):
        pygame.draw.circle(self.scherm, self.kleur, self.center, self.straal)

    def botsing(self, personage):
        # parameters van de speler in rechthoekvorm
        spelerx1 = personage.x - personage.radius
        spelerx2 = personage.x + personage.radius
        spelery1 = personage.y - personage.radius
        spelery2 = personage.y + personage.radius
        # parameters object in rechthoekvorm
        x1 = self.centerbalx - self.straal + refactor
        x2 = self.centerbalx + self.straal - refactor
        y1 = self.centerbaly - self.straal + refactor
        y2 = self.centerbaly + self.straal - refactor
        # botsing nagaan
        if spelerx2 > x1 and spelerx1 < x2 and spelery2 > y1 and spelery1 < y2:
            return True
        return False

    def punten(self):
        return 10

#----------------------------------------------------------------------------------------------------------------------#

class MazeChecker:
    def __init__(self, maze, afmeting):
        self.maze = maze
        self.afmeting = afmeting

    def is_valid(self, x, y):
        kol = x // self.afmeting
        rij = y // self.afmeting
        if self.maze[rij][kol] in [0, 4, 5, 9, 18, 19 ]:
            return True
        return False
maze_checker = MazeChecker(gebruikte_maze, muurgrootte)

#----------------------------------------------------------------------------------------------------------------------#

# Muur + weg
img_wall0 = pygame.transform.scale(pygame.image.load("Savanne_decor/way_30x30.jpeg"), (30, 30))

#rivier
greenbleu_30x30 = pygame.transform.scale(pygame.image.load("Rivier/greenbleu_30x30.jpg"), (30, 30))
etoue_30x30 = pygame.transform.scale(pygame.image.load("struik/etoue_30x30.jpg"), (30, 30))
yellow_green_gradient = pygame.transform.scale(pygame.image.load("Rivier/yellow_green_gradient.png"), (30, 30))
resized_tile_0_4 = pygame.transform.scale(pygame.image.load("struik/resized_tile_0_4 (1).png"), (30, 30))

# weg
donkergroen = pygame.transform.scale(pygame.image.load("Voetbal_decor/donkergroen.png"), (30, 30))


# veld
lichtgroen = pygame.transform.scale(pygame.image.load("Voetbal_decor/lichtgroen.png"), (30, 30))
corner_LB = pygame.transform.scale(pygame.image.load("Voetbal_decor/corner(LB).png"), (30, 30))
corner_LBOVEN = pygame.transform.scale(pygame.image.load("Voetbal_decor/corner(LBOVEN).png"), (30, 30))
corner_RB_copy = pygame.transform.scale(pygame.image.load("Voetbal_decor/corner(RB) copy.png"), (30, 30))
corner_RBOVEN_copy_2 = pygame.transform.scale(pygame.image.load("Voetbal_decor/corner(RBOVEN) copy 2.png"), (30, 30))
separatie_boven = pygame.transform.scale(pygame.image.load("Voetbal_decor/separatie(boven).png"), (30, 30))
separatie = pygame.transform.scale(pygame.image.load("Voetbal_decor/separatie.png"), (30, 30))
wite_lijn_L = pygame.transform.scale(pygame.image.load("Voetbal_decor/wite lijn(L).jpg"), (30, 30))
wite_lijn_R = pygame.transform.scale(pygame.image.load("Voetbal_decor/wite lijn(R).png"), (30, 30))


#----------------------------------------------------------------------------------------------------------------------#

# Walls en Items vullen
walls = []
items = []
items2 = []
if maze1 == gebruikte_maze :
    start_positie_x_speler1, start_positie_y_speler1 = maze1_speler_startpositie_x, maze1_speler_startpositie_y

    start_positie_x_soort1, start_positie_y_soort1 = maze1_voorwerp1_startpositie_x, maze1_voorwerp1_startpositie_y
    start_positie_x_soort2, start_positie_y_soort2 = maze1_voorwerp2_startpositie_x, maze1_voorwerp2_startpositie_y
    start_positie_x_soort3, start_positie_y_soort3 = maze1_voorwerp3_startpositie_x, maze1_voorwerp3_startpositie_y
    start_positie_x_soort4, start_positie_y_soort4 = maze1_voorwerp4_startpositie_x, maze1_voorwerp4_startpositie_y

    for row_index, row in enumerate(gebruikte_maze):
        for col_index, tile in enumerate(row):
            x = col_index * muurgrootte
            y = row_index * muurgrootte
            if tile == 0:
                items.append(Object1(x, y, screen, balgrootte, WIT))
            elif tile == 1:
                walls.append(Muur(x, y, screen, muurgrootte, BLAUW))
            elif tile == 2:
                walls.append(Muur(x, y, screen, muurgrootte, ROOD))
            elif tile == 3:
                walls.append(Muur(x, y, screen, muurgrootte, GEEL))
            elif tile == 4:
                walls.append(Muur(x, y, screen, muurgrootte, GROEN))
            elif tile == 5:
                items.append(Object2(x, y, screen, balgrootte1, WIT))
                items2.append(Object2(x, y, screen, balgrootte1, WIT))



if maze3 == gebruikte_maze:
    start_positie_x_speler1, start_positie_y_speler1 = maze3_speler_startpositie_x, maze3_speler_startpositie_y

    start_positie_x_soort1, start_positie_y_soort1 = maze3_voorwerp1_startpositie_x, maze3_voorwerp1_startpositie_y
    start_positie_x_soort2, start_positie_y_soort2 = maze3_voorwerp2_startpositie_x, maze3_voorwerp2_startpositie_y
    start_positie_x_soort3, start_positie_y_soort3 = maze3_voorwerp3_startpositie_x, maze3_voorwerp3_startpositie_y
    start_positie_x_soort4, start_positie_y_soort4 = maze3_voorwerp4_startpositie_x, maze3_voorwerp4_startpositie_y

    for row_index, row in enumerate(gebruikte_maze):
        for col_index, tile in enumerate(row):
            x = col_index * muurgrootte
            y = row_index * muurgrootte
            if tile == 0:
                items.append(Object1(x, y, screen, balgrootte, WIT))
            elif tile == 1:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=resized_tile_0_4))
            elif tile == 2:
                walls.append(Muur(x, y, screen, muurgrootte, kleur=ROOD))
            elif tile == 3:
                walls.append(Muur(x, y, screen, muurgrootte, kleur=GEEL))
            elif tile == 4:
                walls.append(Muur(x, y, screen, muurgrootte, kleur=GROEN))
            elif tile == 5:
                items.append(Object2(x, y, screen, balgrootte1, WIT))
            elif tile == 7:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=yellow_green_gradient))
            elif tile == 8:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=etoue_30x30))
            elif tile == 9:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=greenbleu_30x30))
            elif tile == 18:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=etoue_30x30))
            elif tile == 19:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=resized_tile_0_4))

if maze2 == gebruikte_maze:
    start_positie_x_speler1, start_positie_y_speler1 = maze2_speler_startpositie_x, maze2_speler_startpositie_y

    start_positie_x_soort1, start_positie_y_soort1 = maze2_voorwerp1_startpositie_x, maze2_voorwerp1_startpositie_y
    start_positie_x_soort2, start_positie_y_soort2 = maze2_voorwerp2_startpositie_x, maze2_voorwerp2_startpositie_y
    start_positie_x_soort3, start_positie_y_soort3 = maze2_voorwerp3_startpositie_x, maze2_voorwerp3_startpositie_y
    start_positie_x_soort4, start_positie_y_soort4 = maze2_voorwerp4_startpositie_x, maze2_voorwerp4_startpositie_y

    for row_index, row in enumerate(gebruikte_maze):
        for col_index, tile in enumerate(row):
            x = col_index * muurgrootte
            y = row_index * muurgrootte
            if tile == 0:
                items.append(Object1(x, y, screen, balgrootte, WIT))
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=donkergroen))
            elif tile == 1:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=lichtgroen))
            elif tile == 2:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=corner_LB))
            elif tile == 3:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=corner_RB_copy))
            elif tile == 4:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=corner_RBOVEN_copy_2))
            elif tile == 7:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=separatie_boven))
            elif tile == 8:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=separatie))
            elif tile == 9:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=wite_lijn_L))
            elif tile == 5:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=wite_lijn_R))
            elif tile == 10:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=corner_LBOVEN))



#----------------------------------------------------------------------------------------------------------------------#

def check_collision2(speler, spook):
    # Maak een rechthoek voor de speler op basis van zijn positie en straal
    speler_rect = pygame.Rect(speler.x - speler.radius, speler.y - speler.radius, speler.radius * 2, speler.radius * 2)

    # Controleer of de speler's rechthoek botst met de rechthoek van het spook
    if speler_rect.colliderect(spook.rect):
        return True  # Als er een botsing is, retourneer True
    else:
        return False  # Als er geen botsing is, retourneer False

#----------------------------------------------------------------------------------------------------------------------#

# Klasse die de speler representeert en beweging/leven/overdracht regelt
class Speler:
    def __init__(self, x, y, scherm, kleur, radius, snelheid):
        self.x, self.y = x, y
        self.scherm = scherm
        self.kleur = kleur
        self.radius = radius
        self.snelheid = snelheid

        self.startpositie = (x, y)
        self.levens = 3
        self.punten = 0
        self.timer = None
        self.richting = None  # Toegevoegd: huidige richting ("UP", "DOWN", etc.)


    def draw(self):
        pygame.draw.circle(self.scherm, self.kleur, (self.x, self.y), self.radius)

    def move(self, snelheid_x, snelheid_y):
        nieuw_x, nieuw_y = self.x + snelheid_x , self.y + snelheid_y

        # Controleer of alle randen van de cirkel in lege ruimte zijn
        te_controleren_posities = [
            (nieuw_x + self.radius, nieuw_y + self.radius),
            (nieuw_x + self.radius, nieuw_y - self.radius),
            (nieuw_x - self.radius, nieuw_y + self.radius),
            (nieuw_x - self.radius, nieuw_y - self.radius)
        ]
        geldig = True
        for coordinaat_x, coordinaat_y in te_controleren_posities:
            if not maze_checker.is_valid(coordinaat_x, coordinaat_y):
                geldig = False
                break
        if geldig:
            self.x = nieuw_x
            self.y = nieuw_y

    def patrol(self):
        keys = pygame.key.get_pressed()

        # Update richting bij nieuwe toetsaanslagen
        if keys[pygame.K_DOWN]:
            self.richting = "DOWN"
        elif keys[pygame.K_UP]:
            self.richting = "UP"
        elif keys[pygame.K_LEFT]:
            self.richting = "LEFT"
        elif keys[pygame.K_RIGHT]:
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
        if (self.x, self.y) == zone1:
            self.x, self.y = zone2
        elif (self.x, self.y) == zone2:
            self.x, self.y = zone1

    def start_eetmodus(self):
        self.timer = time.time()  # Start de eet-modus

    def eetmodus_actief(self):
        if self.timer is None:
            return False
        if time.time() - self.timer <= tijd_van_bonus:  # 30 seconden duren
            return True
        else:
            self.timer = None  # Zet terug naar None als tijd voorbij is
            return False

    def check_collision(self, spook):
        speler_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        return speler_rect.colliderect(spook.rect)

    def eetspook(self, spook):
        if self.eetmodus_actief() and self.check_collision(spook):
            spook.reset()  # Verberg / reset het spook
            return 50  # Geef 50 punten
        return 0

#----------------------------------------------------------------------------------------------------------------------#

# A* algoritme om kortste pad te berekenen tussen start en doel

def a_star(maze, start, goal, tile_size):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    rows, cols = len(maze), len(maze[0])
    start_tile = (start[1] // tile_size, start[0] // tile_size)
    goal_tile = (goal[1] // tile_size, goal[0] // tile_size)

    frontier = [(0, start_tile)]
    came_from = {start_tile: None}
    cost_so_far = {start_tile: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal_tile:
            break

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = current[0] + dy, current[1] + dx
            if 0 <= nx < rows and 0 <= ny < cols and maze[int(nx)][int(ny)] in (0, 2, 4, 9): # welke vakjes de spook mag bewegen
                next_tile = (int(nx), int(ny))
                new_cost = cost_so_far[current] + 1
                if next_tile not in cost_so_far or new_cost < cost_so_far[next_tile]:
                    cost_so_far[next_tile] = new_cost
                    priority = new_cost + heuristic(goal_tile, next_tile)
                    heapq.heappush(frontier, (priority, next_tile))
                    came_from[next_tile] = current

    path = []
    current = goal_tile
    while current != start_tile:
        if current in came_from:
            path.append((current[1] * tile_size + tile_size//2, current[0] * tile_size + tile_size//2))
            current = came_from[current]
        else:
            return []
    path.reverse()
    return path

#----------------------------------------------------------------------------------------------------------------------#

# Klasse voor vijanden (spoken), met AI gedrag per type
class Spook:
    def __init__(self, x, y, scherm, afbeelding_pad, snelheid, type):
        self.x, self.y = x, y
        self.scherm = scherm
        self.snelheid = snelheid
        self.afbeelding = pygame.image.load(afbeelding_pad)
        self.afbeelding = pygame.transform.scale(self.afbeelding, (37, 37))
        self.rect = self.afbeelding.get_rect(center=(x, y))
        self.initial_state = (x, y)
        self.pad = []
        self.doel_index = 0
        self.type = type
        self.oorspronkelijke_type = type

    def draw(self):
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
        if self.doel_index >= len(self.pad):
            if self.type == "blinky":
                target = (speler.x, speler.y)
            elif self.type == "pinky":
                dx, dy = 0, 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]: dy = -4 * muurgrootte
                elif keys[pygame.K_DOWN]: dy = 4 * muurgrootte
                elif keys[pygame.K_LEFT]: dx = -4 * muurgrootte
                elif keys[pygame.K_RIGHT]: dx = 4 * muurgrootte
                target = (speler.x + dx, speler.y + dy)
            elif self.type == "inky":
                dx, dy = 0, 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]: dy = -2 * muurgrootte
                elif keys[pygame.K_DOWN]: dy = 2 * muurgrootte
                elif keys[pygame.K_LEFT]: dx = -2 * muurgrootte
                elif keys[pygame.K_RIGHT]: dx = 2 * muurgrootte
                projected = (speler.x + dx, speler.y + dy)
                if extra_speler:
                    vx = projected[0] - extra_speler.x
                    vy = projected[1] - extra_speler.y
                    target = (extra_speler.x + 2 * vx, extra_speler.y + 2 * vy)
                else:
                    target = projected
            elif self.type == "clyde":
                afstand = ((self.x - speler.x)**2 + (self.y - speler.y)**2)**0.5
                if afstand > 160:
                    target = (speler.x, speler.y)
                else:
                    target = (1 * muurgrootte, 17 * muurgrootte)
            else:
                target = (speler.x, speler.y)
            self.pad = a_star(gebruikte_maze, (self.x, self.y), target, muurgrootte)
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


#----------------------------------------------------------------------------------------------------------------------#

# Checkt of speler en spook: leeuwen etc voila botsen met elkaar
def check_collision(speler, spook):
    speler_rect = pygame.Rect(speler.x - speler.radius, speler.y - speler.radius , speler.radius-5, speler.radius+5)
    return speler_rect.colliderect(spook.rect)


# Teken hartjes linksboven misschien later voor elk niveau iets anders
def toon_levens(screen, levens):
    hart_afbeelding = pygame.image.load("vijanden_savanne/hart1.png")
    hart_afbeelding = pygame.transform.scale(hart_afbeelding, (25, 25))
    for i in range(levens):
        screen.blit(hart_afbeelding, (10 + i * 35, 10))

def herstart_spel(speler, spoken):
    speler.levens -= 1
    speler.reset()
    for spook in spoken:
        spook.reset()
        spook.pad = []         #  Leeg het oude pad
        spook.doel_index = 0   #  Zet index terug op 0 zodat hij direct herberekent
    pygame.time.delay(1000)

#----------------------------------------------------------------------------------------------------------------------#

# Spelers & Spoken aanmaken
speler = Speler(start_positie_x_speler1 , start_positie_y_speler1, screen, WIT, radius_speler, snelheid_speler)
leeuw = Spook(start_positie_x_soort1, start_positie_y_soort1 , screen, "vijanden_savanne/leeuw1.png", snelheid_monster, "pinky")
olifant = Spook(start_positie_x_soort2, start_positie_y_soort2 , screen, "vijanden_savanne/olifant1.png", snelheid_monster, "blinky")
neushoorn = Spook(start_positie_x_soort3, start_positie_y_soort3 , screen, "vijanden_savanne/neushoorn1.png", snelheid_monster, "inky")
gier = Spook(start_positie_x_soort4, start_positie_y_soort4 , screen, "vijanden_savanne/gier.png", snelheid_monster, "clyde")
list_of_objects = [speler, leeuw, olifant, neushoorn, gier]
list_of_monsters = [leeuw, olifant, neushoorn, gier]

#----------------------------------------------------------------------------------------------------------------------#

# Game-loop
running = True
while running:
    tijd.tick(fps)
    screen.fill(ZWART)

    for wall in walls:
        wall.draw()

    for obj in list_of_objects:
        obj.draw()
        if isinstance(obj, Spook):
            obj.patrol(speler, olifant)
        else:
            obj.patrol()
        obj.overdracht()

    # 1. Normale items pakken
    for item in items[:]:
        if item.botsing(speler):
            items.remove(item)
            speler.punten += item.punten()

    # 2. Speciale items pakken om eetmodus te starten
    for item in items2[:]:
        if item.botsing(speler):
            items2.remove(item)
            speler.start_eetmodus()

            # Zet alle spoken tijdelijk in "vlucht" modus
            for spook in list_of_monsters:
                spook.verander_type("clyde")

    # 3. Spoken checken
    for spook in list_of_monsters:
        if speler.check_collision(spook):
            if speler.eetmodus_actief():
                speler.punten += speler.eetspook(spook)  # alleen eet als eetmodus actief
            else:
                speler.levens -= 1
                speler.reset()
                for spook in list_of_monsters:
                    spook.reset()
                pygame.time.delay(500)

    # 4. Check na botsing of eetmodus voorbij is
    if not speler.eetmodus_actief():
        for spook in list_of_monsters:
            spook.verander_type(spook.oorspronkelijk_type)  # Zet type terug


    toon_levens(screen, speler.levens)

    if speler.levens <= 0:
        font = pygame.font.SysFont(None, 75)
        tekst = font.render("Game Over", True, ROOD)
        screen.blit(tekst, (breedte // 2 - 150, hoogte // 2 - 40))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Muren tekenen
    for wall in walls:
        wall.draw()

    # Items tekenen
    for item in items:
        item.draw()

    # --> HIER score tonen
    score_text = font.render(f"Score: {speler.punten}", True, (255, 255, 255))  # Witte tekst
    screen.blit(score_text, (10, 580))  # Zet de tekst linksboven op (10,10)

    pygame.display.flip()

pygame.quit()