import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
purple = (128, 0, 128)
orange = (255, 165, 0)
blue = (0, 0, 255)
green = (0, 128, 0)

width = 300
height = 600
cell_size = 30

game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

shapes = [
    [[1, 1, 1, 1]],                  # I
    [[1, 1], [1, 1]],                # O
    [[0, 1, 0], [1, 1, 1]],          # T
    [[1, 0, 0], [1, 1, 1]],          # L
    [[0, 0, 1], [1, 1, 1]],          # J
    [[0, 1, 1], [1, 1, 0]],          # S
    [[1, 1, 0], [0, 1, 1]]           # Z
]

shape_colors = [cyan, yellow, purple, orange, blue, green, red]


class Piece:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color


def create_grid(locked_positions=None):
    if locked_positions is None:
        locked_positions = {}

    grid = [[black for _ in range(10)] for _ in range(20)]

    for (x, y), color in locked_positions.items():
        if 0 <= y < 20 and 0 <= x < 10:
            grid[y][x] = color

    return grid


def draw_grid(surface, grid, score):
    surface.fill(black)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (j * cell_size, i * cell_size, cell_size, cell_size))

    for i in range(21):
        pygame.draw.line(surface, white, (0, i * cell_size), (width, i * cell_size))

    for j in range(11):
        pygame.draw.line(surface, white, (j * cell_size, 0), (j * cell_size, height))

    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, white)
    surface.blit(score_text, (10, 10))

def convert_shape_format(piece):
    positions = []

    for i, line in enumerate(piece.shape):
        for j, value in enumerate(line):
            if value == 1:
                positions.append((piece.x + j, piece.y + i))

    return positions


def valid_space(piece, grid):
    positions = convert_shape_format(piece)

    for x, y in positions:
        if x < 0 or x >= 10 or y >= 20:
            return False
        if y >= 0 and grid[y][x] != black:
            return False

    return True

def clear_rows(grid, locked):
    rows_to_clear = []

    for i in range(len(grid)):
        if black not in grid[i]:
            rows_to_clear.append(i)

    if len(rows_to_clear) > 0:
        for row in rows_to_clear:
            for col in range(10):
                try:
                    del locked[(col, row)]
                except:
                    continue

        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            shift = sum(1 for row in rows_to_clear if y < row)
            if shift > 0:
                new_key = (x, y + shift)
                locked[new_key] = locked.pop(key)

    return len(rows_to_clear)

def check_lost(locked):
    for x, y in locked:
        if y < 1:
            return True
    return False

def draw_game_over(surface, score):
    surface.fill(black)

    font1 = pygame.font.SysFont("Arial", 36)
    font2 = pygame.font.SysFont("Arial", 24)

    text1 = font1.render("Game Over", True, red)
    text2 = font2.render(f"Final Score: {score}", True, white)
    text3 = font2.render("Press R to Restart", True, white)
    text4 = font2.render("Press Q to Quit", True, white)

    surface.blit(text1,(60, 220))
    surface.blit(text2,(75, 270))
    surface.blit(text3,(55, 320))
    surface.blit(text4,(75, 360))

    pygame.display.update()

def main():
    locked_positions = {}
    current_piece = Piece(3, 0, random.choice(shapes), random.choice(shape_colors))
    clock = pygame.time.Clock()
    run = True

    fall_time = 0
    fall_speed = 500
    score = 0
    game_over = False

    while run:
        grid = create_grid(locked_positions)
        dt = clock.tick(30)

        if not game_over:
            fall_time += dt

            if fall_time >= fall_speed:
                fall_time = 0
                current_piece.y += 1

                if not valid_space(current_piece, grid):
                    current_piece.y -= 1

                    for pos in convert_shape_format(current_piece):
                        locked_positions[pos] = current_piece.color

                    cleared = clear_rows(grid, locked_positions)
                    score += cleared * 10

                    current_piece = Piece(3, 0, random.choice(shapes), random.choice(shape_colors))

                    if check_lost(locked_positions):
                        game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1

                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1

                    elif event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1

                    elif event.key == pygame.K_UP:
                        old_shape = current_piece.shape
                        current_piece.shape = [list(row) for row in zip(*current_piece.shape[::-1])]
                        if not valid_space(current_piece, grid):
                            current_piece.shape = old_shape

                else:
                    if event.key == pygame.K_r:
                        main()
                        return
                    elif event.key == pygame.K_q:
                        run = False

        if not game_over:
            for x, y in convert_shape_format(current_piece):
                if 0 <= y < 20 and 0 <= x < 10:
                    grid[y][x] = current_piece.color

            draw_grid(game_window, grid, score)
        else:
            draw_game_over(game_window, score)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()