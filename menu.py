import pygame
import json
from Setting import breedte, hoogte, font , screen, BLAUW ,WIT, ZWART, GROEN, BRUIN,GRIJS


def create_button(text, rect, color, text_color):
    pygame.draw.rect(screen, color, rect)
    txt = font.render(text, True, text_color)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)

# Speluitleg-scherm
def show_help():
    running = True

    # Vergroot het scherm
    nieuw_breedte = 1200
    nieuw_hoogte = 700
    font = pygame.font.SysFont(None, 30)
    screen = pygame.display.set_mode((nieuw_breedte, nieuw_hoogte))

    help_text = [
        "Regels:",
        "1. Eet pac-dots om punten te scoren.",
        "2. Geesten Opeten: Als je 10 vijanden opeet, krijg je een extra leven. Je kunt geesten alleen opeten wanneer je ",
        "   een power-up hebt gepakt.",
        "3. Punten: Hoe meer geesten je opeet, hoe meer punten je verdient. Je score blijft stijgen zolang je vijanden ",
        "   blijft verslaan.",
        "4. Het Einddoel: In het laatste deel van het spel is het doel om een geheime doorgang te vinden. Zodra je die vindt, ",
        "   moet je het geheime tunnelpad volgen naar de uitgang aan het einde van het doolhof.",
        "5. Snellere Geesten: In dit laatste deel worden de geesten sneller, wat het moeilijker maakt om te ontsnappen.",
        "6. Speciale Power-Ups:",
        "      - Snelheids-power-up: Hiermee kun je sneller bewegen. Je verdient deze door punten te verzamelen.",
        "      - Muur-breek-power-up: Deze laat je bepaalde muren in het doolhof breken om een nieuwe weg te maken. ",
        "        Ook deze power-up krijg je door meer punten te scoren.",
    ]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        screen.fill(BLAUW if hasattr(pygame, 'BLAUW') else BLAUW)
        for i, line in enumerate(help_text):
            txt = font.render(line, True, WIT)
            screen.blit(txt, (50, 20 + i * 50))
        pygame.display.flip()
   # Zet scherm terug naar originele grootte na uitleg
    screen = pygame.display.set_mode((breedte, hoogte))

# Hoofdmenu
def toon_menu():
    achtergrond = pygame.image.load("Background1.png")
    achtergrond = pygame.transform.scale(achtergrond, (breedte, hoogte))

    # Definieer knoppen
    start_rect = pygame.Rect(breedte//2 - 100, hoogte//2 - 50, 200, 100)
    help_rect = pygame.Rect(50, hoogte - 100, 200, 50)

    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    toon_submenu()  # Eerst submenu tonen
                    return  # Daarna verder
                elif help_rect.collidepoint(event.pos):
                    show_help()



        screen.blit(achtergrond, (0, 0))
        create_button("Start", start_rect, GROEN, ZWART)
        create_button("How to Play", help_rect, WIT, ZWART)
        pygame.display.flip()

# Roep menu aan bij het opstarten



#submenu
def toon_submenu():
    achtergrond = pygame.image.load("achtergrond_savanne.png")
    achtergrond = pygame.transform.scale(achtergrond, (breedte, hoogte))
    font = pygame.font.SysFont(None, 55)
    klein_font = pygame.font.SysFont(None, 35)
    knop_rect = pygame.Rect(100, hoogte // 2 - 50, 200, 100)
    knop_rect2 = pygame.Rect(570, hoogte // 2 - 50, 200, 100)
    knop_terug = pygame.Rect(300, hoogte - 80, 300, 50)

    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if knop_rect.collidepoint(event.pos):
                    menu_running = False  # Start Mode 1
                elif knop_rect2.collidepoint(event.pos):
                    menu_running = False  # Start Mode 2
                elif knop_terug.collidepoint(event.pos):
                    from menu import toon_menu
                    toon_menu()
                    return  # Sluit dit menu na terugkeren naar hoofdmenu



        screen.blit(achtergrond, (0, 0))
        pygame.draw.rect(screen, BRUIN, knop_rect)
        pygame.draw.rect(screen, GRIJS, knop_rect2)
        pygame.draw.rect(screen, WIT, knop_terug)

        tekst = font.render("Mode 1:", True, ZWART)
        screen.blit(tekst, (knop_rect.x + 10, knop_rect.y + 25))

        tekst1_1 =   klein_font.render("Chrono", True, ZWART)
        screen.blit(tekst1_1, (knop_rect.x + 10, knop_rect.y + 60))

        tekst2 = font.render("Mode 2:", True, ZWART)
        screen.blit(tekst2, (knop_rect2.x + 10, knop_rect2.y + 25))

        tekst2_1 =   klein_font.render("Punten", True, ZWART)
        screen.blit(tekst2_1, (knop_rect2.x + 10, knop_rect2.y + 60))

        screen.blit(klein_font.render("Terug naar hoofdmenu", True, ZWART), (knop_terug.x + 30, knop_terug.y + 10))


        pygame.display.flip()

