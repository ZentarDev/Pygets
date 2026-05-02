# Getting Started

This guide shows the minimum setup required to use PyGets in a `pygame` application.

## Requirements

- Python `3.10+`
- `pygame`
- `pyperclip`

PyGets declares its runtime dependencies in `pyproject.toml`, so installing the package is enough:

```bash
pip install .
```

If you are working inside the repository:

```bash
pip install -e .
```

## Basic application loop

PyGets widgets are designed to be created with a target `pygame.Surface` and then updated or drawn inside the normal `pygame` loop.

```python
import pygame

from pygets.core.theme import themes
from pygets.widgets import Button, Slider


pygame.init()

# Configuration of the screen
screen = pygame.display.set_mode((600, 400)) # (900, 600)
pygame.display.set_caption("PyGets Demo")

font = pygame.font.Font(None, 28)
theme = themes["dark"]


# The widgets
button = Button(
    x=215,
    y=150,
    font=font,
    screen=screen,
    theme=theme,
    text="Apply",
    width=100,
    height=50
)

slider = Slider(
    x=150,
    y=100,
    width=280,
    height=8,
    screen=screen,
    theme=theme,
    min_val=0,
    max_val=100,
    initial_value=35,
)


# Main loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        slider.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button.rect.collidepoint(event.pos):
                print(f"Current slider value: {slider.value:.0f}")

    screen.fill((96, 140, 168))
    button.draw()
    slider.draw()
    pygame.display.flip()

pygame.quit()
```

## Widget usage patterns

PyGets widgets follow three common interaction models:

### 1. Event-driven widgets

Use `handle_event(event)` inside the event loop.

- `Slider`
- `Textbox`
- `Combobox`
- `Popup`

### 2. Frame-updated widgets

Call `update(...)` once per frame, then `draw()`.

- `Checkbox`
- `Togglebutton`

Example:

```python
mousedown = False

for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mousedown = True

checkbox.update(mousedown, pygame.mouse.get_pos())
checkbox.draw()
```

### 3. Draw-only widgets with manual click detection

The `Button` widget exposes `rect`, so click handling is usually done by your main loop:

```python
if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    if button.rect.collidepoint(event.pos):
        print("Pressed")
```

## Textbox note

For a better typing experience, the repository examples enable key repeat:

```python
pygame.key.set_repeat(300, 40)
```

That is especially useful when working with `Textbox`.

## Available widgets

Import widgets from `pygets.widgets`:

```python
from pygets.widgets import (
    Button,
    Checkbox,
    Combobox,
    Popup,
    Slider,
    Textbox,
    Togglebutton,
)
```

## Example scripts

The `examples/` directory is the fastest way to learn the API:

- `example_button.py`
- `example_checkbox.py`
- `example_combobox.py`
- `example_popup.py`
- `example_slider.py`
- `example_textbox.py`
- `example_togglebutton.py`

Run one directly:

```bash
python examples/example_combobox.py
```

## Testing

Run the test suite from the repository root:

```bash
pytest tests
```
