import pygame
from pygets.core.widgets import WidgetBase
from pygets.utils.validators import *


class Slider(WidgetBase):
    """
    Slider widget for selecting a value within a range.

    Parameters
    ----------
    x, y : int
        Position of the slider on the screen.
    width, height : int
        Size of the slider bar.
    screen : pygame.Surface
        Surface where the slider is drawn.
    theme : Theme
        Theme instance defining the colors.
    min_val : float, optional
        Minimum value of the slider (default 0).
    max_val : float, optional
        Maximum value of the slider (default 100).
    initial_value : float, optional
        Initial slider value (default 50).

    Attributes
    ----------
    value : float
        Current value of the slider.
    dragging : bool
        True if the handle is being dragged.
    handle_rect : pygame.Rect
        Rectangle representing the draggable handle.

    Methods
    -------
    handle_event(event):
        Handles mouse events for dragging and clicking the slider.
    draw():
        Draws the slider on the screen.
    _update_handle():
        Updates the handle position according to the current slider value.
    _update_value():
        Updates the slider value based on the current handle position.
    """
    def __init__(self, x, y, width, height, screen, theme, min_val=0, max_val=100, initial_value=50):
        validate_position(x, y, screen, width, height)
        validate_size(width, height)
        validate_screen(screen)
        validate_theme(theme)
        validate_slider(min_val, max_val, initial_value)

        super().__init__(x, y, width, height, screen)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_value
        self.dragging = False
        self.handle_width = 14
        self.handle_height = height + 6
        self._update_handle()
        self.theme = theme
        self.color_bar = theme.foreground
        self.bg_color = theme.accent
        self.color_handle = theme.background

    def _update_handle(self):
        """
        Update the position of the slider handle according to the current value.
        """
        percentage = (self.value - self.min_val) / (self.max_val - self.min_val)
        x = self.rect.x + int(percentage * (self.rect.width - self.handle_width))
        y = self.rect.centery - self.handle_height // 2
        self.handle_rect = pygame.Rect(x, y, self.handle_width, self.handle_height)

    def _update_value(self):
        """
        Update the slider value based on the current handle position.
        """
        rel_x = self.handle_rect.x - self.rect.x
        percentage = rel_x / (self.rect.width - self.handle_width)
        self.value = max(self.min_val, min(self.max_val, self.min_val + percentage * (self.max_val - self.min_val)))

    def handle_event(self, event):
        """
        Handle mouse events for dragging and clicking the slider.

        Parameters
        ----------
        event : pygame.event.Event
            Pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
            elif self.rect.collidepoint(event.pos):
                x = event.pos[0] - self.handle_width // 2
                x = max(self.rect.x, min(x, self.rect.right - self.handle_width))
                self.handle_rect.x = x
                self._update_value()
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            x = event.pos[0] - self.handle_width // 2
            x = max(self.rect.x, min(x, self.rect.right - self.handle_width))
            self.handle_rect.x = x
            self._update_value()

    def draw(self):
        """
        Draw the slider on the screen.
        """
        pygame.draw.rect(self.screen, self.color_bar, self.rect, border_radius=4)
        fill = pygame.Rect(self.rect.x, self.rect.y, self.handle_rect.centerx - self.rect.x, self.rect.height)
        pygame.draw.rect(self.screen, self.bg_color, fill, border_radius=4)
        pygame.draw.rect(self.screen, self.color_handle, self.handle_rect, border_radius=6)