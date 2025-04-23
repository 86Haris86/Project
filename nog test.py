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

# Overdrachtszones
zone1 = (435, 95)
zone2 = (435, 385)

#menu
# Toont het hoofdmenu met achtergrond en startknop

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

# Eerst menu tonen
toon_menu()



# Maze inladen
# Leest maze-data uit een tekstbestand en zet het om naar een lijst van lijsten

def maze_van_bestand(bestand):
    document = []
    file = open(bestand, 'r')
    for lijn in file:
        lijn = lijn.strip().split()
        lijn = [int(cijfer) for cijfer in lijn]
        document.append(lijn)
    file.close()
    return document
maze = maze_van_bestand("maze.txt")

# Muren
# Representatie van een muur-tegel in de maze

class Muur:
    def __init__(self, x, y, size, kleur):
        self.rect = pygame.Rect(x, y, size, size)
        self.kleur = kleur

    def draw(self, surface):
        pygame.draw.rect(surface, self.kleur, self.rect)

# Maze muren genereren
from PIL import Image
import random

# Laad de muur-afbeeldingen
img_wall_1 = Image.open("Savanne_decor/Muur_savanne.png").resize((32, 32))
img_wall_2 = Image.open("Savanne_decor/Rivier.png").resize((32, 32))
img_wall_3 = Image.open("Savanne_decor/Rivier_met_steen.png").resize((32, 32))

# Laad de pad-afbeelding
img_path = Image.open("Savanne_decor/weg_savanne.png").resize((32, 32))

# Verzamel de muur-afbeeldingen in een lijst
wall_images = [img_wall_1, img_wall_2, img_wall_3]

# Lees het maze-bestand
with open("maze.txt", "r") as f:
    maze = [[int(n) for n in line.strip().split()] for line in f]

rows = len(maze)
cols = len(maze[0])
tile_size = 32

# Maak de eindafbeelding
scrn = pygame.display.set_mode((30, 30))
img1 = pygame.image.load("Savanne_decor/weg_savanne.png").convert()
# Vul het maze met de juiste afbeelding
for y in range(rows):
    for x in range(cols):
        value = maze[y][x]
        if value == 1:
            tile = random.choice(wall_images)
        else:
            tile = img_path

# Toon het resultaat
walls = []
for row_index, row in enumerate(maze):
    for col_index, tile in enumerate(row):
        if tile != 0:
            x = col_index * muurgrootte
            y = row_index * muurgrootte
            kleur = img1 if tile == 1 else ROOD if tile == 2 else GEEL if tile == 3 else ZWART
            walls.append(Muur(x, y, muurgrootte, kleur))

# Controleert of een positie geldig is (dus geen muur)

class MazeChecker:
    def __init__(self, maze, tile_size):
        self.maze = maze
        self.tile_size = tile_size

    def is_valid(self, x, y):
        kol = x // self.tile_size
        rij = y // self.tile_size
        if maze[rij][kol] == 0 or maze[rij][kol] == 4:
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
    speler_rect = pygame.Rect(speler.x - speler.radius, speler.y - speler.radius, speler.radius*2, speler.radius*2)
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


speler  = Speler(435, 405, WIT, 14, 5)
leeuw = Spook(13 * muurgrootte + 15, 9 * muurgrootte + 15, "vijanden_savanne/leeuw1.png", 0, "pinky")
olifant = Spook(13 * muurgrootte + 15, 10 * muurgrootte , "vijanden_savanne/olifant1.png", 0, "blinky")
neushoorn = Spook(15 * muurgrootte + 15, 9 * muurgrootte + 15, "vijanden_savanne/neushoorn1.png", 0, "inky")
gier = Spook(15 * muurgrootte + 15, 10 * muurgrootte , "vijanden_savanne/gier.png", 0, "clyde")
list_of_objects = [speler, leeuw, olifant, neushoorn, gier]

running = True
while running:
    time.tick(fps)
    screen.fill(ZWART)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    for wall in walls:
        wall.draw(screen)

    for obj in list_of_objects:
        obj.draw(screen)
        if isinstance(obj, Spook):
            obj.patrol(speler, olifant)
        else:
            obj.patrol()
        obj.overdracht()

    if any(check_collision(speler, spook) for spook in [leeuw, olifant, neushoorn, gier]):
        speler.levens -= 1
        speler.reset()
        for spook in [leeuw, olifant, neushoorn, gier]: spook.reset()
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
