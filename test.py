# Importing the library
import pygame

# Initializing Pygame
pygame.init()

# Initializing surface
surface = pygame.display.set_mode((1280, 720))

# Initializing Color
color = (255, 0, 0)

# Drawing Rectangle
rect = pygame.draw.rect(surface, color, (30, 60, 500, 50))
pygame.display.flip()
print(rect.bottomright)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
