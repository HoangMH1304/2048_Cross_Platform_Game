try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass

import pygame
import random
import asyncio

pygame.init()

# initial set up: khởi tạo
WIDTH = 400
HEIGHT = 500
# Khởi tạo kích thước cho cửa sổ
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("2048 Nhóm 4")
timer = pygame.time.Clock()
fps = 30
font = pygame.font.Font('Assets/Fonts/FreeSansBold.ttf', 24)

# 2048 game color library
colors = {0: (204, 192, 179),  # không hiển thị số 0
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
          'light text': (249, 246, 242),  # màu chữ từ 2 - 8
          'dark text': (119, 110, 101),  # màu chữ 8 - 2048
          'other': (0, 0, 0),  # số lớn hơn 2048
          'bg': (187, 173, 160)}

# game variables initialize
board_values = [[0 for _ in range(5)]
                for _ in range(5)]  # khởi tạo ma trận toàn 0
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('2048_Scripts/high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high

# draw game over and restart text (step 7)


def draw_over():
    pygame.draw.rect(screen, 'black', [50, 200, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 215))
    screen.blit(game_over_text2, (70, 255))

# take your turn base on direction (step 5)


def take_turn(direction, board):
    # global score
    merged = [[False for _ in range(5)] for _ in range(5)]

    if direction == 'UP':
        turn_up(board, merged)
    elif direction == 'DOWN':
        turn_down(board, merged)
    elif direction == 'LEFT':
        turn_left(board, merged)
    else:
        turn_right(board, merged)
    return board


def turn_up(board, merged):
    global score
    for i in range(5):
        for j in range(5):
            shift = 0
            if i > 0:
                for k in range(i):
                    if board[k][j] == 0:
                        shift += 1
                if shift > 0:
                    board[i - shift][j] = board[i][j]
                    board[i][j] = 0
                if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift - 1][j] \
                        and not merged[i - shift][j]:
                    board[i - shift - 1][j] *= 2
                    score += board[i - shift - 1][j]
                    board[i - shift][j] = 0
                    merged[i - shift - 1][j] = True


def turn_down(board, merged):
    global score
    for i in range(4):
        for j in range(5):
            shift = 0
            for k in range(i + 1):
                if board[4 - k][j] == 0:
                    shift += 1
            if shift > 0:
                board[3 - i + shift][j] = board[3 - i][j]
                board[3 - i][j] = 0
            if 4 - i + shift <= 4:
                if board[3 - i + shift][j] == board[4 - i + shift][j] and not merged[4 - i + shift][j] \
                        and not merged[3 - i + shift][j]:
                    board[4 - i + shift][j] *= 2
                    score += board[4 - i + shift][j]
                    # score += board[3 - i + shift][j]
                    board[3 - i + shift][j] = 0
                    merged[4 - i + shift][j] = True


def turn_left(board, merged):
    global score
    for i in range(5):
        for j in range(5):
            shift = 0
            for k in range(j):
                if board[i][k] == 0:
                    shift += 1
            if shift > 0:
                board[i][j - shift] = board[i][j]
                board[i][j] = 0
            if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                    and not merged[i][j - shift]:
                board[i][j - shift - 1] *= 2
                score += board[i][j - shift - 1]
                # score += board[i][j - shift - 1]
                board[i][j - shift] = 0
                merged[i][j - shift - 1] = True


def turn_right(board, merged):
    global score
    for i in range(5):
        for j in range(5):
            shift = 0
            for k in range(j):
                if board[i][4 - k] == 0:
                    shift += 1
            if shift > 0:
                board[i][4 - j + shift] = board[i][4 - j]
                board[i][4 - j] = 0
            if 5 - j + shift <= 4:
                if board[i][5 - j + shift] == board[i][4 - j + shift] and not merged[i][5 - j + shift] \
                        and not merged[i][4 - j + shift]:
                    board[i][5 - j + shift] *= 2
                    score += board[i][5 - j + shift]
                    board[i][4 - j + shift] = 0
                    merged[i][5 - j + shift] = True

# spawn in new pieces randomly when turns start: sinh ngẫu nhiên số và cập nhật lại bảng trong 1 lần


def new_pieces(board):
    count = 0
    full = True
    # kiểm tra xem có thể sinh số thêm được không
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 4)
        col = random.randint(0, 4)
        if board[row][col] == 0:
            # Sẽ có 10% sinh ra số 4, còn lại chỉ sinh ra số 2
            count += 1
            full = False
            if random.randint(1, 10) == 1:
                board[row][col] = 4
            else:
                board[row][col] = 2
    return board, full

# draw background for the board


def draw_board():
    rect = pygame.Rect(0, 0, 400, 400)  # left, top, weight, height
    pygame.draw.rect(screen, colors['bg'], rect, 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    # print(f'x={rect.x}, y={rect.y}, w={rect.w}, h={rect.h}')
    # print(f'left={rect.left}, top={rect.top}, right={rect.right}, bottom={rect.bottom}')
    # print(f'center={rect.center}')

# draw tiles for game


def draw_pieces(board):
    for i in range(5):
        for j in range(5):
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
            pygame.draw.rect(
                screen, color, [10 + 78 * j, 10 + 78 * i, 68, 68], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font(
                    'Assets/Fonts/FreeSansBold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(
                    center=(j * 78 + 44, i * 78 + 44))  # hard code
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [10 + 78 * j, 10 + 78 * i, 68, 68], 2, 5)
        # print()


# main game loop

async def main():
    global colors, board_values, game_over, spawn_new, init_count, direction, score, file, init_high, high_score
    run = True
    global color
    while run:
        timer.tick(fps)  # thiết lập fps cho game
        screen.fill('gray')  # thiết lập nền xám làm background
        draw_board()
        draw_pieces(board_values)

        if direction != '':
            board_values = take_turn(direction, board_values)
            direction = ''
            spawn_new = True

        if spawn_new or init_count < 2:
            board_values, game_over = new_pieces(board_values)
            spawn_new = False
            init_count += 1

        if game_over:
            draw_over()
            if high_score > init_high:
                file = open('2048_py/high_score', 'w')
                file.write(f'{high_score}')
                file.close()
                init_high = high_score

        for event in pygame.event.get():  # Xét các event khi game chạy
            # Khi ấn vào nút X(close) trên console
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                global opos 
                opos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                v = pygame.Vector2(event.pos) - pygame.Vector2(opos)
                print("vector swipe: ", v)
                
                if abs(v.x) > abs(v.y):
                    v.y = 0
                    if abs(v.x) < 50: continue
                else:
                    v.x = 0
                    if abs(v.y) < 50: continue

                
                if v.x > 0:
                    direction = 'RIGHT'
                elif v.x < 0:
                    direction = 'LEFT'
                elif v.y > 0:
                    direction = 'DOWN'
                elif v.y < 0:
                    direction = 'UP'

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    direction = 'UP'
                if event.key == pygame.K_DOWN:
                    direction = 'DOWN'
                if event.key == pygame.K_LEFT:
                    direction = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'
                
               

                if game_over:
                    if event.key == pygame.K_RETURN:
                        board_values = [[0 for _ in range(5)] for _ in range(5)]
                        spawn_new = True
                        init_count = 0
                        score = 0
                        direction = ''
                        game_over = False

        if score > high_score:
            high_score = score
        pygame.display.flip()  # cập nhật nội dung TOÀN BỘ màn hình
        # pygame.quit  build for pc
        await asyncio.sleep(0)
        # if not run:
        #     pygame.quit()
        #     return

asyncio.run(main())
