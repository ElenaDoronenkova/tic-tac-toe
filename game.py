import pygame
import sys

# Парамутры
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 3
TILE_SIZE = SCREEN_WIDTH // GRID_SIZE
LINE_WIDTH = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()

font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 50)
#Рисуем в клетку в которую нас посадят
def draw_grid(screen):
    for x in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x * TILE_SIZE, 0), (x * TILE_SIZE, SCREEN_HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (0, x * TILE_SIZE), (SCREEN_WIDTH, x * TILE_SIZE), LINE_WIDTH)
#рисовашки картиношки, т.е иксов и ошек
def draw_board(screen, board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == "X":
                pygame.draw.line(screen, RED, (col * TILE_SIZE + 50, row * TILE_SIZE + 50), ((col + 1) * TILE_SIZE - 50, (row + 1) * TILE_SIZE - 50), LINE_WIDTH)
                pygame.draw.line(screen, RED, (col * TILE_SIZE + 50, (row + 1) * TILE_SIZE - 50), ((col + 1) * TILE_SIZE - 50, row * TILE_SIZE + 50), LINE_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, BLUE, (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 3, LINE_WIDTH)
#КТО ПОБЕДИТЕЛЬ?!
def check_winner(board):
    for i in range(GRID_SIZE):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    return None
#Базовая функция игры
def game(screen, menu_callback):
    board = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
    current_player = "X"
    game_over = False
    winner = None

    while True: #Когда правда.. А когда ложь?
        screen.fill(WHITE)
        draw_grid(screen)
        draw_board(screen, board)

        if game_over:
            if winner:
                text = font.render(f"{winner} Победил!", True, BLACK)
            else:
                text = font.render("Ничья!", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

            restart_button = menu_font.render("Играть", True, BLACK)
            menu_button = menu_font.render("Назад", True, BLACK)
            screen.blit(restart_button, (SCREEN_WIDTH // 2 - restart_button.get_width() // 2, 400))
            screen.blit(menu_button, (SCREEN_WIDTH // 2 - menu_button.get_width() // 2, 500))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if (SCREEN_WIDTH // 2 - restart_button.get_width() // 2 <= mouse_x <= SCREEN_WIDTH // 2 + restart_button.get_width() // 2 and
                        400 <= mouse_y <= 400 + restart_button.get_height()):
                        game(screen, menu_callback)
                    if (SCREEN_WIDTH // 2 - menu_button.get_width() // 2 <= mouse_x <= SCREEN_WIDTH // 2 + menu_button.get_width() // 2 and
                        500 <= mouse_y <= 500 + menu_button.get_height()):
                        menu_callback()
                        return
        else: #обработошка нажатия
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    x, y = event.pos
                    col, row = x // TILE_SIZE, y // TILE_SIZE
                    if board[row][col] is None:
                        board[row][col] = current_player
                        winner = check_winner(board)
                        if winner or all(all(row) for row in board):
                            game_over = True
                        current_player = "O" if current_player == "X" else "X"
        #Отображаем всё
        pygame.display.flip()
