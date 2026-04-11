import pygame
import sys
import os

from pygets.widgets import Button
from pygets.core.theme import themes
from pygets.utils.colors import colors


# Initialize pygame
pygame.init()

# Screen configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Example Button")

# Base directory
BASE_DIR = os.path.dirname(__file__)

# Font path
font_path = os.path.join(BASE_DIR, "assets", "fonts", "Inter.ttf")

# Image path
image_path = os.path.join(BASE_DIR, "assets", "images", "star.png")

try:
    font = pygame.font.Font(font_path, 26)
    font.set_bold(True)
except FileNotFoundError:
    font = pygame.font.Font(None, 26)

try:
    image = pygame.image.load(image_path).convert_alpha()
except FileNotFoundError:
    print(f"Image not found at {image_path}!")
    image = pygame.Surface((100, 100), pygame.SRCALPHA)  # empty fallback surface


# Create buttons with themes and hover visible
button1 = Button(
    x=100, y=100,
    theme=themes["light"],
    font=font, screen=screen, text="Click me!",
)

button2 = Button(
    x=100, y=200,
    theme=themes["dark"],
    font=font, screen=screen, image=image, text="I love python"
)

button3 = Button(
    x=100, y=300,
    theme=themes["sunset"],
    font=font, screen=screen, text="Other button", width=200
)

# Loop principal
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detect button clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button1.rect.collidepoint(event.pos):
                print("Button 1 pressed!")
            if button2.rect.collidepoint(event.pos):
                print("Button 2 pressed!")
            if button3.rect.collidepoint(event.pos):
                print("Button 3 pressed!")
    
    screen.fill(colors["BLUISH_GRAY"])

    button1.draw()
    button2.draw()
    button3.draw()
    
    pygame.display.flip()

pygame.quit()
sys.exit()
