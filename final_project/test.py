import pygame
import time
import os

pygame.init()
screen = pygame.display.set_mode((600, 600))
done = False

happy = pygame.image.load(os.path.join("texture", "Hero.png"))

checkers = pygame.image.load(os.path.join("texture", "Hero.png"))  # 32x32 repeating checkered image

while not done:
    start = time.time()
    # pump those events!
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
    # checker the background
    # x = 0
    # while x < 300:
    #     y = 0
    #     while y < 300:
    #         screen.blit(checkers, (x, y))
    #         y += 32
    #     x += 32

    # here comes the protagonist
    screen.blit(happy, (100, 100))

    pygame.display.flip()

    # yeah, I know there's a pygame clock method
    # I just like the standard threading sleep
    end = time.time()
    diff = end - start
    framerate = 30
    delay = 1.0 / framerate - diff
    if delay > 0:
        time.sleep(delay)