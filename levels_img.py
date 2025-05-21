#!/usr/bin/env python3
import pygame, psycopg

def conv_level(lvl):
    ls = [[int(lvl["lvl"][j+8*i]) for j in range(8)] for i in range(8)]
    li = [[(0,0,2,3)[ls[i][j]] for j in range(8)] for i in range(8)]
    h = [int(lvl["hinth"][i]) for i in range(8)]
    v = [int(lvl["hintv"][i]) for i in range(8)]
    return (li, ls, h, v)

def conv_level_solved(lvl):
    ls = [[int(lvl["lvl"][j+8*i]) for j in range(8)] for i in range(8)]
    li = [[(0,1,2,3)[ls[i][j]] for j in range(8)] for i in range(8)]
    h = [int(lvl["hinth"][i]) for i in range(8)]
    v = [int(lvl["hintv"][i]) for i in range(8)]
    return (li, ls, h, v)

def draw_screen(finish=False):
    global img, font_hint, screen, lvltab, lvlh, lvlv, wallh, wallv, background_surface

    # Appliquer le fond du site
    screen.blit(background_surface, (0, 0))

    # Taille des cases et décalage
    case_size = 50
    offset_x = 40
    offset_y = 40

    # Dessiner les éléments de la grille
    for i in range(8):
        for j in range(8):
            case = lvltab[i][j]
            if case == 1:  # Mur
                screen.blit(img[0], (offset_x + j * case_size, offset_y + i * case_size))
            if case == 2:  # Mob (Goomba)
                screen.blit(img[1], (offset_x + j * case_size, offset_y + i * case_size))
            elif case == 3:  # Trunk
                screen.blit(img[2], (offset_x + j * case_size, offset_y + i * case_size))

    # Dessiner les indices horizontaux (en haut)
    for i in range(8):
        color = (0, 255, 0) if lvlh[i] == 0 else (255, 0, 0)
        if finish:
            color = (0, 255, 0)
        text = font_hint.render(str(lvlh[i]), False, color)
        screen.blit(text, (offset_x + i * case_size + case_size // 2 - 10, offset_y - 30))

    # Dessiner les indices verticaux (à gauche)
    for i in range(8):
        color = (0, 255, 0) if lvlv[i] == 0 else (255, 0, 0)
        if finish:
            color = (0, 255, 0)
        text = font_hint.render(str(lvlv[i]), False, color)
        screen.blit(text, (offset_x - 30, offset_y + i * case_size + case_size // 2 - 10))

    # Dessiner la grille (lignes vertes)
    for i in range(9):
        # Lignes horizontales
        pygame.draw.line(screen, (0, 255, 0), (offset_x, offset_y + i * case_size), (offset_x + 8 * case_size, offset_y + i * case_size), 2)
        # Lignes verticales
        pygame.draw.line(screen, (0, 255, 0), (offset_x + i * case_size, offset_y), (offset_x + i * case_size, offset_y + 8 * case_size), 2)

pygame.init()
screen = pygame.display.set_mode((450, 450))
pygame.display.set_caption("Dungeon & Diagrams")

clock = pygame.time.Clock()

# Charger les images
wall = pygame.image.load("static/img/brique.png")
mob = pygame.image.load("static/img/monstre.png")
trunk = pygame.image.load("static/img/lucky.png")

img = (wall, mob, trunk)

font_hint = pygame.font.Font(None, 36)  # Taille de police ajustée

# Créer une surface pour le fond du site
background_surface = pygame.Surface((450, 450))
background_surface.fill((27, 48, 36))  # Fond noir
for y in range(0, 460, 2):
    pygame.draw.line(background_surface, (28, 37, 38), (0, y), (460, y), 1)  # 0.05 * 255 ≈ 12 pour l'alpha


running = True
wallh = [0] * 8
wallv = [0] * 8


if __name__ == "__main__":
    conn = psycopg.connect(
        "dbname=py2501 user=py2501 password=cruipi72failou host=student.endor.be port=5433"
    )
    with conn.cursor() as cursor:
        cursor.execute("SELECT lvl, hinth, hintv, lid FROM levels")
        levels = cursor.fetchall()

        for level in levels:
            lvl = {"lvl": level[0], "hinth": level[1], "hintv": level[2]}
            (lvltab, lvlsol, lvlh, lvlv) = conv_level(lvl)
            draw_screen()
            pygame.display.flip()
            # Enregistrer l'image de la grille non résolue
            pygame.image.save(screen, f"static/img/levels/level-{level[3]}.png")
            (lvltab, lvlsol, lvlh, lvlv) = conv_level_solved(lvl)
            draw_screen(True)
            pygame.display.flip()
            # Enregistrer l'image de la grille résolue
            pygame.image.save(screen, f"static/img/levels-solved/level-{level[3]}.png")


