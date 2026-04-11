import pygame
import pyperclip

from pygets.core.widgets import WidgetBase
from pygets.utils.validators import *
from pygets.utils.colors import colors


class Textbox(WidgetBase):
    """
    Text input box widget for typing and displaying text.

    Parameters
    ----------
    x, y : int
        Position of the textbox on the screen.
    screen : pygame.Surface
        Surface where the textbox is drawn.
    font : pygame.font.Font
        Font used to render the text.
    theme : Theme
        Theme instance defining colors.
    function : callable, optional
        Function called when Enter is pressed.
    placeholder : str, optional
        Placeholder text shown when textbox is empty (default "Write something...").
    width : int, optional
        Width of the textbox (default 300).
    max_characters : int, optional
        Maximum number of characters allowed (default 54).
    border_radius : int, optional
        Corner radius of the textbox (default 10).

    Attributes
    ----------
    textbox_content : str
        Current text inside the textbox.
    active : bool
        True if the textbox is focused for input.
    cursor_visible : bool
        Cursor visibility for blinking effect.
    cursor_position : int
        Position of the cursor in the text.

    Methods
    -------
    update_hover():
        Updates the hover state based on mouse position.
    handle_event(event):
        Handles mouse and keyboard events for text input.
    update():
        Updates the cursor blinking animation when active.
    draw():
        Draws the textbox with text, cursor, and visual effects.
    _update_rendering():
        Renders and updates the text surface for the given text
    """
    def __init__(self, x, y, screen, font, theme, function=None, placeholder="Write something...",
                 width=300, max_characters=54, border_radius=10):
        validate_position(x, y, screen, width, None)
        validate_screen(screen)
        validate_theme(theme, extra_attrs=["idle"])
        validate_textbox(font, max_characters, function)

        super().__init__(x, y, width, max(30, font.get_height() + 10), screen)

        self.font = font
        self.bg_color = theme.background
        self.inactive_color = theme.foreground
        self.active_color = theme.accent
        self.text_color = theme.text
        self.border_radius = border_radius
        self.textbox_content = ""
        self.max_characters = max_characters
        self.function = function
        self.hover = False
        self.theme = theme
        self.placeholder = placeholder
        self.placeholder_color = theme.idle
        self.surface_text_placeholder = self.font.render(placeholder, True, self.placeholder_color)
        self.active = False
        self.cursor_visible = False
        self.blink_time = 0
        self.cursor_position = 0
        self.offset = 0
        self.__accepted_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-+()[]{}:;\"',_.@?/\\><*&%$#!=+|~ "

    def _update_rendering(self, text):
        """
        Renders and updates the text surface for the given text.

        Parameters
        ----------
        text : str
            Text to render.
        """
        self.text_surface = self.font.render(text, True, self.text_color)
        self.rect.h = max(self.rect.h, self.text_surface.get_height() + 10)

    def update_hover(self):
        """
        Updates the hover state based on mouse position.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.cursor_visible = True
                self.blink_time = pygame.time.get_ticks()
                x_relative = event.pos[0] - self.rect.x - 5 + self.offset
                self.cursor_position = len(self.textbox_content)
                for i in range(len(self.textbox_content) + 1):
                    width = self.font.size(self.textbox_content[:i])[0]
                    if width >= x_relative:
                        self.cursor_position = i
                        break
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_CTRL and event.key == pygame.K_v:
                try:
                    pasted_text = pyperclip.paste()
                except Exception:
                    pasted_text = ""
                pasted_text = pasted_text.replace('\n', ' ').replace('\r', ' ')
                if pasted_text:
                    if not len(pasted_text) + len(self.textbox_content) > self.max_characters:
                        self.textbox_content = self.textbox_content[:self.cursor_position] + pasted_text + self.textbox_content[self.cursor_position:]
                        self.cursor_position += len(pasted_text)
                    else:
                        for char in pasted_text:
                            if not len(self.textbox_content) + 1 > self.max_characters:
                                self.textbox_content = self.textbox_content[:self.cursor_position] + char + self.textbox_content[self.cursor_position:]
                                self.cursor_position += 1
                            else:
                                break

            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.active = False
                if self.function is not None:
                    self.function()

            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_position > 0:
                    self.textbox_content = self.textbox_content[:self.cursor_position - 1] + self.textbox_content[self.cursor_position:]
                    self.cursor_position -= 1

            elif event.key == pygame.K_DELETE:
                if self.cursor_position < len(self.textbox_content):
                    self.textbox_content = self.textbox_content[:self.cursor_position] + self.textbox_content[self.cursor_position + 1:]

            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_HOME, pygame.K_END):
                if event.key == pygame.K_LEFT and self.cursor_position > 0:
                    self.cursor_position -= 1
                elif event.key == pygame.K_RIGHT and self.cursor_position < len(self.textbox_content):
                    self.cursor_position += 1
                elif event.key == pygame.K_HOME:
                    self.cursor_position = 0
                elif event.key == pygame.K_END:
                    self.cursor_position = len(self.textbox_content)

            elif event.unicode in self.__accepted_characters and len(self.textbox_content) < self.max_characters and event.unicode != "":
                character = event.unicode
                if event.mod & pygame.KMOD_SHIFT and character.isalpha():
                    character = character.upper()
                if character.isprintable():
                    self.textbox_content = self.textbox_content[:self.cursor_position] + character + self.textbox_content[self.cursor_position:]
                    self.cursor_position += 1

            self._update_rendering(self.textbox_content)
            self.cursor_visible = True
            self.blink_time = pygame.time.get_ticks()

    def update(self):
        if self.active and pygame.time.get_ticks() - self.blink_time > 500:
            self.cursor_visible = not self.cursor_visible
            self.blink_time = pygame.time.get_ticks()

    def draw(self):
        self.update_hover()
        pygame.draw.rect(self.screen, self.bg_color, self.rect, border_radius=self.border_radius)
        edge_color = self.active_color if self.active else self.inactive_color
        pygame.draw.rect(self.screen, edge_color, self.rect, 2, border_radius=self.border_radius)

        if self.hover:
            overlay = pygame.Surface((self.rect.width, self.rect.height), flags=pygame.SRCALPHA)
            pygame.draw.rect(overlay, (*self.theme.idle, 95), overlay.get_rect(), border_radius=self.border_radius)
            self.screen.blit(overlay, self.rect.topleft)

        margin = 5
        available_space = self.rect.w - 2 * margin
        text_until_cursor = self.textbox_content[:self.cursor_position]
        width_until_cursor = self.font.size(text_until_cursor)[0]

        while width_until_cursor - self.offset > available_space:
            self.offset += 10
        while width_until_cursor - self.offset < 0 and self.offset > 0:
            self.offset -= 10

        full_surface = self.font.render(self.textbox_content, True, self.text_color)
        visible_surface = pygame.Surface((available_space, self.rect.h), pygame.SRCALPHA)
        visible_surface.fill((0, 0, 0, 0))
        visible_surface.blit(full_surface, (-self.offset, (self.rect.h - full_surface.get_height()) // 2))
        self.screen.blit(visible_surface, (self.rect.x + margin, self.rect.y))

        if self.textbox_content == "" and self.placeholder:
            placeholder = self.placeholder
            text_mostrado = ""
            for char in placeholder:
                if self.font.size(text_mostrado + char + "…")[0] > available_space:
                    break
                text_mostrado += char
            if text_mostrado != placeholder:
                text_mostrado += "…"
            superficie_placeholder = self.font.render(text_mostrado, True, self.placeholder_color)
            self.screen.blit(superficie_placeholder, (self.rect.x + margin, self.rect.y + (self.rect.h - superficie_placeholder.get_height()) // 2))

        if self.active and self.cursor_visible:
            pos_x = self.rect.x + margin + width_until_cursor - self.offset
            rect_cursor = pygame.Rect(pos_x, self.rect.y + 5, 2, self.rect.h - 10)
            pygame.draw.rect(self.screen, colors["BLACK"], rect_cursor)