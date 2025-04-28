# Import and initialize the pygame library
import pygame
import heapq

# Initialisatie
pygame.init()

# Scherminstellingen
breedte = int(870)
hoogte = int(570)
screen = pygame.display.set_mode([breedte, hoogte])

# Kleuren
WIT = (255, 255, 255)
BLAUW = (0, 0, 128)
BLACK = (0, 0, 0)
ROOD = (255, 0, 0)
GROEN = (0, 255, 0)
GEEL = (255, 255, 0)
ZWART = (0, 0, 0)

# Tijd
time = pygame.time.Clock()
fps = 30

# Grootte van muur en rand
muurgrootte = 30
balgrootte = 5
balgrootte1 = 9

# Overdrachtszones
zone1 = (45, 225)
zone2 = (825, 465)

#zone1 = (45, 225)
#zone1 = (45, 225)

#zone1 = (45, 225)
#zone1 = (45, 225)





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

# Maze laden
def maze_van_bestand(bestand):
    document = []
    file = open(bestand, 'r')
    for lijn in file:
        lijn = lijn.strip().split()
        lijn = [int(cijfer) for cijfer in lijn]
        document.append(lijn)
    file.close()
    return document

maze = maze_van_bestand("maze3.txt")

# Muur Klasse
class Muur:
    def __init__(self, x, y, size, kleur=None, afbeelding=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.kleur = kleur
        self.afbeelding = afbeelding

    def draw(self, surface):
        if self.afbeelding:
            surface.blit(self.afbeelding, self.rect)
        else:
            pygame.draw.rect(surface, self.kleur, self.rect)

# Object Klassen
class Object1:
    def __init__(self,x, y, afmeting, kleur, scherm, type):
        self.x = x
        self.y = y
        self.afmeting = afmeting
        self.kleur = kleur
        self.scherm = scherm
        self.type = type
        self.center = (x + muurgrootte // 2, y + muurgrootte // 2)
        self.radius = afmeting // 2

    def draw(self):
        pygame.draw.circle(self.scherm, self.kleur, self.center, self.radius)

    def botsing(self, speler):
        spelerx1 = speler.x - speler.radius
        spelerx2 = speler.x + speler.radius
        spelery1 = speler.y - speler.radius
        spelery2 = speler.y + speler.radius
        x1 = self.x
        x2 = self.x + self.afmeting
        y1 = self.y
        y2 = self.y + self.afmeting
        if spelerx2 > x1 and spelerx1 < x2 and spelery2 > y1 and spelery1 < y2:
            return True
        return False

class Object2(Object1):
    pass

# Muur + weg
img_wall0 = pygame.transform.scale(pygame.image.load("Savanne_decor/way_30x30.jpeg"), (30, 30))
img_wall1 = pygame.transform.scale(pygame.image.load("Savanne_decor/Muur_savanne.png"), (30, 30))
img_valsmuur = pygame.transform.scale(pygame.image.load("Savanne_decor/Muur_savanne.png"), (30, 30))

bush = pygame.transform.scale(pygame.image.load("struik/bush.png"), (30, 30))


#rivier
img_riverend = pygame.transform.scale(pygame.image.load("Savanne_decor/einde_rivier.jpeg") , (30, 30))
img_river = pygame.transform.scale(pygame.image.load("Savanne_decor/rerivier.jpeg"), (30, 30))
bovengroen = pygame.transform.scale(pygame.image.load("Savanne_decor/bovengroen.jpeg"), (30, 30))
rechtsgroen = pygame.transform.scale(pygame.image.load("Savanne_decor/rechtsgroen.jpeg"), (30, 30))

RIVHOR = pygame.transform.scale(pygame.image.load("Rivier/RIVHOR.jpeg") , (30, 30))
RIVMID = pygame.transform.scale(pygame.image.load("Rivier/RIVMID.jpeg"), (30, 30))
RIVBOV = pygame.transform.scale(pygame.image.load("Rivier/RIVBOV.jpeg"), (30, 30))
RIVOND = pygame.transform.scale(pygame.image.load("Rivier/RIVOND.jpeg"), (30, 30))

greenbleu_30x30 = pygame.transform.scale(pygame.image.load("Rivier/greenbleu_30x30.jpg"), (30, 30))

etoue_30x30 = pygame.transform.scale(pygame.image.load("struik/etoue_30x30.jpg"), (30, 30))

yellow_green_gradient = pygame.transform.scale(pygame.image.load("Rivier/yellow_green_gradient.png"), (30, 30))

#leeuw
img_BL = pygame.transform.scale(pygame.image.load("Leeuw/BOTTOMLEFT.png"), (30, 30))
img_BR = pygame.transform.scale(pygame.image.load("Leeuw/BOTTOMRIGHT.png") , (30, 30))
img_BOL = pygame.transform.scale(pygame.image.load("Leeuw/TOPLEFT.png") , (30, 30))
img_BOR = pygame.transform.scale(pygame.image.load("Leeuw/TOPRIGHT.png"), (30, 30))

#olifant
resized_tile_0_0 = pygame.transform.scale(pygame.image.load("struik/resized_tile_0_0.png"), (30, 30))
resized_tile_0_1 = pygame.transform.scale(pygame.image.load("struik/resized_tile_0_1.png") , (30, 30))
resized_tile_0_2 = pygame.transform.scale(pygame.image.load("struik/resized_tile_0_2.png") , (30, 30))
resized_tile_0_3 = pygame.transform.scale(pygame.image.load("struik/resized_tile_0_3.png"), (30, 30))
resized_tile_0_4 = pygame.transform.scale(pygame.image.load("struik/resized_tile_0_4 (1).png"), (30, 30))
resized_tile_1_0 = pygame.transform.scale(pygame.image.load("struik/resized_tile_1_0.png") , (30, 30))
resized_tile_1_1 = pygame.transform.scale(pygame.image.load("struik/resized_tile_1_1.png") , (30, 30))
resized_tile_1_2 = pygame.transform.scale(pygame.image.load("struik/resized_tile_1_2.png"), (30, 30))
resized_tile_1_3 = pygame.transform.scale(pygame.image.load("struik/resized_tile_1_3 .png"), (30, 30))
resized_tile_1_4 = pygame.transform.scale(pygame.image.load("struik/resized_tile_1_4.png") , (30, 30))
resized_tile_2_0 = pygame.transform.scale(pygame.image.load("struik/resized_tile_2_0.png") , (30, 30))
resized_tile_2_1 = pygame.transform.scale(pygame.image.load("struik/resized_tile_2_1.png"), (30, 30))
resized_tile_2_2 = pygame.transform.scale(pygame.image.load("struik/resized_tile_2_2.png"), (30, 30))
resized_tile_2_3 = pygame.transform.scale(pygame.image.load("struik/resized_tile_2_3.png") , (30, 30))
resized_tile_2_4 = pygame.transform.scale(pygame.image.load("struik/resized_tile_2_4.png") , (30, 30))

#olifant

resized_elephant_tile_0_0 = pygame.transform.scale(pygame.image.load("olifant/resized_elephant_tile_0_0.png") , (30, 30))
resized_elephant_tile_0_1 = pygame.transform.scale(pygame.image.load("olifant/resized_elephant_tile_0_1.png"), (30, 30))
resized_elephant_tile_0_2 = pygame.transform.scale(pygame.image.load("olifant/resized_elephant_tile_0_2.png"), (30, 30))
resized_elephant_tile_1_0 = pygame.transform.scale(pygame.image.load("olifant/resized_elephant_tile_1_0.png") , (30, 30))
resized_elephant_tile_1_1 = pygame.transform.scale(pygame.image.load("olifant/resized_elephant_tile_1_1.png") , (30, 30))
resized_elephant_tile_1_2 = pygame.transform.scale(pygame.image.load("olifant/resized_elephant_tile_1_2.png"), (30, 30))
resized_elephant_tile_2_0 = pygame.transform.scale(pygame.image.load("olifant/resized_elephant_tile_2_0.png"), (30, 30))
resized_elephant_tile_2_1 = pygame.transform.scale(pygame.image.load("olifant/resized_elephant_tile_2_1.png") , (30, 30))
resized_elephant_tile_2_2 = pygame.transform.scale(pygame.image.load("olifant/resized_elephant_tile_2_2.png") , (30, 30))

walls = []

for row_index, row in enumerate(maze):
    for col_index, tile in enumerate(row):
        x = col_index * muurgrootte
        y = row_index * muurgrootte
        if tile == 1:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_0_4))
        elif tile == 2:
            walls.append(Muur(x, y, muurgrootte, kleur=ROOD))
        elif tile == 3:
            walls.append(Muur(x, y, muurgrootte, kleur=GEEL))
        elif tile == 4:
            walls.append(Muur(x, y, muurgrootte, kleur=GEEL))
        elif tile == 6:
            walls.append(Muur(x, y, muurgrootte, afbeelding=img_BR))
        elif tile == 7:
            walls.append(Muur(x, y, muurgrootte, afbeelding=img_BL))
        elif tile == 8:
            walls.append(Muur(x, y, muurgrootte, afbeelding=img_BOL))
        elif tile == 9:
            walls.append(Muur(x, y, muurgrootte, afbeelding=greenbleu_30x30))
        elif tile == 18:
            walls.append(Muur(x, y, muurgrootte, afbeelding=img_riverend))
        elif tile == 1111:
            walls.append(Muur(x, y, muurgrootte, afbeelding=img_river))
        elif tile == 0:
            walls.append(Muur(x, y, muurgrootte, afbeelding=img_wall0))
        elif tile == 19:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_0_4))

        elif tile == 30:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_0_0))
        elif tile == 31:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_0_1))
        elif tile == 32:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_0_2))
        elif tile == 33:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_0_3))
        elif tile == 34:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_0_4))
        elif tile == 10:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_1_0))
        elif tile == 11:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_1_1))
        elif tile == 12:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_1_2))
        elif tile == 13:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_1_3))
        elif tile == 14:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_1_4))
        elif tile == 20:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_2_0))
        elif tile == 21:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_2_1))
        elif tile == 22:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_2_2))
        elif tile == 23:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_2_3))
        elif tile == 24:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_2_4))

        elif tile == 28:
            walls.append(Muur(x, y, muurgrootte, afbeelding=bush))

# olifant
        elif tile == 40:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_elephant_tile_0_0))
        elif tile == 41:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_elephant_tile_0_1))
        elif tile == 42:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_elephant_tile_0_2))
        elif tile == 43:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_elephant_tile_1_0))
        elif tile == 44:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_elephant_tile_1_1))
        elif tile == 45:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_elephant_tile_1_2))
        elif tile == 46:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_elephant_tile_2_0))
        elif tile == 47:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_elephant_tile_2_1))
        elif tile == 48:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_elephant_tile_2_2))
#rivier
        elif tile == 89:
            walls.append(Muur(x, y, muurgrootte, afbeelding=img_river))
        elif tile == 85:
            walls.append(Muur(x, y, muurgrootte, afbeelding=img_riverend))
        elif tile == 86:
            walls.append(Muur(x, y, muurgrootte, afbeelding=bovengroen))
        elif tile == 87:
            walls.append(Muur(x, y, muurgrootte, afbeelding=rechtsgroen))

        elif tile == 51:
            walls.append(Muur(x, y, muurgrootte, afbeelding=RIVHOR))
        elif tile == 52:
            walls.append(Muur(x, y, muurgrootte, afbeelding=RIVMID))
        elif tile == 53:
            walls.append(Muur(x, y, muurgrootte, afbeelding=RIVBOV))
        elif tile == 54:
            walls.append(Muur(x, y, muurgrootte, afbeelding=RIVOND))
# Walls en Items vullen
walls = []
items = []

for row_index, row in enumerate(maze):
    for col_index, tile in enumerate(row):
        x = col_index * muurgrootte
        y = row_index * muurgrootte
        if tile == 0:
            items.append(Object1(x, y, balgrootte, WIT, screen, type=1))
            walls.append(Muur(x, y, muurgrootte, afbeelding=img_wall0))
        elif tile == 1:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_0_4))
        elif tile == 2:
            walls.append(Muur(x, y, muurgrootte, kleur=ROOD))
        elif tile == 3:
            walls.append(Muur(x, y, muurgrootte, kleur=GEEL))
        elif tile == 4:
            walls.append(Muur(x, y, muurgrootte, kleur=GROEN))
        elif tile == 5:
            items.append(Object2(x, y, balgrootte1, WIT, screen, type=2))
            walls.append(Muur(x, y, muurgrootte, afbeelding=img_wall0))
        elif tile == 6:
            walls.append(Muur(x, y, muurgrootte, afbeelding=img_BR))
        elif tile == 7:
            walls.append(Muur(x, y, muurgrootte, afbeelding=yellow_green_gradient))
        elif tile == 8:
            walls.append(Muur(x, y, muurgrootte, afbeelding=etoue_30x30))
        elif tile == 9:
            walls.append(Muur(x, y, muurgrootte, afbeelding=greenbleu_30x30))
        elif tile == 18:
            walls.append(Muur(x, y, muurgrootte, afbeelding=etoue_30x30))
        elif tile == 19:
            walls.append(Muur(x, y, muurgrootte, afbeelding=resized_tile_0_4))
        elif tile == 28:
            walls.append(Muur(x, y, muurgrootte, afbeelding=bush))


class MazeChecker:
    def __init__(self, maze, tile_size):
        self.maze = maze
        self.tile_size = tile_size

    def is_valid(self, x, y):
        kol = x // self.tile_size
        rij = y // self.tile_size
        if maze[rij][kol] == 0 or maze[rij][kol] == 4 or maze[rij][kol] == 5 or maze[rij][kol] == 9 or maze[rij][kol] == 18 or maze[rij][kol] == 53 or maze[rij][kol] == 54 or maze[rij][kol] == 19:
            return True
        return False

maze_checker = MazeChecker(maze, muurgrootte)

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
            if 0 <= nx < rows and 0 <= ny < cols and maze[int(nx)][int(ny)] in (0, 2, 4):
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

# Klasse die de speler representeert en beweging/leven/overdracht regelt
class Speler:
    def __init__(self, x, y, kleur, radius, snelheid):
        self.x, self.y = x, y
        self.kleur = kleur
        self.radius = radius
        self.snelheid = snelheid
        self.initial_state = (x, y)
        self.levens = 3

    def draw(self, screen):
        pygame.draw.circle(screen, self.kleur, (self.x, self.y), self.radius)

    def move(self, dx, dy):
        nieuw_x, nieuw_y = self.x + dx, self.y + dy
        te_controleren = [
            (nieuw_x + self.radius, nieuw_y + self.radius),
            (nieuw_x + self.radius, nieuw_y - self.radius),
            (nieuw_x - self.radius, nieuw_y + self.radius),
            (nieuw_x - self.radius, nieuw_y - self.radius)
        ]
        if all(maze_checker.is_valid(x, y) for x, y in te_controleren):
            self.x, self.y = nieuw_x, nieuw_y

    def patrol(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:  self.move(0, self.snelheid)
        if keys[pygame.K_UP]:    self.move(0, -self.snelheid)
        if keys[pygame.K_LEFT]:  self.move(-self.snelheid, 0)
        if keys[pygame.K_RIGHT]: self.move(self.snelheid, 0)

    def reset(self):
        self.x, self.y = self.initial_state

    def overdracht(self):
        if (self.x, self.y) == zone1:
            self.x, self.y = zone2
        elif (self.x, self.y) == zone2:
            self.x, self.y = zone1

# Klasse voor vijanden (spoken), met AI gedrag per type
class Spook:
    def __init__(self, x, y, afbeelding_pad, snelheid, type):
        self.x, self.y = x, y
        self.snelheid = snelheid
        self.afbeelding = pygame.image.load(afbeelding_pad)
        self.afbeelding = pygame.transform.scale(self.afbeelding, (37, 37))
        self.rect = self.afbeelding.get_rect(center=(x, y))
        self.initial_state = (x, y)
        self.pad = []
        self.doel_index = 0
        self.type = type

    def draw(self, screen):
        self.rect.center = (self.x, self.y)
        screen.blit(self.afbeelding, self.rect)

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
            self.pad = a_star(maze, (self.x, self.y), target, muurgrootte)
            self.doel_index = 0
        self.volg_pad()

    def reset(self):
        self.x, self.y = self.initial_state
        self.pad = []  # ❗ Leeg pad bij reset
        self.doel_index = 0  # ❗ Zorg dat hij bij volgende patrol direct een nieuw pad berekent

    def overdracht(self):
        if (self.x, self.y) == zone1:
            self.x, self.y = zone2
        elif (self.x, self.y) == zone2:
            self.x, self.y = zone1

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
        spook.pad = []         # 👈 Leeg het oude pad
        spook.doel_index = 0   # 👈 Zet index terug op 0 zodat hij direct herberekent
    pygame.time.delay(1000)

# Spelers & Spoken aanmaken
speler = Speler(435, 285, WIT, 14, 5)
leeuw = Spook(1 * muurgrootte + 15, 1 * muurgrootte + 15, "vijanden_savanne/leeuw1.png", 4, "pinky")
olifant = Spook(27 * muurgrootte + 15, 1 * muurgrootte + 15 , "vijanden_savanne/olifant1.png", 4, "blinky")
neushoorn = Spook(1 * muurgrootte + 15, 10 * muurgrootte + 15, "vijanden_savanne/neushoorn1.png", 4, "inky")
gier = Spook(27 * muurgrootte + 15, 10 * muurgrootte + 15, "vijanden_savanne/gier.png", 4, "clyde")
list_of_objects = [speler, leeuw, olifant, neushoorn, gier]

# Game-loop
running = True
while running:
    time.tick(fps)
    screen.fill(ZWART)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    for wall in walls:
        wall.draw(screen)

    for item in items:
        item.draw()

    for obj in list_of_objects:
        obj.draw(screen)
        if isinstance(obj, Spook):
            obj.patrol(speler, olifant)
        else:
            obj.patrol()
        obj.overdracht()

    for item in items[:]:
        if item.botsing(speler):
            items.remove(item)

    if any(check_collision(speler, spook) for spook in [leeuw, olifant, neushoorn, gier]):
        speler.levens -= 1
        speler.reset()
        for spook in [leeuw, olifant, neushoorn, gier]:
            spook.reset()
        pygame.time.delay(500)

    toon_levens(screen, speler.levens)

    if speler.levens <= 0:
        font = pygame.font.SysFont(None, 75)
        tekst = font.render("Game Over", True, ROOD)
        screen.blit(tekst, (breedte // 2 - 150, hoogte // 2 - 40))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

pygame.quit()
