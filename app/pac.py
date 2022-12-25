# -*- coding: utf-8 -*-

import pgzrun
import math
from pgzero.actor import Actor
from pgzero.clock import clock
from pgzero.keyboard import keys
from pgzero.loaders import sounds
from pgzero.rect import Rect

import random

WIDTH = 640
HEIGHT = 640
TITLE = "Pac-Man"
WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE * BLOCK_SIZE
HEIGHT = WORLD_SIZE * BLOCK_SIZE
SPEED = 2
GHOST_SPEED = 1
WELCOME_SCREEN = """
Welcome to Pacman!
Please enter your name:
"""

leaderboard = """
Leaderboard:
1. 1000
2. 900
3. 800
4. 700
"""

char_to_image = {
    ".": "dot.png",
    "=": "wall.png",
    "*": "power.png",
    "g": "ghost1.png",
    "G": "ghost2.png",
}

# An array containing the world tiles

world = [
    "====================",
    "=........G.........=",
    "==..=..=..=..=..=..=",
    "=........=...=...=.=",
    "=...g..=...=...=...=",
    "=......=...=.*.=...=",
    "=......=...=...=...=",
    "==..=..=..=..=..=..=",
    "=........=...=...=.=",
    "=..g...=...=...=...=",
    "=......=...=...=...=",
    "=......=...=...=...=",
    "==..=..=..=..=..=..=",
    "=.....G..=...=...=.=",
    "=..*...=...=...=...=",
    "=......=...=...=...=",
    "=......=...=...=...=",
    "=......=...=...=...=",
    "=......=...=...=...=",
    "====================",
]

# Our sprites
pacman = Actor("pacman_o.png")
pacman.x = pacman.y = 1.5 * BLOCK_SIZE
# Direction that we're going in
pacman.dx, pacman.dy = 0, 0
pacman.banner = None
pacman.banner_counter = 0
pacman.score = 0
pacman.lives = 3
pacman.powerup = 0
pacman.freeze = False
pacman.initialised = False
pacman.player = ""
pacman.name_saved = False
pacman.food_left = 0
for row in world:
    pacman.food_left += row.count(".")

ghosts = []
# Where do the ghosts start?
ghost_start_pos = []

RED = 200, 0, 0
BOX = Rect((50, 380), (200, 75))

# Your level will contain characters, they map
# to the following images
char_to_image = {
    ".": "dot.png",
    "=": "wall.png",
    "*": "power.png",
    "g": "ghost1.png",
    "G": "ghost2.png",
}


def check_world():
    res = True
    depth = len(world)
    width = len(world[0])
    if depth != WORLD_SIZE:
        raise Exception("World is not the right depth")
        res = False
    for row in world:
        if len(row) != width:
            raise Exception("World rows are not all the same width")
            res = False
        for char in row:
            if char not in char_to_image:
                raise Exception("Unknown character in world: " + char)
                res = False

    return res


def eat_food():
    ix, iy = int(pacman.x / BLOCK_SIZE), int(pacman.y / BLOCK_SIZE)
    if world[iy][ix] == ".":
        world[iy] = world[iy][:ix] + " " + world[iy][ix + 1 :]
        pacman.food_left -= 1
        pacman.score += 1
        sounds.eat_food.play()
        print("Food left: ", pacman.food_left)
    elif world[iy][ix] == "*":
        powerup(ix, iy)


def powerup(ix, iy):
    world[iy] = world[iy][:ix] + " " + world[iy][ix + 1 :]
    pacman.score += 5
    pacman.powerup = 25
    sounds.power_pellet.play()
    set_banner("Power Up!", 5)
    clock.schedule_unique(powerdown, 5)
    for g in ghosts:
        new_ghost_direction(g, GHOST_SPEED)


def powerdown():
    set_banner("Power down", 3)
    pacman.powerup = 0


def new_ghost_direction(g, GHOST_SPEED):
    if pacman.powerup:
        g.dx = math.copysign(GHOST_SPEED * 1.5, g.x - pacman.x)
        g.dy = math.copysign(GHOST_SPEED * 1.5, g.y - pacman.y)
    else:
        g.dx = random.choice([-GHOST_SPEED, GHOST_SPEED])
        g.dy = random.choice([-GHOST_SPEED, GHOST_SPEED])


def make_ghost_actors():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            if block in ["g", "G"]:
                # Make the sprite in the correct position
                g = Actor(char_to_image[block], (x * BLOCK_SIZE, y * BLOCK_SIZE), anchor=("left", "top"))
                new_ghost_direction(g, GHOST_SPEED)
                ghosts.append(g)
                ghost_start_pos.append((x, y))
                # Now we have the ghost sprite we don't need this block
                world[y] = world[y][:x] + "." + world[y][x + 1 :]


def defualt_text(text, topleft=(0, 0), fontsize=30, fontname="chalkduster", font_color="blue"):
    screen.draw.text(text, topleft=topleft, fontname=fontname, fontsize=fontsize, owidth=1, ocolor=font_color)  # type: ignore # noqa: F821


def draw():
    screen.clear()  # type: ignore # noqa: F821

    if pacman.name_saved and not pacman.initialised:
        defualt_text("Press space to start", topleft=(60, 500))

    if not pacman.initialised:
        screen.draw.rect(BOX, RED)  # type: ignore # noqa: F821
        defualt_text(WELCOME_SCREEN, topleft=(50, 4))
        defualt_text(leaderboard, topleft=(50, 100))
        defualt_text(pacman.player, topleft=(60, 400))
    else:
        for y, row in enumerate(world):
            for x, block in enumerate(row):
                image = char_to_image.get(block, None)
                if image:
                    screen.blit(char_to_image[block], (x * BLOCK_SIZE, y * BLOCK_SIZE))  # type: ignore # noqa: F821
        pacman.draw()
        for g in ghosts:
            g.draw()

        if pacman.banner and pacman.banner_counter > 0:
            screen.draw.text(pacman.banner, center=(WIDTH / 2, HEIGHT / 2), fontsize=80, fontname="chalkduster", owidth=1, ocolor="blue")  # type: ignore # noqa: F821

        screen.draw.text("Score: %s" % pacman.score, topleft=(8, 4), fontsize=40)  # type: ignore # noqa: F821
        screen.draw.text("Lives: %s" % pacman.lives, topright=(WIDTH - 8, 4), fontsize=40)  # type: ignore # noqa: F821


def blocks_ahead_of(sprite, dx, dy):
    """Return a list of tiles at this position + delta"""

    # Here's where we want to move to, bit of rounding to
    # ensure we get the exact pixel position
    x = int(round(sprite.left)) + dx
    y = int(round(sprite.top)) + dy
    # Find integer block pos, using floor (so 4.7 becomes 4)
    ix, iy = int(x // BLOCK_SIZE), int(y // BLOCK_SIZE)
    # Remainder let's us check adjacent blocks
    rx, ry = x % BLOCK_SIZE, y % BLOCK_SIZE
    # Keep in bounds of world
    if ix == WORLD_SIZE - 1:
        rx = 0
    if iy == WORLD_SIZE - 1:
        ry = 0

    blocks = [world[iy][ix]]
    if rx:
        blocks.append(world[iy][ix + 1])
    if ry:
        blocks.append(world[iy + 1][ix])
    if rx and ry:
        blocks.append(world[iy + 1][ix + 1])

    return blocks


def wrap_around(mini, val, maxi):
    if val < mini:
        return maxi
    elif val > maxi:
        return mini
    else:
        return val


def move_ahead(sprite):
    # Record current pos so we can see if the sprite moved
    oldx, oldy = sprite.x, sprite.y

    # In order to go in direction dx, dy there must be no wall that way
    if "=" not in blocks_ahead_of(sprite, sprite.dx, 0):
        sprite.x += sprite.dx
    if "=" not in blocks_ahead_of(sprite, 0, sprite.dy):
        sprite.y += sprite.dy

    # Keep sprite on the screen
    sprite.x = wrap_around(0, sprite.x, WIDTH - BLOCK_SIZE)
    sprite.y = wrap_around(0, sprite.y, HEIGHT - BLOCK_SIZE)

    # Return whether we moved
    moved = oldx != sprite.x or oldy != sprite.y

    # Costume change for pacman
    if moved and sprite == pacman:
        a = 0
        if oldx < sprite.x:
            a = 0
        elif oldy > sprite.y:
            a = 90
        elif oldx > sprite.x:
            a = 180
        elif oldy < sprite.y:
            a = 270
        sprite.angle = a

    return moved


def reset_sprites():
    pacman.x = pacman.y = 1.5 * BLOCK_SIZE
    # Move ghosts back to their start pos
    for g, (x, y) in zip(ghosts, ghost_start_pos):
        g.x = x * BLOCK_SIZE
        g.y = y * BLOCK_SIZE


def set_banner(message, count):
    pacman.banner = message
    pacman.banner_counter = count


def update():
    if pacman.freeze is False:
        move_ahead(pacman)
        eat_food()

        for g in ghosts:
            if g.colliderect(pacman):
                set_banner("Ouch!", 5)
                pacman.lives -= 1
                reset_sprites()
            if not move_ahead(g):
                new_ghost_direction(g, GHOST_SPEED)

        if pacman.lives == 0:
            set_banner("Game Over", 5)
            clock.schedule_unique(new_game, 2)
            pacman.freeze = True
            pacman.lives = 3
            pacman.score = 0


def new_game():
    pacman.freeze = False
    reset_sprites()


def on_key_up(key):
    if key in (keys.LEFT, keys.RIGHT):
        pacman.dx = 0
    if key in (keys.UP, keys.DOWN):
        pacman.dy = 0


def on_key_down(key):
    if key == keys.LEFT:
        pacman.dx = -SPEED
    if key == keys.RIGHT:
        pacman.dx = SPEED
    if key == keys.UP:
        pacman.dy = -SPEED
    if key == keys.DOWN:
        pacman.dy = SPEED
    if not pacman.initialised:
        if not pacman.name_saved:
            if key == keys.BACKSPACE:
                pacman.player = pacman.player[:-1]
            elif key == keys.RETURN and len(pacman.player) > 0:
                pacman.name_saved = True
            elif 65 <= key.value <= 127:
                pacman.player += chr(key.value)

        if pacman.name_saved and key == keys.SPACE:
            pacman.initialised = True
            sounds.pacman_beginning.play()


def periodic():
    if pacman.banner_counter > 0:
        pacman.banner_counter -= 1


# Game set up


check_world()

clock.schedule_interval(periodic, 0.2)

make_ghost_actors()

pgzrun.go()

# End
