import pygame
import sys
import math

pygame.init()

SCREEN_HEIGHT = pygame.display.Info().current_h  # 480
SCREEN_WIDTH = pygame.display.Info().current_w  # 480 × 2
MAP_SIZE = 30
TILE_SIZE = ((SCREEN_WIDTH / 2) / MAP_SIZE) - 7
MAX_DEPTH = 750
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 240
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = (SCREEN_WIDTH) / CASTED_RAYS
uncalc = 6
wallHeight = 28000
qualityBrut = 10
refList = [1, 3, 9]
debug = False
showMap = True
screenPatch = -180  # 120 - 180
maxSpeed = 100

multiplyScreen = 17  # 17 - 25

player_x = (SCREEN_WIDTH / 2) / 2.5
player_y = (SCREEN_WIDTH / 2) / 2.2
player_angle = -math.pi / 2
targetAngle = -math.pi / 2

divideSpeedMax = maxSpeed / 100
absoluteMapSize = MAP_SIZE * TILE_SIZE

MAP = (
    '##############################'
    '##            ##            ##'
    '## #### ##### ## ##### #### ##'
    '## #### ##### ## ##### #### ##'
    '## #### ##### ## ##### #### ##'
    '##                          ##'
    '## #### ## ######## ## #### ##'
    '## #### ## ######## ## #### ##'
    '##      ##    ##    ##      ##'
    '####### ##### ## ##### #######'
    '####### ##### ## ##### #######'
    '####### ##          ## #######'
    '####### ## ###  ### ## #######'
    ' ###### ## #      # ## ###### '
    '           #      #           '
    ' ###### ## #      # ## ###### '
    '####### ## ######## ## #######'
    '####### ##     +    ## #######'
    '####### ## ######## ## #######'
    '####### ## ######## ## #######'
    '##            ##            ##'
    '## #### ##### ## ##### #### ##'
    '## #### ##### ## ##### #### ##'
    '##   ##                ##   ##'
    '#### ## ## ######## ## ## ####'
    '##      ##    ##    ##      ##'
    '## ########## ## ########## ##'
    '## ########## ## ########## ##'
    '##                          ##'
    '##############################'
)
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("3D Pac man")


def move(dir, MAP):
    while dir > 4: dir - 4

    index = MAP.index("+")

    if dir == 0: newPos = index - 30
    if dir == 1: newPos = index + 1
    if dir == 2: newPos = index + 30
    if dir == 3: newPos = index - 1

    if MAP[newPos] == " ":
        MAP = MAP[:index] + " " + MAP[index + 1:]

        MAP = MAP[:newPos] + "+" + MAP[newPos + 1:]

    return MAP


def draw_map():
    # MAP
    if showMap:
        for row in range(MAP_SIZE):
            for col in range(MAP_SIZE):
                square = row * MAP_SIZE + col

                if MAP[square] == "^":
                    color = (200, 0, 102)
                elif MAP[square] == "+":
                    color = (50, 50, 50)
                elif MAP[square] == "#":
                    color = (0, 0, 102)
                else:
                    color = (0, 0, 0)

                pygame.draw.rect(
                    win,
                    color,
                    ((col * TILE_SIZE) + (SCREEN_WIDTH - (MAP_SIZE * TILE_SIZE)),
                     (row * TILE_SIZE) + SCREEN_HEIGHT - (MAP_SIZE * TILE_SIZE), TILE_SIZE, TILE_SIZE),
                )

                pygame.draw.circle(win, (255, 211, 0), (
                    int(player_x) + int(SCREEN_WIDTH - (MAP_SIZE * TILE_SIZE)),
                    int(player_y) + SCREEN_HEIGHT - int(MAP_SIZE * TILE_SIZE)),
                                   6)  # PLAYER


def cast_rays():
    start_angle = player_angle - HALF_FOV

    for ray in range(CASTED_RAYS):
        for dephh in range(int(MAX_DEPTH / uncalc)):

            depth = dephh * uncalc

            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)

            cube = row * MAP_SIZE + col

            if MAP[cube] == '#':

                depth = (dephh - 1) * uncalc

                precision = int((qualityBrut / ((dephh + 1) * 1.6)))
                if precision < 1: precision = 1

                qList = refList
                if target_x > absoluteMapSize: qList = [1]
                for p in range(len(qList)):
                    for i in range(uncalc * (precision * qList[p])):
                        depth += 1 / (precision * qList[p])
                        target_x = player_x - math.sin(start_angle) * depth
                        target_y = player_y + math.cos(start_angle) * depth
                        col = int(target_x / TILE_SIZE)
                        row = int(target_y / TILE_SIZE)

                        cube = row * MAP_SIZE + col
                        (target_y / TILE_SIZE) * MAP_SIZE + target_x / TILE_SIZE
                        if MAP[cube] == '#':
                            depth -= 1 / precision
                            break

                # REMOVE CORNER BUG
                target_x = player_x - math.sin(start_angle) * (depth + (uncalc + 0.5))
                target_y = player_y + math.cos(start_angle) * (depth + (uncalc + 0.5))
                colCheckCorner = int(target_x / TILE_SIZE)
                rowCheckCorner = int(target_y / TILE_SIZE)
                squareCheckCorner = rowCheckCorner * MAP_SIZE + colCheckCorner
                if MAP[squareCheckCorner] != '#': continue

                color = 50 / (1 + depth * depth * 0.0001)

                # Fix fish eye effect
                depth *= math.cos(player_angle - start_angle)

                wall_height = wallHeight / (depth + 0.0001)

                # 3D RENDERING

                pygame.draw.rect(win, (color, color, color), (
                SCREEN_HEIGHT + ray * SCALE - (SCREEN_WIDTH / 2) + screenPatch, (SCREEN_HEIGHT / 2) - wall_height / 2,
                SCALE, wall_height), )

                # DEBUG
                if debug == True:
                    pygame.draw.rect(win, (0, 255, 0), (col * TILE_SIZE + (SCREEN_WIDTH - (MAP_SIZE * TILE_SIZE)),
                                                        row * TILE_SIZE + SCREEN_HEIGHT - (MAP_SIZE * TILE_SIZE),
                                                        TILE_SIZE,
                                                        TILE_SIZE))
                    line = pygame.draw.line(win, (255, 10, 255), (player_x + (SCREEN_WIDTH - (MAP_SIZE * TILE_SIZE)),
                                                                  player_y + SCREEN_HEIGHT - (MAP_SIZE * TILE_SIZE)), (
                                                target_x + (SCREEN_WIDTH - (MAP_SIZE * TILE_SIZE)),
                                                target_y + SCREEN_HEIGHT - (MAP_SIZE * TILE_SIZE)))

                break

        start_angle += STEP_ANGLE


forward = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    pygame.draw.rect(win, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

    pygame.draw.rect(win, (100, 100, 100), (0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(win, (200, 200, 200), (0, -SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT))

    # SAVE PLAYER LOCATION
    backupX = float(player_x)
    backupY = float(player_y)

    if debug:
        draw_map()
        cast_rays()
    else:
        cast_rays()
        draw_map()

    player_x = backupX
    player_y = backupY

    keys = pygame.key.get_pressed()

    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)

    square = row * MAP_SIZE + col
    (player_y / TILE_SIZE) * MAP_SIZE + player_x / TILE_SIZE

    if keys[pygame.K_LEFT]:
        if not forward:
            MAP = move(3, MAP)
            forward = True
            targetAngle = math.pi / 2
    elif keys[pygame.K_RIGHT]:
        if not forward:
            MAP = move(1, MAP)
            forward = True
            targetAngle = -math.pi / 2
    elif keys[pygame.K_UP]:
        if not forward:
            MAP = move(0, MAP)
            forward = True
            targetAngle = math.pi
    elif keys[pygame.K_DOWN]:
        if not forward:
            MAP = move(2, MAP)
            forward = True
            targetAngle = 0

    xTarget = (MAP.index("+") % 30 + 0.5) * multiplyScreen
    yTarget = (MAP.index("+") // 30 + 0.5) * multiplyScreen

    if player_x + divideSpeedMax < xTarget:
        player_x += divideSpeedMax
    elif player_x - divideSpeedMax > xTarget:
        player_x -= divideSpeedMax
    if player_y + divideSpeedMax < yTarget:
        player_y += divideSpeedMax
    elif player_y - divideSpeedMax > yTarget:
        player_y -= divideSpeedMax
    if player_angle + 0.1 < targetAngle:
        player_angle += 0.1
    elif player_angle - 0.1 > targetAngle:
        player_angle -= 0.1
    else:
        player_angle = targetAngle

    if not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[
        pygame.K_RIGHT]: forward = False

    if player_x > MAP_SIZE * TILE_SIZE: player_x = 5
    if player_x < 1: player_x = MAP_SIZE * TILE_SIZE - 5

    pygame.display.flip()
