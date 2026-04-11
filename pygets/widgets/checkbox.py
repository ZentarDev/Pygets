import pygame
from pygets.core.widgets import WidgetBase
from pygets.utils.validators import *


class Checkbox(WidgetBase):
    """
    Interactive checkbox widget with hover and click support.

    This widget can display a square checkbox with optional border radius 
    and manages hover effects and checked state.

    Parameters
    ----------
    x, y : int
        Position of the checkbox on the screen.
    screen : pygame.Surface
        Pygame surface where the checkbox will be drawn.
    theme : Theme
        Theme instance providing colors, must include 'idle'.
    checked : bool, optional
        Initial checked state of the checkbox. Default is False.
    size : int, optional
        Size of the checkbox in pixels. Default is 20.
    border_radius : int, optional
        Radius of the corners in pixels. Default is 0.

    Attributes
    ----------
    checked : bool
        True if the checkbox is checked.
    hover : bool
        True if the mouse is hovering over the checkbox.
    bg_color : tuple
        Background color from theme.
    edge_color : tuple
        Color of the checkbox border.
    check_color : tuple
        Color used to draw the check mark.

    Methods
    -------
    update(mousedown, pos):
        Updates hover state and toggles checked state if clicked.
    draw():
        Draws the checkbox with background, edges, hover overlay, and check mark.
    _update_hover():
        Updates the internal hover state basen on the mouse position
    _draw_check_mark():
        Draws the check mark on the checkbox if it is checked
    
    """

    def __init__(
        self, x, y, screen, theme, checked=False, size=20, border_radius=0
    ):
        # Input validation
        validate_position(x, y, screen, size, size)
        validate_screen(screen)
        validate_theme(theme, extra_attrs=["idle"])
        validate_checkbox(size, checked)

        self.theme = theme
        self.checked = checked
        self.size = size
        self.border_radius = border_radius
        self.hover = False

        # Colors
        self.bg_color = self.theme.background
        self.edge_color = self.theme.foreground
        self.check_color = self.theme.foreground

        super().__init__(x, y, size, size, screen)

    def _update_hover(self):
        """
        Updates the internal hover state based on the mouse position.

        Notes
        -----
        Internal method used by update() and draw().
        """
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos())

    def _draw_check_mark(self):
        """
        Draws the check mark on the checkbox if it is checked.

        Notes
        -----
        Internal method used by draw().
        """
        pygame.draw.lines(
            self.screen,
            self.check_color,
            False,
            [
                (self.rect.x + 4, self.rect.y + self.size // 2),
                (self.rect.x + self.size // 2 - 2, self.rect.y + self.size - 5),
                (self.rect.x + self.size - 4, self.rect.y + 4)
            ],
            3
        )

    def update(self, mousedown, pos):
        """
        Updates the hover state and toggles checked state if clicked.

        Parameters
        ----------
        mousedown : bool
            True if the mouse button is currently pressed.
        pos : tuple of int
            Current mouse position (x, y).

        Notes
        -----
        This method should be called every frame to handle interaction.
        """
        self._update_hover()

        # Click handling
        if mousedown and self.rect.collidepoint(pos):
            self.checked = not self.checked

    def draw(self):
        """
        Draws the checkbox on its assigned Pygame surface.

        This includes:
        - Background and edges.
        - Hover overlay with transparency.
        - Check mark if the checkbox is checked.
        """
        self._update_hover()

        # Draw background and edges
        pygame.draw.rect(self.screen, self.bg_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(self.screen, self.edge_color, self.rect, 2, border_radius=self.border_radius)

        # Draw hover overlay
        if self.hover:
            overlay = pygame.Surface((self.size, self.size), flags=pygame.SRCALPHA)  # type: ignore
            pygame.draw.rect(
                overlay,
                (*self.theme.idle, 95),
                overlay.get_rect(),
                border_radius=self.border_radius
            )
            self.screen.blit(overlay, self.rect.topleft)

        # Draw check mark if checked
        if self.checked:
            self._draw_check_mark()