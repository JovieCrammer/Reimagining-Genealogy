import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 800
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reimagining Genealogy")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(0)

    # draw one circle
    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (500, 350),
        8
    )

    # display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
