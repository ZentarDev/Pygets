import pygame
from pygets.core.widgets import WidgetBase
from pygets.utils.validators import *


class Togglebutton(WidgetBase):
    """
    Toggle button widget that can be switched on/off.

    Parameters
    ----------
    x, y : int
        Position of the toggle button.
    screen : pygame.Surface
        Surface where the button is drawn.
    theme : Theme
        Theme instance for colors.
    width, height : int, optional
        Size of the toggle (default width=60, height=30).
    active : bool, optional
        Initial toggle state (default False).

    Attributes
    ----------
    active : bool
        Current toggle state.
    hover : bool
        True if mouse is hovering over the button.

    Methods
    -------
    update(mousedown, pos):
        Updates hover state and toggles state on mouse click.
    draw():
        Draws the toggle button with visual states.
    """
    def __init__(self, x, y, screen, theme, width=60, height=30, active=False):
        validate_position(x, y, screen, width, height)
        validate_size(width, height)
        validate_screen(screen)
        validate_theme(theme, extra_attrs=["idle"])
        validate_toggle(width, height, active)

        self.theme = theme
        self.height = height
        self.width = width
        self.hover = False
        self.bg_color = self.theme.background
        self.toggle_color = self.theme.accent
        self.edge_color = self.theme.foreground
        self.current_color = self.bg_color

        super().__init__(x, y, width, height, screen)
        self.active = active
        self.radio = self.height // 2

    def update(self, mousedown, pos):
        """
        Updates hover state and toggles state on mouse click.

        Parameters
        ----------
        mousedown : bool
            True if mouse button is pressed.
        pos : tuple
            Mouse position (x, y).
        """
        self.hover = self.rect.collidepoint(pos)
        if mousedown and self.rect.collidepoint(pos):
            self.active = not self.active

    def draw(self):
        """
        Draws the toggle button with visual states.
        """
        toggle_x = self.rect.right - self.radio if self.active else self.rect.left + self.radio
        self.bg_color = self.theme.background if self.active else self.theme.foreground
        toggle_y = self.rect.centery

        pygame.draw.rect(self.screen, self.bg_color, self.rect, border_radius=self.radio)
        pygame.draw.rect(self.screen, self.edge_color, self.rect, width=2, border_radius=self.radio)

        if self.hover:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (*self.theme.idle, 95), overlay.get_rect(), border_radius=self.radio)
            self.screen.blit(overlay, self.rect.topleft)

        pygame.draw.circle(self.screen, self.toggle_color, (toggle_x, toggle_y), self.radio - 3)