import pygame
import sys
import os

from pygets.widgets.popup import Popup
from pygets.core.theme import themes
from pygets.utils.colors import colors


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Example Popup")

BASE_DIR = os.path.dirname(__file__)
font_path = os.path.join(BASE_DIR, "assets", "fonts", "Inter.ttf")

try:
    font = pygame.font.Font(font_path, 24)
    title_font = pygame.font.Font(font_path, 28)
    title_font.set_bold(True)
except FileNotFoundError:
    font = pygame.font.Font(None, 24)
    title_font = pygame.font.Font(None, 28)

popup = Popup(
    title="Lorem ipsum",
    message="Lorem ipsum dolor sit amet consectetur adipiscing elit odio, nostra mus aliquam viverra et fermentum mattis, curabitur aptent pharetra imperdiet dignissim mi sed.",
    font=font,
    title_font=title_font,
    screen_width=SCREEN_WIDTH,
    screen_height=SCREEN_HEIGHT,
    width=500,
    height=250,
    screen=screen,
    theme=themes["light"],
)

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        popup.handle_event(event)

    screen.fill(colors["BLUISH_GRAY"])

    popup.update()
    popup.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()