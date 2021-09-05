import pygame

pygame.init()

screen_w, screen_h = 448, 720
screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption("Puzzle Boggle")

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False


    pygame.display.update()

pygame.quit()
