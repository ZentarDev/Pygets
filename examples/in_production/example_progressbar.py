import pygame
import sys
import os

from pygets.widgets import Progressbar
from pygets.core.theme import themes
from pygets.utils.colors import colors


# Initialize pygame
pygame.init()

# Screen configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Example ProgressBar")

# Base directory
BASE_DIR = os.path.dirname(__file__)

# Font path
font_path = os.path.join(BASE_DIR, "assets", "fonts", "Inter.ttf")

try:
    font = pygame.font.Font(font_path, 26)
    font.set_bold(True)
except FileNotFoundError:
    font = pygame.font.Font(None, 26)

# Create progress bars with themes
progressbar1 = Progressbar(
    x=100, y=100, width=300, height=40,
    theme=themes["light"],
    font=font, screen=screen, text_in_progress="Loading...",
    progress=0.0, text_complete="Complete"
)

progressbar2 = Progressbar(
    x=100, y=200, width=300, height=40,
    theme=themes["dark"],
    font=font, screen=screen, text_in_progress="Progress",
    progress=0.0, border_radius=100, text_complete="Finalized"
)

progressbar3 = Progressbar(
    x=100, y=300, width=300, height=40,
    theme=themes["sunset"],
    font=font, screen=screen, text_complete="Complete",
    progress=1.0
)

# Loop principal
clock = pygame.time.Clock()
running = True
progress_increment = 0.01

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update progress for animation
    if progressbar1.progress < 1.0:
        progressbar1.set_progress(progressbar1.progress + progress_increment)
    if progressbar2.progress < 1.0:
        progressbar2.set_progress(progressbar2.progress + progress_increment)
    
    screen.fill(colors["BLUISH_GRAY"])
    
    progressbar1.draw()
    progressbar2.draw()
    progressbar3.draw()
    
    pygame.display.flip()

pygame.quit()
sys.exit()