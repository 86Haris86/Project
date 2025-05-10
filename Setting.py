# Import
import pygame
import heapq
import random

from Plan_object import Object1 , Object2 , Muur , Snelheidsobject
from Hulpfuncties import maze_van_bestand , MazeChecker
from Afbeeldingen import way_30x30 , greenbleu_30x30  , etoue_30x30  , yellow_green_gradient , resized_tile_0_4 , speed_img
from Afbeeldingen import donkergroen , lichtgroen , wite_lijn_L , cornerbasdroit , cornerbasgauche ,cornerhautdroit ,cornerhautgauche ,ligenhaut ,lignebas ,lignedroit , lignegauche , pase , pase2 , pessa , pessa2 , sepabas , sepahaut
from Afbeeldingen import crocoo1 , gier1 , hippo1 , leeuw1 , neushoorn1 , olifant1
#from Afbeeldingen import ronaldo , messi , neymar , lukaku


#----------------------------------------------------------------------------------------------------------------------#

# scherm groter maken met 'a' om de score bij te schrijven
a = 50
font = pygame.font.SysFont(None, 36)
tekst_punten_x = 10
tekst_punten_y = 580
tekst_tijd_x = 200
tekst_tijd_y = 580

# Scherminstellingen
breedte = int(870)
hoogte = int(570 + a)
screen = pygame.display.set_mode([breedte, hoogte])
#screen = pygame.display.set_mode([breedte, hoogte], pygame.FULLSCREEN)

#----------------------------------------------------------------------------------------------------------------------#

# Tijd
tijd = pygame.time.Clock()
fps = 30
tijd_van_bonus = 10

#----------------------------------------------------------------------------------------------------------------------#

# Kleuren
WIT = (255, 255, 255)
BLAUW = (0, 0, 128)
ROOD = (255, 0, 0)
GROEN = (0, 255, 0)
GEEL = (255, 255, 0)
ZWART = (0, 0, 0)
BRUIN = (138,102,66)
GRIJS = (128,128,128)
#----------------------------------------------------------------------------------------------------------------------#

# Grootte van muur en rand
muurgrootte = 30
balgrootte = 4
balgrootte1 = 8
refactor = 1  # zodat de bal niet bij x(bal) = x(item) verdwijnt maar een beetje later

# cijfer zodat botsing later is
interval = 5



# Setting.py
#class SETTINGS:
 #   def __init__(self):
  #      # Sequence of maze files
   #     self.MAZE_SEQUENCE = ["maze1.txt", "maze2.txt", "maze3.txt"]
    #    # Starting positions for player per maze: (row, col)
     #   self.START_POS = [ (0, 0), (0, 0), (0, 0) ]  # pas aan volgens jouw tekstbestanden
      #  # Starting positions for enemy per maze
       ### Time before switching maze (in seconds)
        #self.SWITCH_INTERVAL = 120
        ### Tile index that determines win
        #self.WIN_TILE = 99
#----------------------------------------------------------------------------------------------------------------------#

# Verschillende maze
maze1 = maze_van_bestand("maze1.txt")
maze2 = maze_van_bestand("maze2.txt")
maze3 = maze_van_bestand("maze3.txt")

# maze dat wordt gebruikt bij het runnen
gebruikte_maze = maze3

# Mazechecer
maze_checker = MazeChecker(gebruikte_maze, muurgrootte)

#----------------------------------------------------------------------------------------------------------------------#

# Walls en Items vullen
walls = []
items = []
items2 = []

#----------------------------------------------------------------------------------------------------------------------#



if maze1 == gebruikte_maze :
    # Waar de speler mag bewegen in de maze
    toegelaten_posities_speler = [0,3,4,5]
    # Waar de vijand mag bewegen in de maze
    toegelaten_posities_vijand = [0,2,3,4,5]
    deur_van_spoken = 2
    # speler
    start_positie_x_speler1, start_positie_y_speler1 = 14 * muurgrootte + muurgrootte//2, 12 * muurgrootte + muurgrootte//2
    # vijanden
    start_positie_x_soort1, start_positie_y_soort1 = 12 * muurgrootte + muurgrootte//2 + 1 * muurgrootte//5, 10 * muurgrootte + muurgrootte//2
    start_positie_x_soort2, start_positie_y_soort2 = 13 * muurgrootte + muurgrootte//2 + 2 * muurgrootte//5, 10 * muurgrootte + muurgrootte//2
    start_positie_x_soort3, start_positie_y_soort3 = 14 * muurgrootte + muurgrootte//2 + 3 * muurgrootte//5, 10 * muurgrootte + muurgrootte//2
    start_positie_x_soort4, start_positie_y_soort4 = 15 * muurgrootte + muurgrootte//2 + 4 * muurgrootte//5, 10 * muurgrootte + muurgrootte//2
    start_positie_x_soort5, start_positie_y_soort5 = None , None
    start_positie_x_soort6, start_positie_y_soort6 = None , None
    # Overdrachtszones
    zone1 ,zone2 = (1 * muurgrootte, 9 * muurgrootte + muurgrootte//2), (28 * muurgrootte, 9 * muurgrootte + muurgrootte//2)
    # startzone
    startzone_tegel = (start_positie_x_speler1, start_positie_y_speler1)
    eindzone_x = start_positie_x_speler1 - muurgrootte // 2
    eindzone_y = start_positie_y_speler1 - muurgrootte // 2
    # activatie van croco en hippo (Flags)
    leeuw_active = True
    olifant_active = True
    neushoorn_active = True
    gier_active = True
    croco_active = False
    hippo_active = False
    # afbeeldingen vijanden
    soort1 = leeuw1
    soort2 = olifant1
    soort3 = neushoorn1
    soort4 = gier1
    soort5 = crocoo1
    soort6 = hippo1

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
                items2.append(Object2(x, y, screen, balgrootte1, WIT))
            elif tile == 4:
                walls.append(Muur(x, y, screen, muurgrootte, GROEN))

    # Zoek alle lege tegels (waarde 0) in het doolhof
    lege_plekken = [(j * muurgrootte, i * muurgrootte) for i, rij in enumerate(maze1) for j, waarde in enumerate(rij) if waarde == 0]

    # Kies willekeurig een positie voor het snelheidsobject
    x_positie, y_positie = random.choice(lege_plekken)

    # Maak het snelheidsobject aan (je kan hier een afbeelding toevoegen later)
    snelheids_object = Snelheidsobject(x_positie, y_positie, screen , muurgrootte,afbeelding=speed_img)


# 1 : muur
# 2 : muur spoken
# 0 : object
# 3 : object2
# 4 : overgang
# 5 : niets


#----------------------------------------------------------------------------------------------------------------------#

# Maze2

if maze2 == gebruikte_maze:
    # Waar de speler mag bewegen in de maze
    toegelaten_posities_speler = [0, 2, 3, 4, 10, 12, 18, 19, 20, 21, 22, 23, 25, 26]
    # Waar de vijand mag bewegen in de maze
    toegelaten_posities_vijand = [0, 2, 3, 4, 10, 12, 18, 19, 20, 21, 22, 23, 25, 26]
    deur_van_spoken = []
    # speler
    start_positie_x_speler1, start_positie_y_speler1 = 430,285
    #start_positie_x_speler1, start_positie_y_speler1 = 14 * muurgrootte + muurgrootte // 2, 9 * muurgrootte + muurgrootte // 2
    # vijanden
    start_positie_x_soort1, start_positie_y_soort1 = 1 * muurgrootte + 15, 1 * muurgrootte + 15
    start_positie_x_soort2, start_positie_y_soort2 = 18 * muurgrootte + 15, 1 * muurgrootte + 15
    start_positie_x_soort3, start_positie_y_soort3 = 1 * muurgrootte + 15, 18 * muurgrootte + 15
    start_positie_x_soort4, start_positie_y_soort4 = 18 * muurgrootte + 15, 18 * muurgrootte + 15
    start_positie_x_soort5, start_positie_y_soort5 = None, None
    start_positie_x_soort6, start_positie_y_soort6 = None, None
    # Overdrachtszones
    zone1, zone2 = None , None
    # startzone
    startzone_tegel = (start_positie_x_speler1, start_positie_y_speler1)
    eindzone_x = start_positie_x_speler1 - muurgrootte // 2
    eindzone_y = start_positie_y_speler1 - muurgrootte // 2
    # activatie van croco en hippo (Flags)
    leeuw_active = True
    olifant_active = True
    neushoorn_active = True
    gier_active = True
    croco_active = False
    hippo_active = False
    # afbeeldingen vijanden
    soort1 = leeuw1
    soort2 = olifant1
    soort3 = neushoorn1
    soort4 = gier1
    soort5 = crocoo1
    soort6 = hippo1
    # afbeeldingen vijanden
    #soort1 = ronaldo
    #soort2 = messi
    #soort3 = neymar
    #soort4 = lukaku
    #soort5 = crocoo1
    #soort6 = hippo1

    for row_index, row in enumerate(gebruikte_maze):
        for col_index, tile in enumerate(row):
            x = col_index * muurgrootte
            y = row_index * muurgrootte
            if tile == 0:
                items.append(Object1(x, y, screen, balgrootte, WIT))
                walls.append(Muur(x, y,screen, muurgrootte, afbeelding=donkergroen))
            elif tile == 1:
                walls.append(Muur(x, y,screen, muurgrootte, afbeelding=lichtgroen))
            elif tile == 2:
                walls.append(Muur(x, y,screen, muurgrootte, afbeelding=cornerbasgauche))
            elif tile == 3:
                walls.append(Muur(x, y,screen, muurgrootte, afbeelding=cornerbasdroit))
            elif tile == 4:
                walls.append(Muur(x, y,screen, muurgrootte, afbeelding=cornerhautdroit))
            elif tile == 5:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=lignebas))
            elif tile == 6:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=ligenhaut))
            elif tile == 7:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=sepahaut))
            elif tile == 8:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=sepabas))
            elif tile == 9:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=lignegauche))
            elif tile == 10:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=cornerhautgauche))
            elif tile == 12:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=wite_lijn_L))
            elif tile == 13:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=lignedroit))
            elif tile == 20:
                walls.append(Muur(x, y, screen, muurgrootte, kleur=WIT))
            elif tile == 18:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=pase))
            elif tile == 19:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=pase2))
            elif tile == 21:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=pessa))
            elif tile == 22:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=pessa2))
            elif tile == 23:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=lignedroit))
            elif tile == 26:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=ligenhaut))
            elif tile == 25:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=lignebas))

        # Zoek alle lege tegels (waarde 0) in het doolhof
        lege_plekken = [(j * muurgrootte, i * muurgrootte) for i, rij in enumerate(maze2) for j, waarde in enumerate(rij) if waarde == 0]

        # Kies willekeurig een positie voor het snelheidsobject
        x_positie, y_positie = random.choice(lege_plekken)

        # Maak het snelheidsobject aan (je kan hier een afbeelding toevoegen later)
        snelheids_object = Snelheidsobject(x_positie, y_positie, screen, muurgrootte, afbeelding=speed_img)

#----------------------------------------------------------------------------------------------------------------------#

# Maze3

if maze3 == gebruikte_maze:
    # Waar de speler mag bewegen in de maze
    toegelaten_posities_speler = [0,6,9, 10]
    # Waar de vijand mag bewegen in de maze
    toegelaten_posities_vijand = [0,9,10]
    deur_van_spoken = []
    # speler
    start_positie_x_speler1, start_positie_y_speler1 = 14 * muurgrootte + muurgrootte//2, 9 * muurgrootte + muurgrootte//2
    # vijanden
    start_positie_x_soort1, start_positie_y_soort1 = 1 * muurgrootte + 15, 1 * muurgrootte + 15
    start_positie_x_soort2, start_positie_y_soort2 = 27 * muurgrootte + 15, 1 * muurgrootte + 15
    start_positie_x_soort3, start_positie_y_soort3 = 1 * muurgrootte + 15, 10 * muurgrootte + 15
    start_positie_x_soort4, start_positie_y_soort4 = 27 * muurgrootte + 15, 10 * muurgrootte + 15
    start_positie_x_soort5, start_positie_y_soort5 = 27 * muurgrootte + 15, 13 * muurgrootte + 15
    start_positie_x_soort6, start_positie_y_soort6 = 27 * muurgrootte + 15, 17 * muurgrootte + 15
    # Overdrachtszones
    #zone1, zone2 = (1 * muurgrootte + muurgrootte // 2, 7 * muurgrootte + muurgrootte // 2), (27 * muurgrootte + muurgrootte // 2, 15 * muurgrootte + muurgrootte // 2)
    zone1 = (45, 225)
    zone2 = (825, 465)
    # startzone
    startzone_tegel = (start_positie_x_speler1, start_positie_y_speler1)
    eindzone_x = start_positie_x_speler1 - muurgrootte // 2
    eindzone_y = start_positie_y_speler1 - muurgrootte // 2
    # activatie van vijanden
    leeuw_active = True
    olifant_active = True
    neushoorn_active = True
    gier_active = True
    croco_active = False
    hippo_active = False
    # afbeeldingen vijanden
    soort1 = leeuw1
    soort2 = olifant1
    soort3 = neushoorn1
    soort4 = gier1
    soort5 = crocoo1
    soort6 = hippo1

    for row_index, row in enumerate(gebruikte_maze):
        for col_index, tile in enumerate(row):
            x = col_index * muurgrootte
            y = row_index * muurgrootte
            if tile == 0:
                items.append(Object1(x, y, screen, balgrootte, WIT))
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=way_30x30))
            elif tile == 1:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=resized_tile_0_4))
            elif tile == 2:
                walls.append(Muur(x, y, screen, muurgrootte, kleur=ROOD))
            elif tile == 3:
                walls.append(Muur(x, y, screen, muurgrootte, kleur=GEEL))
            elif tile == 4:
                walls.append(Muur(x, y, screen, muurgrootte, kleur=GROEN))
            elif tile == 5:
                items2.append(Object2(x, y, screen, balgrootte1, WIT))
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=way_30x30))
            elif tile == 6:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=resized_tile_0_4))
            elif tile == 7:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=yellow_green_gradient))
            elif tile == 8:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=etoue_30x30))
            elif tile == 9:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=greenbleu_30x30))
            elif tile == 10:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=etoue_30x30))
            elif tile == 11:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=etoue_30x30))
            elif tile == 31:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=etoue_30x30))
            elif tile == 99:
                walls.append(Muur(x, y, screen, muurgrootte, afbeelding=etoue_30x30))

        # Zoek alle lege tegels (waarde 0) in het doolhof
        lege_plekken = [(j * muurgrootte, i * muurgrootte) for i, rij in enumerate(maze3) for j, waarde in enumerate(rij) if waarde == 0]

        # Kies willekeurig een positie voor het snelheidsobject
        x_positie, y_positie = random.choice(lege_plekken)

        # Maak het snelheidsobject aan (je kan hier een afbeelding toevoegen later)
        snelheids_object = Snelheidsobject(x_positie, y_positie, screen, muurgrootte, afbeelding=speed_img)

#----------------------------------------------------------------------------------------------------------------------#

def a_star(maze, start, goal, tile_size, toegelaten_posities_vijand):
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
            if 0 <= nx < rows and 0 <= ny < cols and maze[int(nx)][int(ny)] in toegelaten_posities_vijand: # welke vakjes de spook mag bewegen
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