import pygame
import random

pygame.init()

display_width = 300
display_height = 450

pygame.mouse.set_cursor(*pygame.cursors.broken_x)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Space Invaders")

# LOADING ALL THE IMAGES
BG = pygame.image.load("spaceBG.png")
UFO = pygame.image.load("ufo_pixel.png")
ASTEROID = pygame.image.load("asteroid_pixel.png")
HEART = pygame.image.load("heart_pixel.png")
PLAY_BUTTON = pygame.image.load("play.png")
HOME_SCREEN = pygame.image.load("thumbnail.png")
END_SCREEN = pygame.image.load("endscreen.png")

# LOADING THE BACKGROUND MUSIC
pygame.mixer.music.load("bittyMix.mp3")
pygame.mixer.music.play(-1, 0.0)

clock = pygame.time.Clock()
FPS = 20


def startScreen():
    click = False
    while not click:
        mouse_pos = pygame.mouse.get_pos()
        # print(str(mouse_pos[0]) + ", " + str(mouse_pos[1]))
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 60 < mouse_pos[0] < 240 and 285 < mouse_pos[1] < 360:
                    gameLoop()
        gameDisplay.blit(HOME_SCREEN, [0, 0])
        pygame.display.update()


def endScreen():
    replay = False
    while not replay:
        gameDisplay.blit(END_SCREEN, [0, 0])
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Replay button
                if 155 < mouse_pos[0] < 255 and 270 < mouse_pos[1] < 300:
                    replay = True
                elif 155 < mouse_pos[0] < 255 and 320 < mouse_pos[1] < 355:
                    pygame.quit()
                    quit()

        pygame.display.update()
    gameLoop()


def gameLoop():
    # asteroid belt, positions
    belt_x = []
    belt_y = []

    y_change = 10
    lives = 5
    ufo_y_pos = display_height - 75
    # initial number of asteroids
    INIT_AST = 3
    gameOver = False

    levels = []
    for level in range(11):
        levels.append(display_height * (-1 - (level**2)))
        # levels.append(display_height * (-1 - ((level + 1) ** 2)))

    """
    PRINTS EACH LEVEL'S LENGTH AND # OF ASTEROIDS  
    print(levels)
    for x in range(10):
        print(1 * (x**2))
    """

    # RANDOM ASTEROID POSITION GENERATOR
    for level in range(10):
        for asteroids in range(INIT_AST * ((level + 1)**2)):
            belt_x.append(random.randrange(0, display_width - 20))
            # display height * variable that increases per every increasing # of asteroids
            belt_y.append(random.randrange(levels[level + 1], levels[level]))

    while not gameOver:

        mouse_pos = pygame.mouse.get_pos()
        x_pos = mouse_pos[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # DRAWING BG AND UFO
        gameDisplay.blit(BG, [0, 0])
        gameDisplay.blit(UFO, [x_pos - 30, ufo_y_pos])

        # DRAWING ASTEROIDS
        for asteroid in range(len(belt_x)):
            gameDisplay.blit(ASTEROID, [belt_x[asteroid], belt_y[asteroid]])
            belt_y[asteroid] += y_change

        # DRAWING HEART
        for heart in range(lives):
            gameDisplay.blit(HEART, [display_width - 30 - (30 * heart), 10])

        # IMPLEMENTING ASTEROID COLLISION
        asteroid_count = 0
        for asteroid in belt_y:
            if ufo_y_pos < asteroid < ufo_y_pos + 30:
                print(str(belt_x[asteroid_count]) + " -> " + str(x_pos))
                # took me longer to write this next line than it did to write rest of program, trouble with accuracy
                # (x_pos + 40 > belt_x[asteroid_count] > x_pos)
                if x_pos > belt_x[asteroid_count] > x_pos - 40:
                    lives -= 1
                    belt_x[asteroid_count] = display_width
                    belt_y[asteroid_count] = display_height

            """
            Attempt at removing asteroids after leaving the screen
            if asteroid > display_height:
                belt_x.remove(belt_x[asteroid_count])
                belt_y.remove(belt_y[asteroid_count])
            """

            asteroid_count += 1

        # GAME OVER
        if lives == 0:
            # ideally there will be a game over screen
            gameOver = True

        # print(x_pos)
        clock.tick(FPS)
        pygame.display.update()

    endScreen()


startScreen()
