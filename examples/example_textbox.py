import pygame
import sys
import os

from pygets.widgets import Textbox
from pygets.core.theme import themes
from pygets.utils.colors import colors


# Initialize pygame
pygame.init()
pygame.key.set_repeat(300, 40)  # IMPORTANT FOR TEXTBOXES

# Screen configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Example TextBox")

# Import the font
BASE_DIR = os.path.dirname(__file__)
font_path = os.path.join(BASE_DIR, "assets", "fonts", "Inter.ttf")

try:
    font = pygame.font.Font(font_path, 26)
    font.set_bold(True)
except FileNotFoundError:
    font = pygame.font.Font(None, 26)


# Select theme
theme = themes["dark"]

# Callback function (optional)
def when_enter_presses():
    print(f"Text entered: {textbox1.textbox_content}")


# Crear inputs
textbox1 = Textbox(
    x=100,
    y=100,
    screen=screen,
    font=font,
    function=when_enter_presses,
    placeholder="Write your name...",
    width=400,
    theme=theme
)

textbox2 = Textbox(
    x=100,
    y=250,
    screen=screen,
    font=font,
    placeholder="Write your name...",
    width=400,
    max_characters=100,
    theme=theme
)


# Main loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        textbox1.handle_event(event)
        textbox2.handle_event(event)

    textbox1.update()
    textbox2.update()

    screen.fill(colors["BLUISH_GRAY"])

    label1 = font.render("Name:", True, theme.text)
    label2 = font.render("Email:", True, theme.text)
    screen.blit(label1, (100, 70))
    screen.blit(label2, (100, 220))

    textbox1.draw()
    textbox2.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
