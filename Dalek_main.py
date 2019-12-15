import pygame as pg
import re
import random as rnd
# -------- Pygame initializer and constants
pg.init()
# graphic constants
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
GREEN = (0, 128, 0)
# Defining the fonts used for end screens
font1 = pg.font.Font(None, 60)
font2 = pg.font.Font(None, 30)
# The clock will be used to control how fast the screen updates
clock = pg.time.Clock()
# -------- Object Classes -----------
# class for doctor, the player controlled object
class Player(object):
    def __init__(self, pos):
        self.rect = pg.Rect(pos[0], pos[1], 20, 20)
    def move(self, dx, dy):
        """move along each axis separately"""
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
        """defines how each dalek moves to chase the doctor"""
        for i, dalek in enumerate(dalek_list):
            d_x = abs(self.rect.x - dalek.rect.x)
            d_y = abs(self.rect.y - dalek.rect.y)
            if not d_y == 0:
                R = (d_x/d_y)
            if d_x == 0: # The doctor and dalek are on the same level
                if dalek.rect.x < self.rect.x:
                    dalek.move(20, 0)
                if dalek.rect.x > self.rect.x:
                    dalek.move(-20, 0)
                if dalek.rect.y < self.rect.y:
                    dalek.move(0, 20)
                if dalek.rect.y > self.rect.y:
                    dalek.move(0, -20)
            elif d_y == 0: # The doctor and dalek are above and below each other 
                if dalek.rect.x < self.rect.x:
                    dalek.move(20, 0)
                if dalek.rect.x > self.rect.x:
                    dalek.move(-20, 0)
                if dalek.rect.y < self.rect.y:
                    dalek.move(0, 20)
                if dalek.rect.y > self.rect.y:
                    dalek.move(0, -20)
            elif d_x > d_y: # the dalek is further to the side than above or below
                r_x = rnd.randrange(1, d_x)
                r_y = rnd.randrange(1, d_y)
                r = (r_x/r_y)
                if r > R:
                    if dalek.rect.x < self.rect.x:
                        dalek.move(20, 0)
                    if dalek.rect.x > self.rect.x:
                        dalek.move(-20, 0)
                    if dalek.rect.y < self.rect.y:
                        dalek.move(0, 20)
                    if dalek.rect.y > self.rect.y:
                        dalek.move(0, -20)
                if r < R:
                    if dalek.rect.x < self.rect.x:
                        dalek.move(20, 0)
                    elif dalek.rect.x > self.rect.x:
                        dalek.move(-20, 0)
                    elif dalek.rect.y < self.rect.y:
                        dalek.move(0, 20)
                    elif dalek.rect.y > self.rect.y:
                        dalek.move(0, -20)
            elif d_x < d_y: # the dalek is further above or below, than to the side
                r_x = rnd.randrange(1, d_x)
                r_y = rnd.randrange(1, d_y)
                r = (r_x / r_y)
                if r > R:
                    if dalek.rect.x < self.rect.x:
                        dalek.move(20, 0)
                    elif dalek.rect.x > self.rect.x:
                        dalek.move(-20, 0)
                    elif dalek.rect.y < self.rect.y:
                        dalek.move(0, 20)
                    elif dalek.rect.y > self.rect.y:
                        dalek.move(0, -20)
                if r < R:
                    if dalek.rect.x < self.rect.x:
                        dalek.move(20, 0)
                    if dalek.rect.x > self.rect.x:
                        dalek.move(-20, 0)
                    if dalek.rect.y < self.rect.y:
                        dalek.move(0, 20)
                    if dalek.rect.y > self.rect.y:
                        dalek.move(0, -20)
            elif d_x == d_y: # The doctor and dalek are on a diagonal
                if dalek.rect.x < self.rect.x:
                    dalek.move(20, 0)
                if dalek.rect.x > self.rect.x:
                    dalek.move(-20, 0)
                if dalek.rect.y < self.rect.y:
                    dalek.move(0, 20)
                if dalek.rect.y > self.rect.y:
                    dalek.move(0, -20)
    def move_single_axis(self, dx, dy):
        """move along one axis separately"""
        self.rect.x += dx
        self.rect.y += dy
        """Check for collisions with walls, if we hit a wall, move away from wall"""
        for wall in wall_list:
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
        for junk in junk_list:
            if self.rect.colliderect(junk.rect):
                if dx > 0:
                    self.rect.right = junk.rect.left
                if dx < 0:
                    self.rect.left = junk.rect.right
                if dy > 0:
                    self.rect.bottom = junk.rect.top
                if dy < 0:
                    self.rect.top = junk.rect.bottom
# class for the dalek
class Dalek(object):
    def __init__(self, pos, id):
        self.id = id
        self.rect = pg.Rect(pos[0], pos[1], 20, 20)
        self.x_change = 20
        self.y_change = 20
        dalek_pos_list.append((self.rect.x, self.rect.y))
        dalek_list.append(self)
    def move(self, dx, dy):
        """move along each axis separately"""
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    def move_single_axis(self, dx, dy):
        """move along one axis separately"""
        self.rect.x += dx
        self.rect.y += dy
        """Check for collisions with walls, if we hit a wall, move away from wall"""
        for wall in wall_list:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom
# class for the walls
class Wall(object):
    def __init__(self, pos):
        wall_list.append(self)
        self.rect = pg.Rect(pos[0], pos[1], 20, 20)
        wall_pos_list.append((self.rect.x, self.rect.y))
# class for floor
class Floor(object):
    def __init__(self, pos):
        floor_list.append(self)
        self.rect = pg.Rect(pos[0], pos[1], 20, 20)
        floor_pos_list.append((self.rect.x, self.rect.y))
# class for Junk
class Junk(object):
    def __init__(self, pos):
        junk_list.append(self)
        self.rect = pg.Rect(pos[0], pos[1], 20, 20)
        junk_pos_list.append((self.rect.x, self.rect.y))
# Adding the individual objects to the relevant list
wall_list = []
wall_pos_list = []
floor_list = []
floor_pos_list = []
dalek_list = []
dalek_pos_list = []
junk_list = []
junk_pos_list = []
# -------- Main Program Loop -----------
class Game():
    # creates a map from a user-selected file
    # criteria for valid file selection
    # Player instructions
    log = open("WelcomeScreen", "r").read()
    print(log)
    loop = True
    while loop:
        try:
            file = input("Please select a level: ")
            txt = open(file)
            MapData = txt.readlines()
            txt.close()
            loop = False
        except FileNotFoundError:
            print("No such file in directory.")
    for i in MapData:
        if not re.match("^[DA*.#]*$", i):
            raise ValueError("""Error: Only (D), (A), (*), (.), (#) are allowed!
            Please select a new map.""")
        elif len(i) != 21:
            raise ValueError("""Error: All lines must be 20 entries long!
            Please select a new map.""")
    # Making the map from the selected file
    x = 0
    y = 0
    id = 0
    for row in MapData:
        for col in row:
            if col == "D":
                player = Player((x, y))
            if col == "A":
                Dalek((x, y), id)
                id += 1
            if col == "*":
                Wall((x, y))
            if col == ".":
                Floor((x, y))
            if col == "#":
                Junk((x, y))
            x += 20
        y += 20
        x = 0
    # --- Main event loop
    CarryOn = True
    while CarryOn:
        for event in pg.event.get():  # User did something
            if event.type == pg.QUIT:  # If user clicked close
                CarryOn = False     # Flag that we are done so we exit this loop
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_x:     # Pressing the x Key will quit the game
                    CarryOn = False
        # Move the player if an arrow key is pressed
        # For each step taken, dalek moves towards doctor
            key = pg.key.get_pressed()
            if key[pg.K_LEFT]:
                player.move(-20, 0)
            if key[pg.K_RIGHT]:
                player.move(20, 0)
            if key[pg.K_UP]:
                player.move(0, -20)
            if key[pg.K_DOWN]:
                player.move(0, 20)
        # Teleport the doctor to a random position on the map, not into a wall, or junk
            if key[pg.K_s]:
                t_pos = list(set(floor_pos_list)-set(junk_pos_list))
                new_pos = rnd.choice(t_pos)
                player.rect.x = new_pos[0]
                player.rect.y = new_pos[1]
        # --- Drawing code should go here
        screen = pg.display.set_mode((400, 400))
        pg.display.set_caption("Dalek_PreAlpha")
        screen.fill(BLACK)
        for wall in wall_list:
            pg.draw.rect(screen, GREEN, wall.rect)
        for dalek in dalek_list:
            pg.draw.rect(screen, ORANGE, dalek.rect)
        for junk in junk_list:
            pg.draw.rect(screen, RED, junk.rect)
        pg.draw.rect(screen, WHITE, player.rect)
        # --- Creates a junk when two daleks collide
        collided = []
        for d1 in dalek_list:
            for d2 in dalek_list:
                if d1.id != d2.id and d1.id not in collided:
                    if d1.rect == d2.rect:
                        junk = Junk(d1.rect)
                        junk_list.append(junk)
                        wall_pos_list.append(junk.rect)
                        collided.append(d1)
                        collided.append(d2)
                        dalek_list.remove(d1)
                        dalek_list.remove(d2)
        # --- Removes a dalek if it collides with junk
        for junk in junk_list:
            for dalek in dalek_list:
                if dalek.rect.colliderect(junk.rect):
                    dalek_list.remove(dalek)
        # --- Wining and Losing
        for dalek in dalek_list:  # If the player is caught by a dalek, the game will end
            if player.rect.colliderect(dalek.rect):
                # If you win or lose the game, display the relevant info
                screen.fill(BLACK)
                LoseText = font1.render("YOU LOSE", 1, WHITE)
                screen.blit(LoseText, (200 - LoseText.get_width() // 2, 150))
                LoseDesc = font2.render("YOU WERE CAUGHT BY A DALEK", 1, WHITE)
                screen.blit(LoseDesc, (200 - LoseDesc.get_width() // 2, 200))
        if len(dalek_list) == 0:  # If no Daleks are left the game will end
            # If you win or lose the game, display the relevant info
            screen.fill(BLACK)
            WinText = font1.render("YOU WIN", 1, WHITE)
            screen.blit(WinText, (200 - WinText.get_width() // 2, 150))
            WinDesc = font2.render("ALL DALEKS ARE DEAD", 1, WHITE)
            screen.blit(WinDesc, (200 - WinDesc.get_width() // 2, 200))
        # flip screen between frames
        pg.display.flip()
        # --- Limit to 60 frames per second
        clock.tick(60)
    # Once we have exited the main program loop we can stop the game engine:
    pg.quit()
