# graphics.py

import pygame
from settings import MAX_ATTEMPTS, WORD_LENGTH

# Color definitions
BACKGROUND_COLOR = (18, 18, 19)
LIGHT_GRAY = (211, 211, 211)  # Light gray for alternating squares
DARK_GRAY = (169, 169, 169)  # Dark gray for alternating squares
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (83, 141, 78)  # Wordle-style green for correct letters
YELLOW = (181, 159, 59)  # Wordle-style yellow for misplaced letters
GRAY = (58, 58, 60)  # Wordle-style gray for incorrect letters

LETTER_SIZE = 70
MARGIN = 10
KEYBOARD_ROWS = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]


def draw_grid(screen, guesses, current_guess, target_word, keyboard_colors):
    font = pygame.font.Font(None, 48)
    screen.fill(BACKGROUND_COLOR)

    # Center the grid on the screen
    grid_width = WORD_LENGTH * (LETTER_SIZE + MARGIN) - MARGIN
    grid_height = MAX_ATTEMPTS * (LETTER_SIZE + MARGIN) - MARGIN
    start_x = (screen.get_width() - grid_width) // 2
    start_y = (screen.get_height() - grid_height) // 3  # Shift up for keyboard

    # Draw the grid with alternating gray squares
    for row in range(MAX_ATTEMPTS):
        for col in range(WORD_LENGTH):
            x = start_x + col * (LETTER_SIZE + MARGIN)
            y = start_y + row * (LETTER_SIZE + MARGIN)

            # Default square color
            color = LIGHT_GRAY if (row + col) % 2 == 0 else DARK_GRAY
            letter = ''

            if row < len(guesses):  # Add feedback colors if a guess exists
                letter = guesses[row][col]
                if letter == target_word[col]:
                    color = GREEN
                elif letter in target_word:
                    color = YELLOW
                else:
                    color = GRAY

            # Draw each square and letter
            pygame.draw.rect(screen, color, pygame.Rect(x, y, LETTER_SIZE, LETTER_SIZE))
            pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, LETTER_SIZE, LETTER_SIZE), 2)
            if letter:
                text = font.render(letter, True, BLACK if color in [LIGHT_GRAY, DARK_GRAY] else WHITE)
                text_rect = text.get_rect(center=(x + LETTER_SIZE // 2, y + LETTER_SIZE // 2))
                screen.blit(text, text_rect)

    # Draw the current guess while typing
    if current_guess:
        row = len(guesses)
        for col in range(len(current_guess)):
            x = start_x + col * (LETTER_SIZE + MARGIN)
            y = start_y + row * (LETTER_SIZE + MARGIN)
            pygame.draw.rect(screen, WHITE, pygame.Rect(x, y, LETTER_SIZE, LETTER_SIZE))
            pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, LETTER_SIZE, LETTER_SIZE), 2)
            text = font.render(current_guess[col], True, BLACK)
            text_rect = text.get_rect(center=(x + LETTER_SIZE // 2, y + LETTER_SIZE // 2))
            screen.blit(text, text_rect)

    # Draw the keyboard below the grid
    draw_keyboard(screen, keyboard_colors, font)
    pygame.display.update()


def draw_keyboard(screen, keyboard_colors, font):
    # Keyboard position settings
    key_width, key_height = 50, 60
    keyboard_y = screen.get_height() - (len(KEYBOARD_ROWS) * (key_height + MARGIN)) - MARGIN

    # Draw each row of the keyboard
    for row_idx, row in enumerate(KEYBOARD_ROWS):
        row_x = (screen.get_width() - (len(row) * (key_width + MARGIN) - MARGIN)) // 2
        y = keyboard_y + row_idx * (key_height + MARGIN)

        for key in row:
            color = keyboard_colors.get(key, LIGHT_GRAY)
            x = row_x + row.index(key) * (key_width + MARGIN)

            # Draw each key with the corresponding color
            pygame.draw.rect(screen, color, pygame.Rect(x, y, key_width, key_height))
            pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, key_width, key_height), 2)

            # Draw letter on key
            text = font.render(key, True, BLACK if color in [LIGHT_GRAY, DARK_GRAY] else WHITE)
            text_rect = text.get_rect(center=(x + key_width // 2, y + key_height // 2))
            screen.blit(text, text_rect)