import pygame
import sys
import os

from pygets.widgets import Combobox
from pygets.core.theme import themes
from pygets.utils.colors import colors


# Initialize pygame
pygame.init()

# Screen configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Example ComboBox")

# Import the font
BASE_DIR = os.path.dirname(__file__)
font_path = os.path.join(BASE_DIR, "assets", "fonts", "Inter.ttf")

try:
    font = pygame.font.Font(font_path, 26)
    font.set_bold(True)
except FileNotFoundError:
    font = pygame.font.Font(None, 26)


# Create a comobobx with the theme "light"
combo = Combobox(
    x=100,
    y=100,
    width=250,
    height=35,
    screen=screen,
    options=["Python", "Java", "C++", "JavaScript", "Rust", "Go"],
    font=font,
    border_radius=10,
    theme=themes["light"]
)


# Main loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        combo.handle_event(event)

    screen.fill(colors["BLUISH_GRAY"])
    
    combo.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
