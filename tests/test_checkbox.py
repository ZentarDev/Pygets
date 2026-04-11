import pygame
import pytest

from pygets.widgets.checkbox import Checkbox
from pygets.core.theme import themes

def make_checkbox(screen, **kwargs):
    return Checkbox(
        x=10,
        y=10,
        screen=screen,
        theme=themes["dark"],
        **kwargs,
    )


@pytest.mark.parametrize(
    ("size", "checked"),
    [
        (20, False),
        (30, True),
        (40, False),
    ],
)
def test_checkbox_initialization(small_screen, size, checked):
    checkbox = make_checkbox(small_screen, size=size, checked=checked)

    assert checkbox.checked is checked
    assert checkbox.size == size
    assert checkbox.rect.size == (size, size)
    assert checkbox.rect.topleft == (10, 10)
    assert checkbox.bg_color == themes["dark"].background
    assert checkbox.edge_color == themes["dark"].foreground
    assert checkbox.hover is False


def test_checkbox_hover_state_updates_with_mouse_position(monkeypatch, small_screen):
    checkbox = make_checkbox(small_screen)

    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: checkbox.rect.center)
    checkbox.update(mousedown=False, pos=(0, 0))
    assert checkbox.hover is True

    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (checkbox.rect.right + 10, checkbox.rect.bottom + 10))
    checkbox.update(mousedown=False, pos=(0, 0))
    assert checkbox.hover is False


def test_checkbox_click_toggle_changes_checked_state(small_screen):
    checkbox = make_checkbox(small_screen, checked=False)

    checkbox.update(mousedown=True, pos=checkbox.rect.center)
    assert checkbox.checked is True

    checkbox.update(mousedown=True, pos=checkbox.rect.center)
    assert checkbox.checked is False


def test_checkbox_click_outside_does_not_change_state(small_screen):
    checkbox = make_checkbox(small_screen, checked=True)

    checkbox.update(mousedown=True, pos=(checkbox.rect.right + 20, checkbox.rect.bottom + 20))

    assert checkbox.checked is True


def test_checkbox_draw_renders_background(monkeypatch, small_screen):
    checkbox = make_checkbox(small_screen, checked=True, size=24)
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (checkbox.rect.right + 20, checkbox.rect.bottom + 20))

    checkbox.draw()

    interior_pixel = checkbox.screen.get_at((checkbox.rect.x + 2, checkbox.rect.y + 2))
    assert interior_pixel[:3] == checkbox.bg_color
