import pygame
import sys
import os

from pygets.core.theme import themes
from pygets.utils.colors import colors
from pygets.widgets import Checkbox


# Initialize pygame
pygame.init()

# Screen configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Example CheckBox")

# Import the font
BASE_DIR = os.path.dirname(__file__)
font_path = os.path.join(BASE_DIR, "assets", "fonts", "Inter.ttf")

try:
    font = pygame.font.Font(font_path, 26)
    font.set_bold(True)
except FileNotFoundError:
    font = pygame.font.Font(None, 26)


# Create checkboxes
checkbox1 = Checkbox(x=100, y=100, screen=screen, theme=themes["forest"], border_radius=100)
checkbox2 = Checkbox(x=100, y=200, screen=screen, theme=themes["ocean"], checked=True, border_radius=5)
checkbox3 = Checkbox(x=100, y=300, screen=screen, theme=themes["sunset"])
checkbox4 = Checkbox(x=100, y=400, screen=screen, checked=False, theme=themes["purple_night"])

# Texto asociado
texts = [
    font.render("Show debug info.", True, checkbox1.theme.text),
    font.render("Enable background scrolling.", True, checkbox2.theme.text),
    font.render("Show collision outlines.", True, checkbox3.theme.text),
    font.render("Enable screen transitions.", True, checkbox4.theme.text)
]

# List of checkboxes
checkboxes = [checkbox1, checkbox2, checkbox3, checkbox4]


# Main Loop
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

    # Update and draw the checkboxes
    for i, cb in enumerate(checkboxes):
        cb.update(mousedown, pygame.mouse.get_pos())
        cb.draw()
        screen.blit(texts[i], (cb.rect.right + 10, cb.rect.y - 2)) # Draw the texts

    # Show status in console if clicked
    if mousedown:
        mouse_pos = pygame.mouse.get_pos()
        for i, cb in enumerate(checkboxes):
            if cb.rect.collidepoint(mouse_pos):
                print(f"Checkbox {i+1} {'marked' if cb.checked else 'unmarked'}")

    pygame.display.flip()

pygame.quit()
sys.exit()
