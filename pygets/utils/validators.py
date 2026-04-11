import pygame


# Base validations (shared)

def validate_position(x, y, screen=None, width=None, height=None):
    if x is not None and not isinstance(x, (int, float)):
        raise TypeError("'x' must be a number (int or float) if provided.")
    if y is not None and not isinstance(y, (int, float)):
        raise TypeError("'y' must be a number (int or float) if provided.")

    if screen is not None:
        if not isinstance(screen, pygame.Surface):
            raise TypeError("'screen' must be a pygame.Surface.")

        screen_width, screen_height = screen.get_size()

        if x is not None and x < 0:
            raise ValueError("Position 'x' cannot be negative.")
        if y is not None and y < 0:
            raise ValueError("Position 'y' cannot be negative.")

        if width is not None and x is not None and x + width > screen_width:
            raise ValueError("Widget exceeds screen width.")

        if height is not None and y is not None and y + height > screen_height:
            raise ValueError("Widget exceeds screen height.")

def validate_size(width, height):
    if width is not None and width <= 0:
        raise ValueError("'width' must be greater than 0.")
    if height is not None and height <= 0:
        raise ValueError("'height' must be greater than 0.")

def validate_screen(screen):
    if not isinstance(screen, pygame.Surface):
        raise TypeError("'screen' must be a pygame.Surface.")

def validate_theme(theme, extra_attrs=None):
    required = ["background", "accent", "text", "foreground"]
    if extra_attrs:
        required += extra_attrs

    for attr in required:
        if not hasattr(theme, attr):
            raise AttributeError(f"'theme' must have attribute '{attr}'.")


# Button

def validate_button(text, image, font):
    if text is None and image is None:
        raise ValueError("Button requires either 'text' or 'image'.")

    if text is not None and font is None:
        raise ValueError("'font' must be provided when using 'text'.")

    if image is not None and not isinstance(image, pygame.Surface):
        raise TypeError("'image' must be a pygame.Surface.")


# Combobox

def validate_combobox(options, font):
    if not isinstance(options, (list, tuple)) or len(options) == 0:
        raise ValueError("'options' must be a non-empty list or tuple.")

    if not all(isinstance(opt, str) for opt in options):
        raise TypeError("All 'options' must be strings.")

    if font is None:
        raise ValueError("'font' is required for Combobox.")


# Slider

def validate_slider(min_val, max_val, initial_value):
    if not isinstance(min_val, (int, float)) or not isinstance(max_val, (int, float)):
        raise TypeError("'min_val' and 'max_val' must be numbers.")

    if min_val >= max_val:
        raise ValueError("'min_val' must be less than 'max_val'.")

    if not (min_val <= initial_value <= max_val):
        raise ValueError("'initial_value' must be between min_val and max_val.")


# Checkbox

def validate_checkbox(size, checked):
    if not isinstance(size, int) or size <= 0:
        raise ValueError("'size' must be a positive integer.")

    if not isinstance(checked, bool):
        raise TypeError("'checked' must be a boolean.")


# Togglebutton

def validate_toggle(width, height, active):
    if width <= 0 or height <= 0:
        raise ValueError("'width' and 'height' must be greater than 0.")

    if not isinstance(active, bool):
        raise TypeError("'active' must be a boolean.")


# Textbox

def validate_textbox(font, max_characters, function):
    if font is None:
        raise ValueError("'font' is required for Textbox.")

    if not isinstance(max_characters, int) or max_characters <= 0:
        raise ValueError("'max_characters' must be a positive integer.")

    if function is not None and not callable(function):
        raise TypeError("'function' must be callable.")


# Popup

def validate_popup(title, message, font, title_font, screen_width, screen_height):
    if not isinstance(title, str):
        raise TypeError("'title' must be a string.")
    if message is not None and not isinstance(message, str):
        raise TypeError("'message' must be a string if provided.")
    if not isinstance(font, pygame.font.Font):
        raise TypeError("'font' must be a pygame.font.Font.")
    if not isinstance(title_font, pygame.font.Font):
        raise TypeError("'title_font' must be a pygame.font.Font.")
    if not isinstance(screen_width, int) or screen_width <= 0:
        raise ValueError("'screen_width' must be a positive integer.")
    if not isinstance(screen_height, int) or screen_height <= 0:
        raise ValueError("'screen_height' must be a positive integer.")