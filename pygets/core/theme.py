"""
theme.py

This module defines the `Theme` class for Pygets widgets, which allows 
customization of colors for backgrounds, text, buttons, accents, and states.

It also provides several predefined themes: Light, Dark, Forest, Ocean, 
Sunset, PurpleNight, and Silver, each with specific color schemes for 
widgets and UI elements.
"""

from pygets.utils.colors import colors


class Theme:
    def __init__(
        self,
        name: str,
        background,
        foreground,
        accent,
        idle,
        text
    ):
        self.name = name
        self.background = background
        self.foreground = foreground
        self.accent = accent
        self.idle = idle
        self.text = text


# BASIC THEMES

LightTheme = Theme(
    name="light",
    background=colors["WHITE"],
    foreground=colors["BLACK"],
    accent=colors["BLUISH_GRAY"],
    idle=colors["GRAY"],
    text= colors["BLACK"],
)

DarkTheme = Theme(
    name="dark",
    background=colors["DARK_GRAY"],
    foreground=colors["WHITE"],
    accent=colors["TURQUOISE"],
    idle=colors["GRAY"],
    text= colors["WHITE"],
)

ForestTheme = Theme(
    name="forest",
    background=colors["OLIVE"],
    foreground=colors["WHITE"],
    accent=colors["MINT_GREEN"],
    idle=colors["DARK_GRAY"],
    text= colors["WHITE"],
)

OceanTheme = Theme(
    name="ocean",
    background=colors["BLUE"],
    foreground=colors["WHITE"],
    accent=colors["CYAN"],
    idle=colors["LIGHT_BLUE"],
    text= colors["WHITE"],
)

SunsetTheme = Theme(
    name="sunset",
    background=colors["DARK_ORANGE"],
    foreground=colors["WHITE"],
    accent=colors["GOLD"],
    idle=colors["SAND"],
    text= colors["WHITE"],
)

PurpleNightTheme = Theme(
    name="purple_night",
    background=colors["PURPLE"],
    foreground=colors["LAVENDER"],
    accent=colors["MAGENTA"],
    idle=colors["GRAY"],
    text= colors["LAVENDER"],
)

SilverTheme = Theme(
    name="silver",
    background=colors["SILVER"],
    foreground=colors["BLACK"],
    accent=colors["BLUISH_GRAY"],
    idle=colors["DARK_GRAY"],
    text= colors["BLACK"],
)


# THEMES REGISTRATION

themes = {
    LightTheme.name: LightTheme,
    DarkTheme.name: DarkTheme,
    ForestTheme.name: ForestTheme,
    OceanTheme.name: OceanTheme,
    SunsetTheme.name: SunsetTheme,
    PurpleNightTheme.name: PurpleNightTheme,
    SilverTheme.name: SilverTheme,
}
