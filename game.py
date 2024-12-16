import pygame
import sys

# Параметры
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (240, 248, 255)  # Фон поля
RESULTS_BACKGROUND_COLOR = (220, 229, 226)  # Фон экрана результатов
BUTTON_COLOR = (220, 220, 220)
BUTTON_HOVER_COLOR = (176, 196, 222)
BUTTON_BORDER_COLOR = (173, 216, 230)
LINE_WIDTH = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)

pygame.init()

font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

# Таблица результатов
results = {"X": 0, "O": 0}


def draw_grid(screen, grid_size, offset):
    tile_size = (SCREEN_WIDTH - 2 * offset) // grid_size
    for x in range(1, grid_size):
        pygame.draw.line(screen, BLACK, (offset + x * tile_size, offset),
                         (offset + x * tile_size, SCREEN_HEIGHT - offset), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (offset, offset + x * tile_size),
                         (SCREEN_WIDTH - offset, offset + x * tile_size), LINE_WIDTH)


def draw_x(screen, col, row, tile_size, offset):
    line_width = 5
    start_point = (offset + col * tile_size + tile_size // 4, offset + row * tile_size + tile_size // 4)
    end_point = (offset + (col + 1) * tile_size - tile_size // 4, offset + (row + 1) * tile_size - tile_size // 4)

    pygame.draw.line(screen, X_COLOR, start_point, end_point, line_width)
    start_point = (offset + col * tile_size + tile_size // 4, offset + (row + 1) * tile_size - tile_size // 4)
    end_point = (offset + (col + 1) * tile_size - tile_size // 4, offset + row * tile_size + tile_size // 4)
    pygame.draw.line(screen, X_COLOR, start_point, end_point, line_width)


def draw_o(screen, col, row, tile_size, offset):
    radius = tile_size // 4
    center = (offset + col * tile_size + tile_size // 2, offset + row * tile_size + tile_size // 2)
    pygame.draw.circle(screen, O_COLOR, center, radius, 5)


def draw_board(screen, board, grid_size, offset):
    tile_size = (SCREEN_WIDTH - 2 * offset) // grid_size
    for row in range(grid_size):
        for col in range(grid_size):
            if board[row][col] == "X":
                draw_x(screen, col, row, tile_size, offset)
            elif board[row][col] == "O":
                draw_o(screen, col, row, tile_size, offset)


def check_winner(board, grid_size):
    for i in range(grid_size):
        # Проверка строк и столбцов
        for j in range(grid_size - 2):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] and board[i][j] is not None:
                return board[i][j]
            if board[j][i] == board[j + 1][i] == board[j + 2][i] and board[j][i] is not None:
                return board[j][i]

    # Проверка диагоналей
    for i in range(grid_size - 2):
        for j in range(grid_size - 2):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] and board[i][j] is not None:
                return board[i][j]
            if board[i][j + 2] == board[i + 1][j + 1] == board[i + 2][j] and board[i][j + 2] is not None:
                return board[i][j + 2]

    return None


def draw_rounded_button(screen, text, x, y, width, height, color, hover_color, border_color, border_width, radius):
    mouse_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, width, height)

    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect, border_radius=radius)
    else:
        pygame.draw.rect(screen, color, rect, border_radius=radius)

    pygame.draw.rect(screen, border_color, rect, border_width, border_radius=radius)

    text_surface = menu_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    return rect

def draw_results_overlay(screen, grid_size):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(RESULTS_BACKGROUND_COLOR + (200,))  # Полупрозрачный цвет для фона
    screen.blit(overlay, (0, 0))

    # Отрисовка рамки
    frame_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
    pygame.draw.rect(screen, BLACK, frame_rect, 3)

    text = font.render("Результаты", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))

    x_wins = small_font.render(f"X побед: {results['X']}", True, BLACK)
    o_wins = small_font.render(f"O побед: {results['O']}", True, BLACK)
    screen.blit(x_wins, (SCREEN_WIDTH // 2 - x_wins.get_width() // 2, 200))
    screen.blit(o_wins, (SCREEN_WIDTH // 2 - o_wins.get_width() // 2, 250))

    restart_button = menu_font.render("Играть", True, BLACK)
    menu_button = menu_font.render("Назад", True, BLACK)

    restart_rect = restart_button.get_rect(center=(SCREEN_WIDTH // 2, 400))
    menu_rect = menu_button.get_rect(center=(SCREEN_WIDTH // 2, 500))
    
    restart_button_rect = draw_rounded_button(screen, "Играть", restart_rect.x - 10, restart_rect.y - 10 ,
                                        restart_rect.width + 20,restart_rect.height+20,BUTTON_COLOR, BUTTON_HOVER_COLOR,
                                        BUTTON_BORDER_COLOR, 1, 10)
    menu_button_rect = draw_rounded_button(screen, "Назад", menu_rect.x - 10, menu_rect.y - 10 ,
                                        menu_rect.width + 20,menu_rect.height+20,BUTTON_COLOR, BUTTON_HOVER_COLOR,
                                        BUTTON_BORDER_COLOR, 1, 10)
    screen.blit(restart_button,restart_rect)
    screen.blit(menu_button,menu_rect)
    return restart_button_rect, menu_button_rect


def game(screen, menu_callback, grid_size):
    offset = 50
    board = [[None] * grid_size for _ in range(grid_size)]
    current_player = "X"
    game_over = False
    winner = None
    restart_button_rect = None
    menu_button_rect = None
    show_results = False
    while True:
        screen.fill(BACKGROUND_COLOR)  # Заполнение фона цветом из main.py
        draw_grid(screen, grid_size, offset)
        draw_board(screen, board, grid_size, offset)

        if game_over:
            if show_results:
                restart_button_rect, menu_button_rect = draw_results_overlay(screen, grid_size)
            else:
                if winner:
                    text = font.render(f"{winner} Победил!", True, BLACK)
                else:
                    text = font.render("Ничья!", True, BLACK)
                screen.blit(text,
                            (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

                restart_button = menu_font.render("Играть", True, BLACK)
                menu_button = menu_font.render("Назад", True, BLACK)

                restart_rect = restart_button.get_rect(center=(SCREEN_WIDTH // 2, 400))
                menu_rect = menu_button.get_rect(center=(SCREEN_WIDTH // 2, 500))
                
                restart_button_rect = draw_rounded_button(screen, "Играть", restart_rect.x - 10, restart_rect.y - 10 ,
                                        restart_rect.width + 20,restart_rect.height+20,BUTTON_COLOR, BUTTON_HOVER_COLOR,
                                        BUTTON_BORDER_COLOR, 1, 10)
                menu_button_rect = draw_rounded_button(screen, "Назад", menu_rect.x - 10, menu_rect.y - 10 ,
                                        menu_rect.width + 20,menu_rect.height+20,BUTTON_COLOR, BUTTON_HOVER_COLOR,
                                        BUTTON_BORDER_COLOR, 1, 10)

                screen.blit(restart_button, restart_rect)
                screen.blit(menu_button, menu_rect)
                
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if restart_button_rect and restart_button_rect.collidepoint(mouse_x, mouse_y):
                        game(screen, menu_callback, grid_size)
                        return
                    if menu_button_rect and menu_button_rect.collidepoint(mouse_x, mouse_y):
                        menu_callback()
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        show_results = not show_results

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    x, y = event.pos
                    tile_size = (SCREEN_WIDTH - 2 * offset) // grid_size
                    col = (x - offset) // tile_size
                    row = (y - offset) // tile_size
                    if 0 <= col < grid_size and 0 <= row < grid_size and board[row][col] is None:
                        board[row][col] = current_player
                        winner = check_winner(board, grid_size)
                        if winner:
                            results[winner] += 1
                        if winner or all(all(row) for row in board):
                            game_over = True
                            show_results = True
                        current_player = "O" if current_player == "X" else "X"

        pygame.display.flip()