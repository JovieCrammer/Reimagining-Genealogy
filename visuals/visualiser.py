import pygame
from visuals.node import Node

pygame.init()

WIDTH, HEIGHT = 1000, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reimagining Genealogy")
clock = pygame.time.Clock()

nodes = [Node(None, WIDTH/2, HEIGHT/2)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(0)

    for node in nodes:
        node.update()
        node.draw(screen)

    # display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
