import os

import pygame
import pytest


os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


@pytest.fixture(autouse=True)
def pygame_env():
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()


@pytest.fixture
def small_screen():
    return pygame.Surface((240, 140))


@pytest.fixture
def medium_screen():
    return pygame.Surface((400, 220))


@pytest.fixture
def large_screen():
    return pygame.Surface((800, 600))


@pytest.fixture
def font():
    return pygame.font.Font(None, 24)


@pytest.fixture
def title_font():
    return pygame.font.Font(None, 28)
