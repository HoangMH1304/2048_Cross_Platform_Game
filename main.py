from pickle import TRUE
from turtle import color
import pygame
import random
pygame.init()

# initial set up: khởi tạo
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT]) # Khởi tạo kích thước cho cửa sổ
pygame.display.set_caption("2048")
timer = pygame.time.Clock()
fps = 30
font = pygame.font.Font('freesansbold.ttf', 24)

# 2048 game color library
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# game variables initialize
board_values = [[2048 for _ in range(4)] for _ in range(4)]  # khởi tạo ma trận toàn 0

# draw background for the board
def draw_board():
    rect = pygame.Rect(0, 0, 400, 400)  # left, top, weight, height
    pygame.draw.rect(screen, colors['bg'], rect, 0, 10)
    # print(f'x={rect.x}, y={rect.y}, w={rect.w}, h={rect.h}')
    # print(f'left={rect.left}, top={rect.top}, right={rect.right}, bottom={rect.bottom}')
    # print(f'center={rect.center}')

# draw tiles for game
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            # print(board[i][j], end=' ')
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [20 + 95 * j, 20 + 95 * i, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))   #not understand...
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)
        # print()


# main game loop
run = TRUE
while run:
    timer.tick(fps)  # thiết lập fps cho game
    screen.fill('gray')  # thiết lập nền xám làm background

    draw_board()
    draw_pieces(board_values)
    for event in pygame.event.get():  # Xét các event khi game chạy
        if event.type == pygame.QUIT:  # Khi ấn vào nút X(close) trên console
            run = False

    pygame.display.flip()  # cập nhật nội dung TOÀN BỘ màn hình
pygame.quit
