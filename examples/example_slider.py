import pygame
import sys
import os

from pygets.utils.colors import *
from pygets.widgets import Slider
from pygets.core.theme import themes
from pygets.utils.colors import colors


# Initialize pygame
pygame.init()

# Screen configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Example Slider")

# Import the font
BASE_DIR = os.path.dirname(__file__)
font_path = os.path.join(BASE_DIR, "assets", "fonts", "Inter.ttf")

try:
    font = pygame.font.Font(font_path, 26)
    font.set_bold(True)
except FileNotFoundError:
    font = pygame.font.Font(None, 26)


# Select theme
actual_theme = themes["purple_night"]


# Create sliders
slider1 = Slider(
    x=100, y=200, width=300, height=8,
    screen=screen,
    min_val=0, max_val=100, initial_value=50,
    theme=actual_theme
)

slider2 = Slider(
    x=100, y=300, width=300, height=8,
    screen=screen,
    min_val=0, max_val=1, initial_value=0.25, # type: ignore
    theme=actual_theme
)


# Main loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        slider1.handle_event(event)
        slider2.handle_event(event)

    # Background according to theme
    screen.fill(colors["BLUISH_GRAY"]) # MINT_GREEN

    slider1.draw()
    slider2.draw()

    # Display values ​​with theme text color
    text1 = font.render(f"Slider value 1: {int(slider1.value)}", True, actual_theme.text)
    text2 = font.render(f"Slider value 2: {slider2.value:.2f}", True, actual_theme.text)

    screen.blit(text1, (420, 190))
    screen.blit(text2, (420, 290))

    pygame.display.flip()

pygame.quit()
sys.exit()
