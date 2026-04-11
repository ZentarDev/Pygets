import pygame
from pygets.core.widgets import WidgetBase
from pygets.utils.validators import *


class Button(WidgetBase):
    """
    Interactive button widget with support for text, images, and hover effects.

    This widget can display a text label, an optional image, or both, and 
    automatically calculates its size. It supports hover effects and optional 
    edges/borders.

    Parameters
    ----------
    x, y : int
        Position of the button on the screen.
    font : pygame.font.Font
        Font object used for rendering text.
    screen : pygame.Surface
        Pygame surface where the button will be drawn.
    theme : Theme
        Theme instance providing button colors.
    width : int, optional
        Width of the button. Default: None (auto-calculated).
    height : int, optional
        Height of the button. Default: None (auto-calculated).
    image : pygame.Surface, optional
        Image to display on the button. Default: None.
    text : str, optional
        Text label for the button. Default: None.
    edges : bool, optional
        Whether to draw borders. Default: True.
    border_radius : int, optional
        Corner radius in pixels. Default: 20.
    spacing : int, optional
        Spacing between image and text in pixels. Default: 5.

    Attributes
    ----------
    width : int
        Calculated width of the button.
    height : int
        Calculated height of the button.
    hover : bool
        True if mouse is hovering over the button.
    text_pygame : pygame.Surface
        Rendered Pygame surface of the text.
    bg_color : tuple
        Background color of the button.

    Methods
    -------
    update_hover():
        Updates the hover state based on mouse position.
    draw():
        Draws the button on the assigned Pygame surface.
    _calculate_dimensions():
        Calculates and sets the button's widht and height based on content
    _draw_centered():
        Draws a given surface centered within the button.
    """

    def __init__(
        self, x, y, font, screen, theme, width=None, height=None,
        image=None, text=None, edges=True, border_radius=20, spacing=5
    ):

        validate_position(x, y, screen, width, height)
        validate_size(width, height)
        validate_screen(screen)
        validate_theme(theme)
        validate_button(text, image, font)

        self.theme = theme
        self.bg_color = self.theme.background
        self.hover = False

        self.edges = edges
        self.border_radius = border_radius
        self.spacing = spacing

        self.text = text
        self.text_pygame = None
        self.image = image
        self.font = font
        self.height = height
        self.width = width

        self.text_pygame = self.font.render(self.text, True, self.theme.text)
        self._calculate_dimensions()

        super().__init__(x, y, self.width, self.height, screen)

    def _calculate_dimensions(self):
        """
        Calculates and sets the button's width and height based on content.

        Modifies:
            self.width
            self.height

        Notes:
            Called internally during initialization.
        """
        img_width = self.image.get_width() if self.image else 0
        img_height = self.image.get_height() if self.image else 0
        text_width = self.text_pygame.get_width() if self.text_pygame else 0
        text_height = self.text_pygame.get_height() if self.text_pygame else 0

        side_by_side_width = img_width + self.spacing + text_width if self.image and self.text_pygame else max(img_width, text_width)
        self.width = self.width or max(100, side_by_side_width + 20)
        if self.height is None:
            if self.text_pygame or self.image:
                self.height = max(img_height, text_height) + 10
            else:
                self.height = 40

    def _draw_centered(self, surface):
        """
        Draws a given surface centered within the button.

        Parameters
        ----------
        surface : pygame.Surface
            The Pygame surface to be centered and blitted.

        Notes:
            Internal helper for draw method.
        """
        x = self.rect.x + (self.rect.width - surface.get_width()) // 2
        y = self.rect.y + (self.rect.height - surface.get_height()) // 2
        self.screen.blit(surface, (x, y))

    def update_hover(self):
        """
        Updates the hover state of the button.

        Sets self.hover to True if the mouse is currently over the button,
        otherwise sets it to False.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)

    def draw(self):
        """
        Draws the button on its assigned Pygame surface.

        This includes the background, hover overlay, edges, image, and text.
        Automatically handles image scaling and text cropping if necessary.
        """
        self.update_hover()
        pygame.draw.rect(self.screen, self.bg_color, self.rect, border_radius=self.border_radius)

        if self.hover:
            overlay = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)  # type: ignore
            pygame.draw.rect(
                overlay,
                (*self.theme.idle, 95),
                overlay.get_rect(),
                border_radius=self.border_radius
            )
            self.screen.blit(overlay, self.rect.topleft)

        if self.edges:
            pygame.draw.rect(
                self.screen,
                self.theme.foreground,
                self.rect,
                width=2,
                border_radius=self.border_radius
            )

        margin = 10
        available_width = self.rect.width - 2 * margin

        img_to_draw = self.image
        text_to_draw = self.text

        # Scale image if too wide
        if self.image and self.image.get_width() > available_width // 2 and self.text_pygame:
            scale_factor = (available_width // 2) / self.image.get_width()
            new_w = int(self.image.get_width() * scale_factor)
            new_h = int(self.image.get_height() * scale_factor)
            img_to_draw = pygame.transform.smoothscale(self.image, (new_w, new_h))

        text_to_draw_surface = None
        if self.text_pygame:
            max_text_width = available_width - (img_to_draw.get_width() + self.spacing if img_to_draw else 0)
            displayed_text = ""
            full_text_width = self.font.size(text_to_draw or "")[0]

            if full_text_width <= max_text_width:
                displayed_text = text_to_draw or ""
            else:
                for char in text_to_draw or "":
                    if self.font.size(displayed_text + char + "…")[0] > max_text_width:
                        break
                    displayed_text += char
                displayed_text += "..."
            text_to_draw_surface = self.font.render(displayed_text, True, self.theme.text)

        # Decide layout
        if img_to_draw and text_to_draw_surface and (img_to_draw.get_width() + self.spacing + text_to_draw_surface.get_width() <= available_width):
            # side by side
            x_start = self.rect.x + (self.rect.width - (img_to_draw.get_width() + self.spacing + text_to_draw_surface.get_width())) // 2
            y_center = self.rect.y + (self.rect.height - max(img_to_draw.get_height(), text_to_draw_surface.get_height())) // 2
            self.screen.blit(img_to_draw, (x_start, y_center))
            self.screen.blit(text_to_draw_surface, (x_start + img_to_draw.get_width() + self.spacing, y_center))
        elif img_to_draw and text_to_draw_surface:
            # stacked
            total_height = img_to_draw.get_height() + self.spacing + text_to_draw_surface.get_height()
            y_start = self.rect.y + (self.rect.height - total_height) // 2
            x_img = self.rect.x + (self.rect.width - img_to_draw.get_width()) // 2
            self.screen.blit(img_to_draw, (x_img, y_start))
            x_text = self.rect.x + (self.rect.width - text_to_draw_surface.get_width()) // 2
            self.screen.blit(text_to_draw_surface, (x_text, y_start + img_to_draw.get_height() + self.spacing))
        elif img_to_draw:
            self._draw_centered(img_to_draw)
        elif text_to_draw_surface:
            self._draw_centered(text_to_draw_surface)