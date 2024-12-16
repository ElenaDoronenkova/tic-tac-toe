import pygame
import sys
from game import game

# Параметры
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (240, 248, 255)  # AliceBlue
BUTTON_COLOR = (220, 220, 220)  # LightGray
BUTTON_HOVER_COLOR = (176, 196, 222)  # LightSteelBlue
BUTTON_BORDER_COLOR = (173, 216, 230)  # LightBlue
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

# Установка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Крестики-Нолики")

# Шрифты
title_font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 50)
settings_font = pygame.font.Font(None, 30)

# Параметры игры по умолчанию
GRID_SIZE = 3


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


def draw_settings_button(screen, text, x, y, width, height, color, hover_color, border_color, border_width, radius):
    mouse_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, width, height)

    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect, border_radius=radius)
    else:
        pygame.draw.rect(screen, color, rect, border_radius=radius)

    pygame.draw.rect(screen, border_color, rect, border_width, border_radius=radius)

    text_surface = settings_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    return rect


def settings_menu():
    global GRID_SIZE
    while True:
        screen.fill(BACKGROUND_COLOR)

        # Заголовок настроек
        title = title_font.render("Настройки", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # Текст текущего размера поля
        grid_size_text = settings_font.render(f"Размер поля: {GRID_SIZE}x{GRID_SIZE}", True, BLACK)
        grid_size_rect = grid_size_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(grid_size_text, grid_size_rect)

        # Кнопка для выбора размера 3x3
        size_3_button_width = 150
        size_3_button_height = 40
        size_3_button_rect = draw_settings_button(screen, "3x3", SCREEN_WIDTH // 2 - size_3_button_width - 10, 250,
                                                 size_3_button_width, size_3_button_height, BUTTON_COLOR,
                                                 BUTTON_HOVER_COLOR, BUTTON_BORDER_COLOR, 1, 10)
        # Кнопка для выбора размера 5x5
        size_5_button_width = 150
        size_5_button_height = 40
        size_5_button_rect = draw_settings_button(screen, "5x5", SCREEN_WIDTH // 2 + 10, 250,
                                                  size_5_button_width, size_5_button_height, BUTTON_COLOR,
                                                  BUTTON_HOVER_COLOR, BUTTON_BORDER_COLOR, 1, 10)

        # Кнопка "Назад"
        back_button_width = 150
        back_button_height = 50
        back_button_rect = draw_settings_button(screen, "Назад", SCREEN_WIDTH // 2 - back_button_width // 2, 450,
                                                back_button_width, back_button_height, BUTTON_COLOR,
                                                BUTTON_HOVER_COLOR, BUTTON_BORDER_COLOR, 1, 10)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if size_3_button_rect.collidepoint(mouse_x, mouse_y):
                    GRID_SIZE = 3
                elif size_5_button_rect.collidepoint(mouse_x, mouse_y):
                    GRID_SIZE = 5
                elif back_button_rect.collidepoint(mouse_x, mouse_y):
                    return


def menu():
    while True:
        screen.fill(BACKGROUND_COLOR)

        # Заголовок
        title = title_font.render("Крестики-Нолики", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title, title_rect)

        # Кнопки
        button_width = 200
        button_height = 60
        button_spacing = 30
        start_y = SCREEN_HEIGHT // 2 - (button_height * 1.5 + button_spacing) + 50 # Увеличиваем отступ на 50

        play_button_rect = draw_rounded_button(screen, "Играть", SCREEN_WIDTH // 2 - button_width // 2, start_y,
                                               button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR,
                                               BUTTON_BORDER_COLOR, 1, 10)
        settings_button_rect = draw_rounded_button(screen, "Настройки", SCREEN_WIDTH // 2 - button_width // 2,
                                                start_y + button_height + button_spacing, button_width, button_height,
                                              BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_BORDER_COLOR, 1, 10)
        quit_button_rect = draw_rounded_button(screen, "Выйти", SCREEN_WIDTH // 2 - button_width // 2,
                                              start_y + button_height * 2 + button_spacing * 2, button_width, button_height,
                                              BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_BORDER_COLOR, 1, 10)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if play_button_rect.collidepoint(mouse_x, mouse_y):
                    game(screen, menu, GRID_SIZE)
                if settings_button_rect.collidepoint(mouse_x, mouse_y):
                    settings_menu()
                if quit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    menu()
