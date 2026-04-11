import pygame
from pygets.core.widgets import WidgetBase
from pygets.utils.validators import *


class Combobox(WidgetBase):
    """
    Interactive combobox (dropdown) widget with hover, selection, and open/close behavior.

    Parameters
    ----------
    x, y : int
        Position of the Combobox on the screen.
    width : int
        Width of the combobox in pixels.
    height : int
        Height of the main box of the combobox in pixels.
    screen : pygame.Surface
        Surface where the combobox will be drawn.
    options : list of str
        List of selectable options.
    font : pygame.font.Font
        Font used to render the text.
    theme : Theme
        Theme instance providing colors (background, foreground, text, accent, idle).
    border_radius : int, optional
        Corner radius for the main box and options. Default is 10.

    Attributes
    ----------
    options : list of str
        Available options to select from.
    selected_index : int
        Index of the currently selected option.
    hover : bool
        True if the mouse is over the main box.
    hover_option : int
        Index of the option being hovered over. -1 if none.
    open : bool
        True if the combobox is open (options visible).
    height_option : int
        Height of each option box in pixels.
    width : int
        Width of the combobox.
    height : int
        Height of the main box.
    bg_color : tuple
        Background color from theme.
    edge_color : tuple
        Border color from theme.
    text_color : tuple
        Text color from theme.

    Methods
    -------
    value :
        Returns the currently selected option.
    update_hover():
        Updates hover states for the main box and options.
    handle_event(event):
        Handles mouse clicks for opening/closing and selecting options.
    draw():
        Draws the combobox, selected value, options (if open), and hover/selection effects.
    _draw_arrow():
        Draws the dropdown arrow, pointing up if open, down otherwise.
    _draw_options():
        Draws the options below the main box if the combobox is open.
    """

    def __init__(
        self, x, y, width, height, screen, options, font, theme, border_radius=10
    ):

        validate_position(x, y, screen, width, height)
        validate_size(width, height)
        validate_screen(screen)
        validate_theme(theme)
        validate_combobox(options, font)

        super().__init__(x, y, width, height, screen)

        self.options = options
        self.font = font
        self.border_radius = border_radius
        self.open = False
        self.selected_index = 0
        self.hover_option = -1
        self.height_option = height
        self.hover = False

        self.width = width
        self.height = height
        self.theme = theme

        self.bg_color = theme.background
        self.edge_color = theme.foreground
        self.text_color = theme.text

    @property
    def value(self):
        """Returns the currently selected option."""
        return self.options[self.selected_index]

    def _draw_arrow(self):
        """Draws the dropdown arrow, pointing up if open, down otherwise."""
        center_y = self.rect.centery
        if self.open:
            pygame.draw.polygon(
                self.screen,
                self.text_color,
                [
                    (self.rect.right - 15, center_y + 4),
                    (self.rect.right - 5, center_y + 4),
                    (self.rect.right - 10, center_y - 4),
                ]
            )
        else:
            pygame.draw.polygon(
                self.screen,
                self.text_color,
                [
                    (self.rect.right - 15, center_y - 4),
                    (self.rect.right - 5, center_y - 4),
                    (self.rect.right - 10, center_y + 4),
                ]
            )

    def _draw_options(self):
        """Draws the options below the main box if the combobox is open."""
        if not self.open:
            return

        for i, option in enumerate(self.options):
            rect_option = pygame.Rect(
                self.rect.x,
                self.rect.y + self.rect.height + i * self.height_option,
                self.rect.width,
                self.height_option
            )

            # Background and border
            pygame.draw.rect(self.screen, self.bg_color, rect_option)
            pygame.draw.rect(self.screen, self.edge_color, rect_option, 1)

            # Highlight selected or hovered option
            if i == self.selected_index or i == self.hover_option:
                overlay = pygame.Surface((rect_option.width, rect_option.height), flags=pygame.SRCALPHA)  # type: ignore
                pygame.draw.rect(
                    overlay,
                    (*self.theme.accent, 95),
                    overlay.get_rect()
                )
                self.screen.blit(overlay, rect_option.topleft)

            # Draw text
            text_option = self.font.render(option, True, self.text_color)
            text_y_op = rect_option.y + (rect_option.height - text_option.get_height()) // 2
            self.screen.blit(text_option, (rect_option.x + 8, text_y_op))

    def update_hover(self):
        """
        Updates hover states for the main box and each option if open.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        self.hover_option = -1
        if self.open:
            for i, _ in enumerate(self.options):
                rect_option = pygame.Rect(
                    self.rect.x,
                    self.rect.y + self.rect.height + i * self.height_option,
                    self.rect.width,
                    self.height_option
                )
                if rect_option.collidepoint(mouse_pos):
                    self.hover_option = i
                    break

    def handle_event(self, event):
        """
        Handles mouse clicks for opening/closing the combobox and selecting options.

        Parameters
        ----------
        event : pygame.event.Event
            Pygame event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Click on the main box
            if self.rect.collidepoint(event.pos):
                self.open = not self.open
                return

            # Click on the options
            if self.open:
                for i, _ in enumerate(self.options):
                    rect_option = pygame.Rect(
                        self.rect.x,
                        self.rect.y + self.rect.height + i * self.height_option,
                        self.rect.width,
                        self.height_option
                    )
                    if rect_option.collidepoint(event.pos):
                        self.selected_index = i
                        self.open = False
                        return
                self.open = False

    def draw(self):
        """Draws the combobox, the selected value, arrow, and options (if open)."""
        self.update_hover()

        # Main box
        pygame.draw.rect(self.screen, self.bg_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(self.screen, self.edge_color, self.rect, 2, border_radius=self.border_radius)

        # Hover overlay
        if self.hover:
            overlay = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)  # type: ignore
            pygame.draw.rect(
                overlay,
                (*self.theme.idle, 95),
                overlay.get_rect(),
                border_radius=self.border_radius
            )
            self.screen.blit(overlay, self.rect.topleft)

        # Selected text
        text = self.font.render(self.value, True, self.text_color)
        text_y = self.rect.y + (self.rect.height - text.get_height()) // 2
        self.screen.blit(text, (self.rect.x + 8, text_y))

        # Draw arrow and options
        self._draw_arrow()
        self._draw_options()