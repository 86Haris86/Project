# Import and initialize the pygame library
import pygame



# Initialisatie
pygame.init()


# imports van andere files
from Afbeeldingen import pacman_imgs_op_schaal
from Setting import muurgrootte , gebruikte_maze, maze3, maze2,maze1 , startzone_tegel , eindzone_x ,eindzone_y
from Setting import leeuw_active , olifant_active , neushoorn_active , gier_active , croco_active , hippo_active , soort1 , soort2 , soort3 , soort4 , soort5 , soort6
from Setting import breedte, hoogte, screen, tijd, fps, font, deur_van_spoken, tekst_punten_x, tekst_punten_y, tekst_tijd_x, tekst_tijd_y
from Setting import ROOD , ZWART , WIT , GROEN ,BRUIN, GRIJS, walls , items , items2 , toegelaten_posities_speler , toegelaten_posities_vijand , snelheids_object
from Setting import start_positie_x_speler1 , start_positie_y_speler1 , start_positie_x_soort1, start_positie_y_soort1 , start_positie_x_soort2, start_positie_y_soort2 , start_positie_x_soort3, start_positie_y_soort3
from Setting import start_positie_x_soort4, start_positie_y_soort4 , start_positie_x_soort5, start_positie_y_soort5, start_positie_x_soort6, start_positie_y_soort6
from Hulpfuncties import toon_levens,MazeChecker
from Speler import Speler , radius_speler , snelheid_speler
from Vijand import Spook , snelheid_monster , snelheid_monster_2
from Hulpfuncties import check_collision2, check_collision
from menu import toon_menu, toon_submenu

# Lijst van mazes én de bijbehorende startpositie van de speler
maze_list = [maze1, maze2, maze3]
start_positions = [
    (start_positie_x_speler1, start_positie_y_speler1),  # bij maze1
    (start_positie_x_speler1, start_positie_y_speler1),  # bij maze2 (pas aan indien nodig)
    (start_positie_x_speler1, start_positie_y_speler1),  # bij maze3
]

current_maze_idx = 0
switch_interval_ms = 2 * 60 * 1000  # 2 minuten in milliseconden
last_switch_time = pygame.time.get_ticks()




# Spelers & Spoken aanmaken
speler = Speler(start_positie_x_speler1 , start_positie_y_speler1, screen, WIT, radius_speler, snelheid_speler , toegelaten_posities_speler, pacman_imgs_op_schaal)
leeuw = Spook(start_positie_x_soort1, start_positie_y_soort1 , screen, soort1, snelheid_monster, "pinky" , toegelaten_posities_vijand , leeuw_active )
olifant = Spook(start_positie_x_soort2, start_positie_y_soort2 , screen, soort2, snelheid_monster, "blinky" , toegelaten_posities_vijand , olifant_active )
neushoorn = Spook(start_positie_x_soort3, start_positie_y_soort3 , screen, soort3, snelheid_monster, "inky" , toegelaten_posities_vijand , neushoorn_active )
gier = Spook(start_positie_x_soort4, start_positie_y_soort4 , screen, soort4, snelheid_monster, "clyde" , toegelaten_posities_vijand , gier_active )
croco = Spook(start_positie_x_soort5, start_positie_y_soort5, screen,  soort5, snelheid_monster_2 , "blinky", toegelaten_posities_vijand , croco_active )
hippo = Spook(start_positie_x_soort6, start_positie_y_soort6, screen,  soort6, snelheid_monster_2, "blinky", toegelaten_posities_vijand , hippo_active )

list_of_objects = [speler, leeuw, olifant, neushoorn, gier , croco, hippo]
list_of_monsters = [leeuw, olifant, neushoorn, gier , croco, hippo]

# Vlag om bij te houden of Croco & Hippo al eens geactiveerd zijn deze ronde
croco_hippo_activated =  False




toon_menu()
# Game-loop
running = True
while running:
    tijd.tick(fps)
    screen.fill(ZWART)


    # 1. Normale items pakken
    for item in items[:]:
        if item.botsing(speler):
            items.remove(item)
            speler.punten += item.punten()
        # power-up “muren kapot” activeren bij 1000 punten
        if speler.punten >= 1 and not speler.break_walls:
            speler.break_walls = True
        # power-up “snelheid” activeren bij 1000 punten
        if speler.punten >= 1 and not speler.snelheid:
            speler.break_walls = True

    # 2. Speciale items pakken om eetmodus te starten
    for item in items2[:]:
        if item.botsing(speler):
            items2.remove(item)
            speler.start_eetmodus()

            # Zet alle spoken tijdelijk in "vlucht" modus
            for spook in list_of_monsters:
                spook.verander_type("vlucht")
                spook.removeposities(toegelaten_posities_vijand,deur_van_spoken)

    # 3. Spoken checken
    for spook in list_of_monsters:
        if speler.check_collision(spook):
            if speler.eetmodus_actief():
                speler.punten += speler.eetspook(spook)
                spook.verander_type(spook.oorspronkelijk_type)
            else:
                # speler verliest een leven
                speler.levens -= 1
                speler.reset()

                # alle spoken (incl. Croco & Hippo) terug naar start en paden leegmaken
                for spooks in list_of_monsters:
                    spooks.reset()  # zet x,y terug naar initial_state :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}
                    spooks.appendposities(toegelaten_posities_vijand, deur_van_spoken)

                # Croco & Hippo volledig herstarten én écht de-activeren
                croco.reset()  # opnieuw naar initiele pos :contentReference[oaicite:2]{index=2}:contentReference[oaicite:3]{index=3}
                hippo.reset()
                croco.zet_actief(
                    False)  # blokkeren van draw()/patrol() tot trigger :contentReference[oaicite:4]{index=4}:contentReference[oaicite:5]{index=5}
                hippo.zet_actief(False)

                # trigger‐flag resetten zodat je ze in de nieuwe ronde opnieuw moet activeren
                croco_hippo_activated = False

                pygame.time.delay(500)
                if speler.levens <= 0:
                    font = pygame.font.SysFont(None, 75)
                    tekst = font.render("Game Over", True, ROOD)
                    screen.blit(tekst, (breedte // 2 - 150, hoogte // 2 - 40))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    running = False


    # 4. Check na botsing of eetmodus voorbij is
    if not speler.eetmodus_actief():
        for spook in list_of_monsters:
            spook.verander_type(spook.oorspronkelijk_type)  # Zet type terug
            spook.appendposities(toegelaten_posities_vijand, deur_van_spoken)
        speler.eetcombo = 0


    # Check of speler het snelheidsobject raakt , indien wel start het de snelheid en verwijder de object
    if snelheids_object and snelheids_object.botsing(speler):
        speler.activeer_snelheid()
        snelheids_object.delete()

    # Check of snelheidstimer verlopen is
    speler.update_snelheid()

    # controleer of speler trigger bereikt ( bv op tegel 15,9)
    speler_tegel_x , speler_tegel_y = speler.x // muurgrootte , speler.y // muurgrootte
    if gebruikte_maze == maze3 \
            and not croco_hippo_activated \
            and speler.is_op_triggertegel([(24, 13), (24, 17)]):
        croco.zet_actief(True)
        hippo.zet_actief(True)
        croco_hippo_activated = True

    # Score en timer tonen
    score_text = font.render(f"Score: {speler.punten}", True, WIT)
    screen.blit(score_text, (tekst_punten_x, tekst_punten_y))
    speler.toon_timer(screen, font, tekst_tijd_x, tekst_tijd_y, WIT)


    alle_items_opgeraakt = len(items) == 0 and len(items2) == 0

    if alle_items_opgeraakt:
        pygame.draw.rect(screen, GROEN, (eindzone_x,eindzone_y, muurgrootte, muurgrootte))

    # bepaal tegelcoördinaten
    speler_tegel = (speler.x // muurgrootte, speler.y // muurgrootte)
    # in maze3: tegel == 99 wint het spel
    if gebruikte_maze is maze3 and gebruikte_maze[speler_tegel[1]][speler_tegel[0]] == 99:
        font = pygame.font.SysFont(None, 75)
        tekst = font.render("GEWONNEN!", True, GROEN)
        screen.blit(tekst, (breedte // 2 - 150, hoogte // 2 - 40))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
# ————————————————



        # ————————————————

        # Update breek-animatie en verwijder kapotte muren
    for wall in walls[:]:  # door een kopie lopen om veilig te verwijderen
        if not wall.aanwezig:  # zodra break_stage > 1 is geworden
            walls.remove(wall)  # haal de muur écht weg


        # ————————————————

    # Muren tekenen
    for wall in walls:
        wall.draw()

    # Items tekenen
    for item in items:
        item.draw()
    for item in items2:
        item.draw()

    # teken het snelheidsobject als het nog bestaat
    if not snelheids_object.botsing(speler):
        snelheids_object.draw()

    # Speler tekenen
    speler.draw()
    speler.patrol()
    speler.overdracht()
    # tegel waar de speler staat
    speler_tegel_x, speler_tegel_y = speler.x // muurgrootte, speler.y // muurgrootte
    speler_tegel = (speler_tegel_x, speler_tegel_y)
    # tekent de spoken en 'doet de spoken bewegen'
    for obj in list_of_monsters:
        obj.draw()
        obj.overdracht()
        obj.patrol(speler, olifant)

    # --> HIER score tonen
    score_text = font.render(f"Score: {speler.punten}", True, WIT)
    screen.blit(score_text, (tekst_punten_x , tekst_punten_y))
    speler.toon_timer(screen, font , tekst_tijd_x , tekst_tijd_y , WIT)

    toon_levens(screen, speler.levens)



    pygame.display.flip()



pygame.quit()

#----------------------------------------------------------------------------------------------------------------------#