import pygame
import random
import io
from flask import Flask, render_template, Response
from graphics import draw_grid, GREEN, YELLOW, GRAY
from settings import WORD_LIST, MAX_ATTEMPTS, WORD_LENGTH

# Initialize Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wordle")

# Choose a random target word from the word list
target_word = random.choice(WORD_LIST)
keyboard_colors = {}

# Flask app
app = Flask(__name__)

# Game variables
guesses = []
current_guess = ''
current_row = 0
game_over = False


def update_keyboard_colors(current_guess, target_word):
    for i, letter in enumerate(current_guess):
        if letter == target_word[i]:
            keyboard_colors[letter] = GREEN
        elif letter in target_word and keyboard_colors.get(letter) != GREEN:
            keyboard_colors[letter] = YELLOW
        elif letter not in target_word:
            keyboard_colors[letter] = GRAY


def game_loop():
    """Run one frame of the game and update the Pygame surface."""
    global current_guess, current_row, game_over

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(current_guess) == WORD_LENGTH:
                guesses.append(list(current_guess))
                update_keyboard_colors(current_guess, target_word)
                current_row += 1
                current_guess = ''

                if ''.join(guesses[-1]) == target_word:
                    game_over = True
                elif current_row == MAX_ATTEMPTS:
                    game_over = True

            elif event.key == pygame.K_BACKSPACE:
                current_guess = current_guess[:-1]

            elif event.key in range(pygame.K_a, pygame.K_z + 1) and len(current_guess) < WORD_LENGTH:
                current_guess += chr(event.key).upper()

    draw_grid(screen, guesses, current_guess, target_word, keyboard_colors)


def get_frame():
    """Render the game screen to an image and return it as bytes."""
    game_loop()
    data = pygame.image.tostring(screen, "RGB")
    image = pygame.image.fromstring(data, (SCREEN_WIDTH, SCREEN_HEIGHT), "RGB")
    with io.BytesIO() as output:
        pygame.image.save(image, output, "JPEG")
        return output.getvalue()


@app.route("/")
def index():
    """Render the HTML template."""
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    """Stream the Pygame game as a video feed."""
    def generate():
        while True:
            frame = get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug=True)
