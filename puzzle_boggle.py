import pygame
import os
import random
import math
import _map

###################################################################################################################
pygame.init()

SCREEN_W, SCREEN_H = 448, 720
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Puzzle Boggle")
clock = pygame.time.Clock()
PATH = os.path.dirname(__file__)
game_font = pygame.font.SysFont("arialrounded.ttf", 50)

###################################################################################################################


class Cannon(pygame.sprite.Sprite):
    def __init__(self, image, position) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.image0 = image
        self.center = position
        self.angle = 90

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def rotate(self, to_angle):
        self.angle += to_angle
        if self.angle <= MIN_ANGLE:
            self.angle = MIN_ANGLE
        elif self.angle >= MAX_ANGLE:
            self.angle = MAX_ANGLE
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect(center=self.center)


class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position=(0, 0), index=(-1, -1)) -> None:
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)
        self.set_position(position)
        self.index = index

    def set_position(self, position):
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

###################################################################################################################


def bubble_group_draw(screen):
    global shoot_count
    to_x = 0
    if shoot_count == 2:
        to_x = random.randint(-1, 1)
    elif shoot_count == 1:
        to_x = random.randint(-4, 4)

    for bubble in bubble_group:
        bubble.rect.x += to_x
    bubble_group.draw(screen)
    for bubble in bubble_group:
        bubble.rect.x -= to_x


def get_bubble_position(row, col):
    # 버블은 살짝 타원
    y = row * CELL_SIZE + BUBBLE_H//2 + wall_to_y
    x = col * CELL_SIZE + BUBBLE_W//2
    if row % 2 == 1:
        x += CELL_SIZE//2
    return x, y


def get_map_index(pos: tuple):
    x, y = pos
    y -= wall_to_y
    row = y // CELL_SIZE
    if row % 2 == 0:
        col = x // CELL_SIZE
    else:
        x_ = x-CELL_SIZE//2 if x >= CELL_SIZE//2 else 0
        col = x_ // CELL_SIZE
    return row, col


def get_bubble_image_by_color(color="BLACK"):
    if color == "R":
        return bubble_images[0]
    elif color == "B":
        return bubble_images[1]
    elif color == "Y":
        return bubble_images[2]
    elif color == "G":
        return bubble_images[3]
    elif color == "P":
        return bubble_images[4]
    else:
        return bubble_images[-1]


###################################################################################################################
# ## ammo func

def load_ammo_bubbles():
    global next_bubble, curr_bubble

    if next_bubble:
        curr_bubble = next_bubble
        curr_bubble.set_position(cannon.center)
        next_bubble = None
    else:
        curr_bubble = create_bubble(cannon.center)

    if not next_bubble:
        next_bubble = create_bubble((SCREEN_W//4, SCREEN_H-BUBBLE_H//2-10))


def create_bubble(position):
    bubble = get_random_bubble()
    bubble.set_position(position)
    return bubble


def get_random_bubble():
    # 맵에 있는 색상 한정
    colors = []
    for bubble in bubble_group:
        if not (bubble.color in colors):
            colors.append(bubble.color)
    color = random.choice(colors)
    image = get_bubble_image_by_color(color)
    return Bubble(image, color)


def curr_bubble_move():
    rad_angle = math.radians(shoot_angle)
    x, y = curr_bubble.rect.center
    x = x + SHOOT_SPEED * math.cos(rad_angle)
    y = y + SHOOT_SPEED * math.sin(rad_angle) * (-1)
    curr_bubble.set_position((x, y))


def check_wall_bound():
    global shoot_angle
    if curr_bubble.rect.left <= 0:
        curr_bubble.rect.left = 0
        shoot_angle = 180 - shoot_angle
    elif curr_bubble.rect.right >= SCREEN_W:
        curr_bubble.rect.right = SCREEN_W
        shoot_angle = 180 - shoot_angle

###################################################################################################################
# ## collision


def process_collision():
    global curr_bubble, fired, shoot_count

    hit = pygame.sprite.spritecollideany(
        curr_bubble, bubble_group, pygame.sprite.collide_mask)

    if hit or curr_bubble.rect.top < wall_to_y:
        row, col = get_map_index(curr_bubble.rect.center)

        curr_bubble.set_position(get_bubble_position(row, col))
        curr_bubble.index = (row, col)
        bubble_group.add(curr_bubble)
        update_map(row, col, curr_bubble.color)
        bubble_pop()

        fired = False
        curr_bubble = None
        shoot_count -= 1


def bubble_pop():
    # 같은색 3개 이상 제거
    visited.clear()
    search(curr_bubble.index, curr_bubble.color)

    if len(visited) >= 3:
        for index in visited:
            remove_bubble(index)

        # 엮인 버블 처리
        visited.clear()
        for col, v in enumerate(map[0]):
            index = (0, col)
            if bubble_exists(index) and not index in visited:
                search(index)

        # 제거할 버블 = 전체 - 매달린 버블
        all = [bubble.index for bubble in bubble_group]
        to_remove = list(set(all)-set(visited))
        for index in to_remove:
            remove_bubble(index)


def update_map(row, col, color):
    map[row][col] = color


def bubble_exists(index: tuple):
    s = map[index[0]][index[1]]
    if not(s == "." or s == "/"):
        return True


def remove_bubble(index):
    bubble = get_bubble_by_index(index)
    bubble_group.remove(bubble)
    update_map(*index, ".")


def get_adjacent_indices(row, col):
    # 해당셀의 인접셀
    indices = []
    indices.append((row, col+1))
    indices.append((row, col-1))
    indices.append((row+1, col))
    indices.append((row-1, col))
    if row % 2 == 0:
        indices.append((row+1, col-1))
        indices.append((row-1, col-1))
    else:
        indices.append((row+1, col+1))
        indices.append((row-1, col+1))

    indices = [idx for idx in indices if not (
        idx[0] < 0 or idx[0] >= ROWS_COUNT or idx[1] < 0 or idx[1] >= COLUMNS_COUNT)]

    return indices


def get_bubble_by_index(map_index: tuple) -> Bubble:
    for bubble in bubble_group:
        if bubble.index == map_index:
            return bubble


def get_bubble_color(row, col):
    if map[row][col] == "." or map[row][col] == "/":
        return None
    else:
        return map[row][col]


def search(index, color=None):
    # dfs 깊이우선탐색
    visited.append(index)
    indices = get_adjacent_indices(*index)

    for idx in indices:
        c = get_bubble_color(*idx)
        if c and not idx in visited and (not color or color == c):
            search(idx, color)


def too_low():
    for bubble in bubble_group:
        if bubble.rect.bottom > len(map) * CELL_SIZE:
            return True


def set_result(str):
    global result_text, show_result, running
    result_text = game_font.render(str, True, WHITE)
    show_result = True
    running = False

###################################################################################################################
# stage funcs


def set_stage(level):
    global map
    map = _map.load_map(level)
    init_vars()
    set_bubbles()


def init_vars():
    global wall_to_y, shoot_count, curr_bubble, next_bubble
    wall_to_y = 0
    shoot_count = MAX_SHOOT_COUNT
    curr_bubble = None
    next_bubble = None


def set_bubbles():
    for row_idx, row in enumerate(map):
        for col_idx, color in enumerate(row):
            if color in [".", "/"]:
                continue

            image = get_bubble_image_by_color(color)
            position = get_bubble_position(row_idx, col_idx)
            bubble_group.add(
                Bubble(image, color, position, (row_idx, col_idx)))


def drop_wall():
    global wall_to_y, shoot_count
    shoot_count = MAX_SHOOT_COUNT
    wall_to_y += CELL_SIZE
    for bubble in bubble_group:
        bubble.rect.y += CELL_SIZE


###################################################################################################################
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ROWS_COUNT = 11
COLUMNS_COUNT = 8
CELL_SIZE = 56
BUBBLE_W, BUBBLE_H = 56, 62
MIN_ANGLE = 10
MAX_ANGLE = 170
ANGLE_SPEED = 2
SHOOT_SPEED = 15
MAX_SHOOT_COUNT = 5

to_angle_right = 0
to_angle_left = 0
curr_bubble = None
next_bubble = None
fired = False
shoot_angle = 0
shoot_count = MAX_SHOOT_COUNT
visited = []
wall_to_y = 0

background = pygame.image.load(os.path.join(PATH, "background.png"))
wall = pygame.image.load(os.path.join(PATH, "wall.png"))

bubble_images = [
    pygame.image.load(os.path.join(PATH, "red.png")).convert_alpha(),
    pygame.image.load(os.path.join(PATH, "blue.png")).convert_alpha(),
    pygame.image.load(os.path.join(PATH, "yellow.png")).convert_alpha(),
    pygame.image.load(os.path.join(PATH, "green.png")).convert_alpha(),
    pygame.image.load(os.path.join(PATH, "puple.png")).convert_alpha(),
    pygame.image.load(os.path.join(PATH, "black.png")).convert_alpha()]

bubble_group = pygame.sprite.Group()
cannon_image = pygame.image.load(os.path.join(PATH, "cannon.png"))
cannon = Cannon(cannon_image, (SCREEN_W//2, 624))

result_text = None
show_result = False

level = 1
set_stage(level)


###################################################################################################################

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not fired:
            if event.key == pygame.K_LEFT:
                to_angle_left = ANGLE_SPEED
            elif event.key == pygame.K_RIGHT:
                to_angle_right = -ANGLE_SPEED
            elif event.key == pygame.K_SPACE:
                fired = True
                shoot_angle = cannon.angle

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_angle_left = 0
            elif event.key == pygame.K_RIGHT:
                to_angle_right = 0

    if not curr_bubble:
        load_ammo_bubbles()

    if fired:
        curr_bubble_move()
        check_wall_bound()
        process_collision()

    if too_low():
        for bubble in bubble_group:
            bubble.image = get_bubble_image_by_color()
        set_result("Game Over")

    if not bubble_group:
        # if len(bubble_group) == 0:
        level += 1
        if _map.map_exists(level):
            set_stage(level)
        else:
            set_result("Mission Complete")

    cannon.rotate(to_angle_left+to_angle_right)

    screen.blit(background, (0, 0))
    bubble_group_draw(screen)

    if shoot_count == 0:
        drop_wall()
    screen.blit(wall, (0, -SCREEN_H+wall_to_y))

    cannon.draw(screen)
    if curr_bubble:
        curr_bubble.draw(screen)
    if next_bubble:
        next_bubble.draw(screen)

    if show_result:
        screen.blit(result_text, result_text.get_rect(
            center=screen.get_rect().center))

    pygame.display.update()

pygame.time.delay(2000)
pygame.quit()
