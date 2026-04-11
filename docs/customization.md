# Customization

PyGets customization is centered around `Theme` objects plus a few widget-level sizing and layout parameters.

## Theme model

Each theme defines five color roles:

- `background`
- `foreground`
- `accent`
- `idle`
- `text`

The `Theme` class is available from `pygets.core.theme`.

```python
from pygets.core.theme import Theme

custom_theme = Theme(
    name="custom",
    background=(28, 28, 32),
    foreground=(240, 240, 240),
    accent=(80, 180, 255),
    idle=(110, 110, 120),
    text=(255, 255, 255),
)
```

## Built-in themes

PyGets ships with these predefined themes in `pygets.core.theme.themes`:

- `light`
- `dark`
- `forest`
- `ocean`
- `sunset`
- `purple_night`
- `silver`

Example:

```python
from pygets.core.theme import themes

theme = themes["forest"]
```

## Built-in color palette

If you prefer named RGB values instead of hardcoding tuples, use `pygets.utils.colors.colors`.

Examples available in the palette include:

- `WHITE`, `BLACK`, `GRAY`, `DARK_GRAY`
- `BLUE`, `LIGHT_BLUE`, `TURQUOISE`
- `GREEN`, `LIGHT_GREEN`, `MINT_GREEN`, `OLIVE`
- `DARK_ORANGE`, `GOLD`, `PURPLE`, `LAVENDER`
- `SAND`, `SILVER`, `BLUISH_GRAY`

```python
from pygets.core.theme import Theme
from pygets.utils.colors import colors

theme = Theme(
    name="studio",
    background=colors["BLACK"],
    foreground=colors["WHITE"],
    accent=colors["TURQUOISE"],
    idle=colors["DARK_GRAY"],
    text=colors["WHITE"],
)
```

## Widget-level customization

### Button

Useful parameters:

- `width` and `height` to override auto sizing
- `image` to add an icon
- `text` to show a label
- `edges` to enable or disable the border
- `border_radius` for corner roundness
- `spacing` for image/text separation

```python
button = Button(
    x=40,
    y=40,
    font=font,
    screen=screen,
    theme=theme,
    text="Export",
    width=200,
    border_radius=24,
    spacing=12,
)
```

### Checkbox

Useful parameters:

- `checked` for the initial state
- `size` for the box size
- `border_radius` for square vs rounded corners

```python
checkbox = Checkbox(
    x=40,
    y=120,
    screen=screen,
    theme=theme,
    checked=True,
    size=24,
    border_radius=6,
)
```

### Combobox

Useful parameters:

- `width` and `height`
- `options`
- `border_radius`

```python
combo = Combobox(
    x=40,
    y=180,
    width=260,
    height=36,
    screen=screen,
    options=["Python", "Rust", "Go"],
    font=font,
    theme=theme,
    border_radius=12,
)
```

### Textbox

Useful parameters:

- `placeholder`
- `width`
- `max_characters`
- `border_radius`
- `function` callback when Enter is pressed

```python
textbox = Textbox(
    x=40,
    y=250,
    screen=screen,
    font=font,
    theme=theme,
    placeholder="Write your email...",
    width=360,
    max_characters=120,
    border_radius=14,
)
```

### Slider

Useful parameters:

- `width` and `height`
- `min_val`
- `max_val`
- `initial_value`

```python
slider = Slider(
    x=40,
    y=330,
    width=300,
    height=8,
    screen=screen,
    theme=theme,
    min_val=0,
    max_val=1,
    initial_value=0.5,
)
```

### Togglebutton

Useful parameters:

- `width` and `height`
- `active`

```python
toggle = Togglebutton(
    x=40,
    y=390,
    screen=screen,
    theme=theme,
    width=72,
    height=36,
    active=True,
)
```

### Popup

Useful parameters:

- `title` and `message`
- `width` and `height`
- `font` and `title_font`
- `theme`

```python
popup = Popup(
    title="Saved",
    message="Your settings were updated successfully.",
    font=font,
    title_font=title_font,
    screen=screen,
    screen_width=800,
    screen_height=600,
    width=420,
    height=220,
    theme=theme,
)
```

## Practical guidance

- Use `theme.background` for widget surfaces and a separate window background for contrast.
- Keep `theme.text` and `theme.foreground` high-contrast, especially for `Textbox` and `Combobox`.
- Prefer larger `border_radius` values for soft UI and small values for more compact tooling interfaces.
- When a widget supports hover, `theme.idle` controls the overlay tint that appears on pointer focus.
