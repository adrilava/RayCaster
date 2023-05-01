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
CASTED_RAYS = 480
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = (SCREEN_WIDTH) / CASTED_RAYS
uncalc = 6
wallHeight = 28000
qualityBrut = 10
refList = [1, 3, 9]
debug = False
showMap = False




player_x = (SCREEN_WIDTH / 2) / 2.5
player_y = (SCREEN_WIDTH / 2) / 2.5
player_angle = math.pi

absoluteMapSize = MAP_SIZE*TILE_SIZE

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
    '####### ##          ## #######'
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

clock = pygame.time.Clock()



def draw_map():
    # MAP
    if showMap:
        for row in range(MAP_SIZE):
            for col in range(MAP_SIZE):
                square = row * MAP_SIZE + col


                pygame.draw.rect(
                    win,
                    (0, 0, 102) if MAP[square] == '#' else (0, 0, 0),
                                 ((col * TILE_SIZE) + (SCREEN_WIDTH - (MAP_SIZE * TILE_SIZE)),
                                 (row * TILE_SIZE) + SCREEN_HEIGHT - (MAP_SIZE * TILE_SIZE), TILE_SIZE , TILE_SIZE ),
                                 )

                pygame.draw.circle(win, (255, 211, 0), (
        int(player_x) + (SCREEN_WIDTH - (MAP_SIZE * TILE_SIZE)), int(player_y) + SCREEN_HEIGHT - (MAP_SIZE * TILE_SIZE)),
                           6)  # PLAYER


def cast_rays():
    start_angle = player_angle - HALF_FOV

    rectList = []


    for ray in range(CASTED_RAYS):
        for dephh in range(int(MAX_DEPTH / uncalc)):



            depth = dephh * uncalc



            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)



            cube = row * MAP_SIZE + col

            ################if cube > MAP_SIZE**2 : cube -= MAP_SIZE**2





            if MAP[cube] == '#':



                depth = (dephh - 1) * uncalc


                precision = int((qualityBrut / ((dephh+0.001) * 1.6)))
                if precision < 1: precision = 1


                qList = refList
                if target_x > absoluteMapSize : qList = [1]
                for p in range(len(qList)):
                    for i in range(uncalc * (precision*qList[p])):
                        depth += 1 / (precision*qList[p])
                        target_x = player_x - math.sin(start_angle) * depth
                        target_y = player_y + math.cos(start_angle) * depth
                        col = int(target_x / TILE_SIZE)
                        row = int(target_y / TILE_SIZE)

                        cube = row * MAP_SIZE + col
                        (target_y / TILE_SIZE) * MAP_SIZE + target_x / TILE_SIZE
                        if MAP[cube] == '#':
                            depth-= 1/ precision
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


                wall_height = wallHeight / (depth+0.0001)





                # 3D RENDERING
                first = (SCREEN_HEIGHT + ray * SCALE - (SCREEN_WIDTH / 2) - 120)
                second = ((SCREEN_HEIGHT / 2) - wall_height / 2,SCALE, wall_height)

                rect = pygame.draw.rect(win, (color, color, color), (SCREEN_HEIGHT + ray * SCALE - (SCREEN_WIDTH / 2) - 120, (SCREEN_HEIGHT / 2) - wall_height / 2, SCALE, wall_height), 1)

                rectList.append([col, row, (SCREEN_HEIGHT + ray * SCALE - (SCREEN_WIDTH / 2) - 120, (SCREEN_HEIGHT / 2) - wall_height / 2, SCREEN_HEIGHT + ray * SCALE - (SCREEN_WIDTH / 2) - 120+ SCALE, (SCREEN_HEIGHT / 2) - wall_height / 2+ wall_height), rect])
                # col, row, ( x1, y1, x2, y2 ), rect

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

    # Blue smooth top/bottom


    # rectList build : ([col, row, rect],[...],...)

    listSize = []

    cubePos = rectList[0][0]*100 + rectList[0][1]
    currentCubeSize = 0
    for i in range(len(rectList)):
        cubePosCheck = i
        col = rectList[i][0]
        row = rectList[i][1]
        cubeIPos = col*100 + row
        if i < len(rectList)-1 and (cubeIPos == cubePos or cubeIPos == cubePos-100 or cubeIPos == cubePos+100 or cubeIPos == cubePos + 1 or cubeIPos == cubePos -1) :
            currentCubeSize += 1
        else :
            listSize.append(currentCubeSize)
            currentCubeSize = 0
            cubePos = cubeIPos

    listStartEndWalls = []
    count = 0
    for i in range(len(listSize)):
        listStartEndWalls.append((count, listSize[i]+count))
        count+=listSize[i]+1

    #print(listStartEndWalls)
    for i in range(len(listStartEndWalls)):

        firstRect = rectList[listStartEndWalls[i][0]-1][3]
        firstRectTop = (rectList[listStartEndWalls[i][0]-1][2][0], rectList[listStartEndWalls[i][0]-1][2][1])
        firstRectBot = (rectList[listStartEndWalls[i][0]-1][2][2], rectList[listStartEndWalls[i][0]-1][2][3])

        secondRect = rectList[listStartEndWalls[i][1]-1][3]
        secondRectTop = (rectList[listStartEndWalls[i][1]-1][2][0], rectList[listStartEndWalls[i][1]-1][2][1])
        secondRectBot = (rectList[listStartEndWalls[i][1]-1][2][2],rectList[listStartEndWalls[i][1]-1][2][3])

        if firstRect.x  < secondRect.x:
            pygame.draw.polygon(win, (0, 0, 102), (firstRectTop, secondRectTop, secondRectBot, firstRectBot), 10)








    if debug:
        multip = SCREEN_WIDTH/CASTED_RAYS

        countt = 0
        for i in range(len(listSize)):
            color = (i/len(listSize))*100
            pygame.draw.line(win,(color,color,color), (countt, 100+30*i), (listSize[i]*multip+countt, 100+30*i), 30)
            countt += listSize[i]*multip







forward = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)

    square = row * MAP_SIZE + col
    (player_y / TILE_SIZE) * MAP_SIZE + player_x / TILE_SIZE
    if MAP[square] == '#':
        if forward == True:
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5

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

    if keys[pygame.K_LEFT]: player_angle -= 0.03
    if keys[pygame.K_RIGHT]: player_angle += 0.03
    if keys[pygame.K_UP]:
        forward = True
        player_x += -math.sin(player_angle)
        player_y += math.cos(player_angle)
    if keys[pygame.K_DOWN]:
        forward = False
        player_x -= -math.sin(player_angle)
        player_y -= math.cos(player_angle)


    if player_x > MAP_SIZE*TILE_SIZE : player_x = 5
    if player_x < 1 : player_x = MAP_SIZE*TILE_SIZE-5




    clock.tick(60)

    fps = "Fps : " + str(int(clock.get_fps()))
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(fps, False, (255, 0, 00))
    win.blit(textsurface, (0, 0))
    pygame.display.flip()


