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
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("2048 Nhóm 4")
timer = pygame.time.Clock()
fps = 30
font = pygame.font.Font('Assets/Fonts/FreeSansBold.ttf', 24)
next_scene = False
block = False
matrix_size = 4

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
board_values = [[0 for _ in range(matrix_size)]
                for _ in range(matrix_size)]  # khởi tạo ma trận toàn 0
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('2048_Scripts/high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high
rect_op1 = pygame.Rect(80, 180, 100, 50)
rect_op2 = pygame.Rect(220, 180, 100, 50)
rect_op3 = pygame.Rect(80, 280, 100, 50)
rect_op4 = pygame.Rect(220, 280, 100, 50)

def init():
    global board_values, block_tile_col_index, block_tile_row_index, \
        game_over, spawn_new, init_count, direction, score
    board_values = [[0 for _ in range(matrix_size)]
                for _ in range(matrix_size)]  # khởi tạo ma trận toàn 0
    block_tile_row_index = random.randint(0, matrix_size - 1)
    block_tile_col_index = random.randint(0, matrix_size - 1)
    if block == True: board_values[block_tile_row_index][block_tile_col_index] = 1
    game_over = False
    spawn_new = True
    init_count = 0
    direction = ''
    score = 0

# take your turn base on direction (step 5)
def take_turn(direction, board):
    merged = [[False for _ in range(matrix_size)] for _ in range(matrix_size)]
    if block: merged[block_tile_row_index][block_tile_col_index] = True
    print('isBlock: ', block)
    if direction == 'UP':
        turn_up(board, merged)
    elif direction == 'DOWN':
        turn_down(board, merged)
    elif direction == 'LEFT':
        turn_left(board, merged)
    else:
        turn_right(board, merged)
    return board

def check_turn_up(board):
    idx = -1
    for j in range(matrix_size):
        for i in range(matrix_size):
            if board[i][j] <= 1: continue
            if i == matrix_size - 1:
                if board[i - 1][j] == 0 and idx == -1:
                    idx = j
                    continue
            for k in range(i + 1, matrix_size):
                if i > 0 and board[i - 1][j] == 0 and idx == -1: 
                    idx = j
                if board[i][j] != board[k][j] and board[k][j] != 0:
                    break
                if board[i][j] == board[k][j]:
                    return j
    return idx

def turn_up(board, merged):
    print('choose col: ', check_turn_up(board))
    global score
    n = check_turn_up(board)
    if n == -1: return
    for i in range(matrix_size):
        shift = 0
        if i > 0 and board[i][n] != 1:
            for k in range(i):
                if board[k][n] == 0:
                    shift += 1
                if board[k][n] == 1:
                    shift = 0
            if shift > 0:
                board[i - shift][n] = board[i][n]
                board[i][n] = 0
            if i - shift - 1 < 0:
                continue
            if board[i - shift - 1][n] == board[i - shift][n] and not merged[i - shift - 1][n] \
                    and not merged[i - shift][n]:
                board[i - shift - 1][n] *= 2
                score += board[i - shift - 1][n]
                board[i - shift][n] = 0
                merged[i - shift - 1][n] = True

def check_turn_down(board):
    idx = -1
    for j in range(matrix_size):
        for i in range(matrix_size - 1, -1, -1):
            if board[i][j] <= 1: continue
            if i == 0:
                if board[i + 1][j] == 0 and idx == -1:
                    idx = j
                    continue
            for k in range(i - 1, -1 , -1):
                if i < matrix_size - 1 and board[i + 1][j] == 0 and idx == -1: 
                    idx = j
                if board[i][j] != board[k][j] and board[k][j] != 0:
                    break
                if board[i][j] == board[k][j]:
                    return j
    return idx

def turn_down(board, merged):
    print('choose col: ', check_turn_down(board))
    n = check_turn_down(board)
    if n == -1: return
    global score

    for i in range(matrix_size - 1, -1 , -1):
        shift = 0
        if i < matrix_size - 1 and board[i][n] != 1:
            for k in range(matrix_size - 1, i, -1):
                if board[k][n] == 0:
                    shift += 1
                if board[k][n] == 1:
                    shift = 0
            if shift > 0:
                board[i + shift][n] = board[i][n]
                board[i][n] = 0
            if i + shift + 1 >= matrix_size:
                continue
            if board[i + shift + 1][n] == board[i + shift][n] and not merged[i + shift + 1][n] \
                    and not merged[i + shift][n]:
                board[i + shift + 1][n] *= 2
                score += board[i + shift + 1][n]
                board[i + shift][n] = 0
                merged[i + shift + 1][n] = True

def check_turn_left(board):
    idx = -1
    for i in range(matrix_size):
        for j in range(matrix_size):
            if board[i][j] <= 1: continue
            if j == matrix_size - 1:
                if board[i][j - 1] == 0 and idx == -1:
                    idx = i
                    continue
            for k in range(j + 1, matrix_size):
                if j > 0 and board[i][j - 1] == 0 and idx == -1: 
                    idx = i
                if board[i][j] != board[i][k] and board[i][k] != 0:
                    break
                if board[i][j] == board[i][k]:
                    return i
    return idx

def turn_left(board, merged):
    print('choose row: ', check_turn_left(board))
    global score
    n = check_turn_left(board)
    if n == -1: return
    for j in range(matrix_size):
        shift = 0
        if j > 0 and board[n][j] != 1:
            for k in range(j):
                if board[n][k] == 0:
                    shift += 1
                if board[n][k] == 1:
                    shift = 0
            if shift > 0:
                board[n][j - shift] = board[n][j]
                board[n][j] = 0
            if j - shift - 1 < 0:
                continue
            if board[n][j - shift - 1] == board[n][j - shift] and not merged[n][j - shift - 1] \
                    and not merged[n][j - shift]:
                board[n][j - shift - 1] *= 2
                score += board[n][j - shift - 1]
                board[n][j - shift] = 0
                merged[n][j - shift - 1] = True

def check_turn_right(board):
    idx = -1
    for i in range(matrix_size):
        for j in range(matrix_size - 1, -1, -1):
            if board[i][j] <= 1: continue
            if j == 0:
                if board[i][j + 1] == 0 and idx == -1:
                    idx = i
                    continue
            for k in range(j - 1, -1 , -1):
                if j < matrix_size - 1 and board[i][j + 1] == 0 and idx == -1: 
                    idx = i
                if board[i][j] != board[i][k] and board[i][k] != 0:
                    break
                if board[i][j] == board[i][k]:
                    return i
    return idx

def turn_right(board, merged):
    print('choose row: ', check_turn_right(board))
    n = check_turn_right(board)
    if n == -1: return
    global score

    for j in range(matrix_size - 1, -1 , -1):
        shift = 0
        if j < matrix_size - 1 and board[n][j] != 1:
            for k in range(matrix_size - 1, j, -1):
                if board[n][k] == 0:
                    shift += 1
                if board[n][k] == 1:
                    shift = 0
            if shift > 0:
                board[n][j + shift] = board[n][j]
                board[n][j] = 0
            if j + shift + 1 >= matrix_size:
                continue
            if board[n][j + shift + 1] == board[n][j + shift] and not merged[n][j + shift + 1] \
                    and not merged[n][j + shift]:
                board[n][j + shift + 1] *= 2
                score += board[n][j + shift + 1]
                board[n][j + shift] = 0
                merged[n][j + shift + 1] = True

# spawn in new pieces randomly when turns start: sinh ngẫu nhiên số và cập nhật lại bảng trong 1 lần


def new_pieces(board):
    count = 0
    full = True
    # kiểm tra xem có thể sinh số thêm được không
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, matrix_size - 1)
        col = random.randint(0, matrix_size - 1)
        if board[row][col] == 0:
            # Sẽ có 10% sinh ra số 4, còn lại chỉ sinh ra số 2
            count += 1
            full = False
            if random.randint(1, 10) == 1:
                board[row][col] = 4
                # print('choose tile 4: ', row, col)
            else:
                board[row][col] = 2
                # print('choose tile 2: ', row, col)
    return board, full

# draw background for the board


def draw_board():
    screen.fill('gray')
    rect = pygame.Rect(0, 0, 400, 400)  # left, top, weight, height
    pygame.draw.rect(screen, colors['bg'], rect, 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    back = font.render(f'Back: ESC', True, 'red')

    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    screen.blit(back, (250, 430))
    

# draw tiles for game

def draw_intro():
    rect = pygame.Rect(0, 0, 400, 370)  # left, top, weight, height
    pygame.draw.rect(screen, colors['bg'], rect, 0, 10)
    pygame.draw.rect(screen, 'white', rect_op1, 0, 10)
    pygame.draw.rect(screen, 'white', rect_op2, 0, 10)
    pygame.draw.rect(screen, 'white', rect_op3, 0, 10)
    pygame.draw.rect(screen, 'white', rect_op4, 0, 10)

    title = font.render('Choose play mode', True, 'red')
    op1 = font.render(f'4x4', True, 'blue')
    op2 = font.render(f'5x5', True, 'blue')
    op3 = font.render(f'4x4 hard', True, 'blue')
    op4 = font.render(f'5x5 hard', True, 'blue')

    font_text = pygame.font.Font('Assets/Fonts/FreeSansBold.ttf', 55, bold = True)
    game_tittle = font_text.render('2048 G4_9', True, 'black')
    # mem1 = font.render(f'Mai Huy Hoàng', True, 'black')
    # mem2 = font.render(f'Đinh Minh Phúc', True, 'black')
    # mem3 = font.render(f'Phạm Văn Huy', True, 'black')

    screen.blit(title, (90, 415))
    screen.blit(op1, (110, 190))
    screen.blit(op2, (250, 190))
    screen.blit(op3, (82, 290))
    screen.blit(op4, (222, 290))
    screen.blit(game_tittle, (65, 50))
    # screen.blit(mem1, (10, 380))
    # screen.blit(mem2, (10, 420))
    # screen.blit(mem3, (10, 460))

# draw game over and restart text (step 7)

def draw_over():
    pygame.draw.rect(screen, 'black', [50, 200, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 215))
    screen.blit(game_over_text2, (70, 255))

def draw_pieces_4(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value == 1:
                pygame.draw.rect(screen, 'yellow', [20 + 95 * j, 20 + 95 * i, 75, 75], 0, 5)
                continue
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(
                screen, color, [20 + 95 * j, 20 + 95 * i, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font(
                    'Assets/Fonts/FreeSansBold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(
                    center=(j * 95 + 57, i * 95 + 57))  # hard code
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [
                                 j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

def draw_pieces_5(board):
    for i in range(5):
        for j in range(5):
            value = board[i][j]
            if value == 1:
                pygame.draw.rect(screen, 'yellow', [10 + 78 * j, 10 + 78 * i, 68, 68], 0, 5)
                continue
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


# main game loop

async def main():
    global colors, board_values, game_over, spawn_new, init_count, direction, \
    score, file, init_high, high_score, next_scene, matrix_size, block

    run = True
    first_init = True
    while run:
        timer.tick(fps)  # thiết lập fps cho game
        screen.fill('gray')  # thiết lập nền xám làm background
        if next_scene == False: draw_intro()
        if next_scene == True:
            if first_init: 
                init()
                first_init = False
            draw_board()
            # print('matrix size = ', matrix_size)
            if matrix_size == 4: draw_pieces_4(board_values)
            else: draw_pieces_5(board_values)
        
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
                    file = open('2048_Scripts/high_score', 'w')
                    file.write(f'{high_score}')
                    file.close()
                    init_high = high_score

        for event in pygame.event.get():  # Xét các event khi game chạy
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                global opos 
                opos = event.pos
                if not next_scene:
                    if rect_op1.collidepoint(event.pos):
                        print('option 1')
                        next_scene = True
                        matrix_size = 4
                        block = False
                    elif rect_op2.collidepoint(event.pos):
                        print('option 2')
                        next_scene = True
                        matrix_size = 5
                        block = False
                    elif rect_op3.collidepoint(event.pos):
                        print('option 3')
                        next_scene = True
                        matrix_size = 4
                        block = True
                    else:
                        print('option 4')
                        next_scene = True
                        matrix_size = 5
                        block = True
                    

            if event.type == pygame.MOUSEBUTTONUP:
                v = pygame.Vector2(event.pos) - pygame.Vector2(opos)
                
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
                if event.key == pygame.K_0:
                    print('option 1')
                    next_scene = True
                    matrix_size = 4
                    block = False
                if event.key == pygame.K_UP:
                    direction = 'UP'
                if event.key == pygame.K_DOWN:
                    direction = 'DOWN'
                if event.key == pygame.K_LEFT:
                    direction = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    next_scene = False
                    first_init = True
                if game_over:
                    if event.key == pygame.K_RETURN:
                        next_scene = False
                        first_init = True

        if score > high_score:
            high_score = score
        pygame.display.flip()  # cập nhật nội dung TOÀN BỘ màn hình
        # pygame.quit  build for pc
        await asyncio.sleep(0)
        # if not run:
        #     pygame.quit()
        #     return

asyncio.run(main())
