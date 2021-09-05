import pygame
import os
from _my import *



##############################################################
pygame.init()
screen_w, screen_h = 448, 720
screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption("Puzzle Boggle")
clock = pygame.time.Clock()

##############################################################

class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position) -> None:
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)

def get_position(row, col):
    y = row * CELL_SIZE + BUBBLE_H//2 
    x = col * CELL_SIZE + BUBBLE_W//2
    if row%2==1 : x+= CELL_SIZE//2
    print(row, col, x,y)
    return x, y

def get_image(color):
    if color == "R" :
        return bubble_images[0]
    elif color == "B" :
        return bubble_images[1]
    elif color == "Y" :
        return bubble_images[2]
    elif color == "G" :
        return bubble_images[3]    
    elif color == "P" :
        return bubble_images[4]
    elif color == "B" :
        return bubble_images[-1]

def map_load():
    for row_idx , row in enumerate(map):
        for col_idx, color in enumerate(row):
            if color in [".","/"]: continue

            image = get_image(color)
            position = get_position(row_idx, col_idx)
            bubble_group.add(Bubble(image, color, position))

##############################################################

path = os.path.dirname(__file__)

background = pygame.image.load(os.path.join(path, "background.png"))

bubble_images = [
    pygame.image.load(os.path.join(path, "red.png")).convert_alpha(),
    pygame.image.load(os.path.join(path, "blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(path, "yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(path, "green.png")).convert_alpha(),
    pygame.image.load(os.path.join(path, "puple.png")).convert_alpha(),
    pygame.image.load(os.path.join(path, "black.png")).convert_alpha()]

# 56x62
CELL_SIZE = 56
BUBBLE_W, BUBBLE_H = 56, 62
bubble_grid = []
bubble_group = pygame.sprite.Group()

map = [
    list("RRYYBBGG"),
    list("RRYYBBG/"),
    list("BBGGRRYY"),
    list("BBGGRRY/"),
    list("........"),
    list("......./"),
    list("........"),
    list("......./"),
    list("........"),
    list("......./"),
    list("........")]

map_load()


##############################################################

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0,0))
    bubble_group.draw(screen)
    pygame.display.update()

pygame.quit()
