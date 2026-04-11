import pygame
from pygets.widgets.button import Button
from pygets.utils.validators import *


class Popup:
    """
    Popup window widget with a title, message, and close button.

    Parameters
    ----------
    title : str
        Text displayed in the popup title bar.
    message : str
        Text displayed in the popup body.
    font : pygame.font.Font
        Font used for the message text.
    title_font : pygame.font.Font
        Font used for the title text.
    screen : pygame.Surface
        Surface where the popup is drawn.
    screen_width : int
        Width of the parent screen.
    screen_height : int
        Height of the parent screen.
    width : int
        Width of the popup window.
    height : int
        Height of the popup window.
    theme : Theme, optional
        Theme instance for colors (background, foreground, accent). Defaults to a light theme.

    Attributes
    ----------
    x : int
        X-coordinate of the popup (centered on screen).
    y : int
        Y-coordinate of the popup (centered on screen).
    rect : pygame.Rect
        Rectangle representing the popup area.
    visible : bool
        True if the popup is visible.
    padding : int
        Internal spacing for text inside the popup.
    close_button : Button
        Button instance used to close the popup.
    title_bar_color : tuple
        Color of the title bar.
    background_color : tuple
        Background color of the popup.
    border_color : tuple
        Color of the popup border.

    Methods
    -------
    update():
        Updates internal elements, like the close button position.
    handle_event(event):
        Handles mouse events for closing the popup.
    draw():
        Draws the popup, including title, message, and close button.
    _truncate_text():
        Truncate a single line of text to fit within max_width, adding an ellipsis if needed.
    _wrap_text():
        Wraps text into multiple lines to fit inside to popup content area.
    """

    def __init__(
        self, title, message, font, title_font, screen,
        screen_width, screen_height, width, height, theme=None
    ):
        validate_popup(title, message, font, title_font, screen_width, screen_height)
        validate_position(None, None, screen, width, height)
        validate_size(width, height)
        validate_screen(screen)
        validate_theme(theme)

        self.screen = screen
        self.title = title
        self.message = message
        self.font = font
        self.title_font = title_font
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

        from pygets.core.theme import themes
        self.theme = theme or themes["light"]

        self.title_bar_color = self.theme.accent
        self.background_color = self.theme.background
        self.border_color = self.theme.foreground

        # Center popup on screen
        self.x = (screen_width - width) // 2
        self.y = (screen_height - height) // 2
        self.rect = pygame.Rect(self.x, self.y, width, height)

        self.padding = 10
        self.visible = True

        # Close button
        button_size = self.title_font.get_height() + 7
        self.close_button = Button(
            x=self.rect.right - button_size - 5,
            y=self.rect.top + 5,
            font=self.title_font,
            screen=self.screen,
            theme=self.theme,
            width=button_size,
            height=button_size,
            text="X",
            edges=False
        )

    def _truncate_text(self, text, font, max_width):
        """
        Truncates a single line of text to fit within max_width, adding an ellipsis if needed.

        Parameters
        ----------
        text : str
            Text to truncate.
        font : pygame.font.Font
            Font used for measuring text width.
        max_width : int
            Maximum allowed width in pixels.

        Returns
        -------
        str
            Truncated text with ellipsis if necessary.
        """
        if font.size(text)[0] <= max_width:
            return text

        truncated = ""
        for char in text:
            if font.size(truncated + char + "…")[0] > max_width:
                break
            truncated += char

        return truncated + "..."

    def _wrap_text(self, text, font, max_width, max_height):
        """
        Wraps text into multiple lines to fit inside the popup content area.

        Parameters
        ----------
        text : str
            Text to wrap.
        font : pygame.font.Font
            Font used for measuring text width.
        max_width : int
            Maximum width for each line.
        max_height : int
            Maximum height for the content area.

        Returns
        -------
        list of str
            List of wrapped lines, truncated with ellipsis if text overflows.
        """
        words = text.split()
        lines = []
        current_line = ""
        line_height = font.get_height()
        max_lines = max_height // line_height

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.rstrip())
                current_line = word + " "
                if len(lines) >= max_lines:
                    break

        if current_line and len(lines) < max_lines:
            lines.append(current_line.rstrip())

        # Truncate last line if needed
        total_words_used = sum(len(line.split()) for line in lines)
        if total_words_used < len(words):
            last_line = lines[-1]
            truncated = ""
            for char in last_line:
                if font.size(truncated + char + "…")[0] > max_width:
                    break
                truncated += char
            lines[-1] = truncated + "..."

        return lines

    def update(self):
        """
        Updates internal elements, such as repositioning the close button.
        """
        if not self.visible:
            return

        self.close_button.rect.topleft = (
            self.rect.right - self.close_button.rect.width - 5,
            self.rect.top + 5
        )

    def handle_event(self, event):
        """
        Handles mouse events to close the popup.

        Parameters
        ----------
        event : pygame.event.Event
            Event to process.
        """
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.close_button.rect.collidepoint(event.pos):
                self.visible = False

    def draw(self):
        """
        Draws the popup window, including title bar, message, border, and close button.
        """
        if not self.visible:
            return

        title_bar_height = self.title_font.get_height() + 15

        # Background
        pygame.draw.rect(
            self.screen,
            self.background_color,
            self.rect,
            border_radius=10
        )

        # Title bar
        pygame.draw.rect(
            self.screen,
            self.title_bar_color,
            (self.rect.x, self.rect.y, self.rect.width, title_bar_height),
            border_top_left_radius=10,
            border_top_right_radius=10
        )

        # Border
        pygame.draw.rect(
            self.screen,
            self.border_color,
            self.rect,
            2,
            border_radius=10
        )

        # Separator
        pygame.draw.line(
            self.screen,
            self.border_color,
            (self.rect.left, self.rect.top + title_bar_height),
            (self.rect.right, self.rect.top + title_bar_height),
            2
        )

        # Title
        available_width = self.rect.width - self.padding * 2 - self.close_button.rect.width
        displayed_title = self._truncate_text(self.title, self.title_font, available_width)
        title_surface = self.title_font.render(displayed_title, True, self.border_color)
        title_rect = title_surface.get_rect()
        title_rect.left = self.rect.left + self.padding
        title_rect.centery = self.rect.top + title_bar_height // 2
        self.screen.blit(title_surface, title_rect)

        # Message
        if self.message:
            content_top = title_rect.bottom + 10
            content_height = self.rect.bottom - content_top - self.padding
            lines = self._wrap_text(self.message, self.font, self.rect.width - self.padding * 2, content_height)
            y_offset = content_top
            for line in lines:
                line_surface = self.font.render(line, True, self.border_color)
                line_rect = line_surface.get_rect()
                line_rect.centerx = self.rect.centerx
                line_rect.top = y_offset
                self.screen.blit(line_surface, line_rect)
                y_offset += self.font.get_height()

        # Close button
        self.close_button.draw()