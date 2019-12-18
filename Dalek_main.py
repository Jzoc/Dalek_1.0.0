import pygame as pg
import re
import random as rnd

"""FIX ERROR"""
"""B DEL I FUNKTIONER"""

# -------- Pygame initializer and constants
pg.init()
# -------- Graphic constants
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
GREEN = (0, 128, 0)
# -------- Defining fonts for game overlay --------
BigFont = pg.font.Font(None, 60)
SmallFont = pg.font.Font(None, 30)


# -------- Object Classes --------
# Class for walls
class Wall(object):
    wall_list = []
    wall_pos_list = []

    def __init__(self, pos):
        self.wall_list.append(self)
        self.rect = pg.Rect(pos[0], pos[1], 20, 20)
        self.wall_pos_list.append((self.rect.x, self.rect.y))


# Class for floor (used for Sonic Screwdriver)
class Floor(object):
    floor_list = []
    floor_pos_list = []

    def __init__(self, pos):
        self.floor_list.append(self)
        self.rect = pg.Rect(pos[0], pos[1], 20, 20)
        self.floor_pos_list.append((self.rect.x, self.rect.y))


# Class for Junk
class Junk(object):
    junk_list = []
    junk_pos_list = []

    def __init__(self, pos):
        self.junk_list.append(self)
        self.rect = pg.Rect(pos[0], pos[1], 20, 20)
        self.junk_pos_list.append((self.rect.x, self.rect.y))


# Class for Dalek
class Dalek(object):
    dalek_list = []

    def __init__(self, pos, d_id):
        self.d_id = d_id
        self.rect = pg.Rect((pos[0], pos[1], 20, 20))
        self.x_change = 20
        self.y_change = 20
        self.dalek_list.append(self)

    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        for wall in Wall.wall_list:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom

    def move(self, dx, dy):
        """Move along the Dalek"""
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)


# Class for Doctor
class Doctor(object):
    def __init__(self, pos):
        self.rect = pg.Rect(pos[0], pos[1], 20, 20)

    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        for wall in Wall.wall_list:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom
        """Check for collisions with junk, if we hit junk, move away from junk"""
        for junk in Junk.junk_list:
            if self.rect.colliderect(junk.rect):
                if dx > 0:
                    self.rect.right = junk.rect.left
                if dx < 0:
                    self.rect.left = junk.rect.right
                if dy > 0:
                    self.rect.bottom = junk.rect.top
                if dy < 0:
                    self.rect.top = junk.rect.bottom

    def move(self, dx, dy):
        """Move along the Dalek"""
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
        for i, dalek in enumerate(Dalek.dalek_list):
            if dalek.rect.x < self.rect.x:
                dalek.move(20, 0)
            if dalek.rect.x > self.rect.x:
                dalek.move(-20, 0)
            if dalek.rect.y < self.rect.y:
                dalek.move(0, 20)
            if dalek.rect.y > self.rect.y:
                dalek.move(0, -20)


# -------- Game Functions and classes--------
def teleport(player):
    t_pos = list(set(Floor.floor_pos_list) - set(Junk.junk_pos_list))
    new_pos = rnd.choice(t_pos)
    player.rect.x = new_pos[0]
    player.rect.y = new_pos[1]


class LenghtError(Exception):
    pass


class SymbolError(Exception):
    pass


def check_file():
    """Checks user file and makes sure it is in the right format and in the right directory"""
    log = open("WelcomeScreen", "r").read()
    print(log)
    loop = True
    while loop:
        try:
            file = input("Please select a level: ")
            txt = open(file)
            map_data = txt.readlines()
            txt.close()
            for i in map_data:
                if not re.match("^[DA*.#]*$", i):
                    raise SymbolError
                elif len(i) != 21:
                    raise LenghtError
            loop = False
        except SymbolError:
            print("Error: Only (D), (A), (*), (.), (#) are allowed!")
        except LenghtError:
            print("Error: All lines must be 20 entries long!")
        except FileNotFoundError:
            print("No such file in directory.")
        except PermissionError:
            print("No such file in directory.")
        except OSError:
            print("No such file in directory.")
        except SyntaxError:
            print("No such file in directory.")

    return map_data


def main():
    """Makes the level from the selected file"""
    file = check_file()
    map_x = 0
    map_y = 0
    d_id = 0
    for row in file:
        for sym in row:
            if sym == "*":
                Wall((map_x, map_y))
            if sym == ".":
                Floor((map_x, map_y))
            if sym == "#":
                Junk((map_x, map_y))
            if sym == "A":
                Dalek((map_x, map_y), d_id)
                d_id += 1
            if sym == "D":
                doctor = Doctor((map_x, map_y))
            map_x += 20
        map_y += 20
        map_x = 0

    # ----------- Main Game Loop -------------
    clock = pg.time.Clock()
    carry_on = True
    end = False
    while carry_on:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                carry_on = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_x:
                    carry_on = False
            key = pg.key.get_pressed()
            if not end:
                if key[pg.K_LEFT]:
                    doctor.move(-20, 0)
                if key[pg.K_RIGHT]:
                    doctor.move(20, 0)
                if key[pg.K_UP]:
                    doctor.move(0, -20)
                if key[pg.K_DOWN]:
                    doctor.move(0, 20)
                if key[pg.K_s]:
                    teleport(doctor)
        # Drawing
        screen = pg.display.set_mode((400, 400))
        pg.display.set_caption("Dalek")
        screen.fill(BLACK)
        for wall in Wall.wall_list:
            pg.draw.rect(screen, GREEN, wall.rect)
        for dalek in Dalek.dalek_list:
            pg.draw.rect(screen, ORANGE, dalek.rect)
        for junk in Junk.junk_list:
            pg.draw.rect(screen, RED, junk.rect)
        pg.draw.rect(screen, WHITE, doctor.rect)
        # Places Junk
        collided = []
        for d1 in Dalek.dalek_list:
            for d2 in Dalek.dalek_list:
                if d1.d_id != d2.d_id and d1.d_id not in collided:
                    if d1.rect == d2.rect:
                        junk = Junk(d1.rect)
                        Junk.junk_list.append(junk)
                        Wall.wall_pos_list.append(junk.rect)
                        collided.append(d1)
                        collided.append(d2)
                        Dalek.dalek_list.remove(d1)
                        Dalek.dalek_list.remove(d2)

        # Removes a dalek if it collides with junk
        for junk in Junk.junk_list:
            for dalek in Dalek.dalek_list:
                if dalek.rect.colliderect(junk.rect):
                    Dalek.dalek_list.remove(dalek)
        # Wining and Losing
        for dalek in Dalek.dalek_list:  # If the player is caught by a dalek, the game will end
            if doctor.rect.colliderect(dalek.rect):
                # If you lose the game, display the relevant info
                screen.fill(BLACK)
                lose_text = BigFont.render("YOU LOSE", 1, WHITE)
                screen.blit(lose_text, (200 - lose_text.get_width() // 2, 150))
                lose_desc = SmallFont.render("YOU WERE CAUGHT BY A DALEK", 1, WHITE)
                screen.blit(lose_desc, (200 - lose_desc.get_width() // 2, 200))
                end = True
        if len(Dalek.dalek_list) == 0:  # If no Daleks are left the game will end
            # If you win the game, display the relevant info
            screen.fill(BLACK)
            win_text = BigFont.render("YOU WIN", 1, WHITE)
            screen.blit(win_text, (200 - win_text.get_width() // 2, 150))
            win_desc = SmallFont.render("ALL DALEKS ARE DEAD", 1, WHITE)
            screen.blit(win_desc, (200 - win_desc.get_width() // 2, 200))
            end = True
        # flip screen between frames
        pg.display.flip()
        # --- Limit to 60 frames per second
        clock.tick(60)
    pg.quit()


main()
