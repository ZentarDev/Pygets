import pygame
import sys
import os

from pygets.core.theme import themes
from pygets.utils.colors import colors
from pygets.widgets import Togglebutton


# Initialize pygame
pygame.init()

# Screen configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Example ToggleButton")

# Import the font
BASE_DIR = os.path.dirname(__file__)
font_path = os.path.join(BASE_DIR, "assets", "fonts", "Inter.ttf")

try:
    font = pygame.font.Font(font_path, 26)
    font.set_bold(True)
except FileNotFoundError:
    font = pygame.font.Font(None, 26)


# Create toggles
toggle1 = Togglebutton(x=100, y=100, screen=screen, theme=themes["dark"], active=True)
toggle2 = Togglebutton(x=100, y=200, screen=screen, theme=themes["light"])
toggle3 = Togglebutton(x=100, y=300, screen=screen, theme=themes["forest"], active=True)
toggle4 = Togglebutton(x=100, y=400, screen=screen, theme=themes["purple_night"])

# Associated text
texts = [
    font.render("Enable fullscreen mode.", True, toggle1.theme.text),
    font.render("Show FPS counter.", True, toggle2.theme.text),
    font.render("Enable background music.", True, toggle3.theme.text),
    font.render("Use custom cursor.", True, toggle4.theme.text)
]

# List of toggles
toggles = [toggle1, toggle2, toggle3, toggle4]


# Main loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    mousedown = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mousedown = True
            pos = event.pos

    screen.fill(colors["BLUISH_GRAY"])

    # Update and draw the toggles
    for i, tg in enumerate(toggles):
        tg.update(mousedown, pygame.mouse.get_pos())
        tg.draw()
        # Draw the text next to
        screen.blit(texts[i], (tg.rect.right + 10, tg.rect.y + (tg.rect.height - texts[i].get_height()) // 2))

    # Show status in console if clicked
    if mousedown:
        mouse_pos = pygame.mouse.get_pos()
        for i, tg in enumerate(toggles):
            if tg.rect.collidepoint(mouse_pos):
                print(f"Toggle {i+1} {'active' if tg.active else 'inactive'}")

    pygame.display.flip()

pygame.quit()
sys.exit()
