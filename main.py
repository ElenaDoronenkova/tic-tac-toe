import pygame
import sys
from game import game

# Параметры
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

# Установка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Крестики-Нолики")

# шрифтек
menu_font = pygame.font.Font(None, 50)

def menu():
    while True:
        screen.fill(WHITE)
        title = menu_font.render("Крестики-Нолики", True, BLACK)
        play_button = menu_font.render("Играть", True, BLACK)
        quit_button = menu_font.render("Выйти", True, BLACK)

        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(play_button, (SCREEN_WIDTH // 2 - play_button.get_width() // 2, 250))
        screen.blit(quit_button, (SCREEN_WIDTH // 2 - quit_button.get_width() // 2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (SCREEN_WIDTH // 2 - play_button.get_width() // 2 <= mouse_x <= SCREEN_WIDTH // 2 + play_button.get_width() // 2 and
                    250 <= mouse_y <= 250 + play_button.get_height()):
                    game(screen, menu)
                if (SCREEN_WIDTH // 2 - quit_button.get_width() // 2 <= mouse_x <= SCREEN_WIDTH // 2 + quit_button.get_width() // 2 and
                    350 <= mouse_y <= 350 + quit_button.get_height()):
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    menu()
