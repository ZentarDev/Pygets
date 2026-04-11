import pygame

class WidgetBase:
    def __init__(self, x, y, width, height, screen):
        self._rect = pygame.Rect(x, y, width, height)
        self.screen = screen

    @property
    def rect(self):
        return self._rect

    @property
    def position(self):
        return self._rect.topleft

    @position.setter
    def position(self, valor):
        self._rect.topleft = valor

    def move(self, x, y):
        self._rect.topleft = (x, y)

    def draw(self):
        raise NotImplementedError("This widget must implement draw()")
