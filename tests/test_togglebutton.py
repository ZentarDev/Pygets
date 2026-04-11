import pytest
import pygame

from pygets.widgets.togglebutton import Togglebutton
from pygets.core.theme import themes

def make_togglebutton(screen, **kwargs):
    return Togglebutton(
        x=10,
        y=10,
        screen=screen,
        theme=themes["purple_night"],
        width=60,
        height=30,
        **kwargs,
    )


@pytest.mark.parametrize("active", [False, True])
def test_togglebutton_initialization(small_screen, active):
    toggle = make_togglebutton(small_screen, active=active)

    assert toggle.active is active
    assert toggle.width == 60
    assert toggle.height == 30
    assert toggle.radio == 15
    assert toggle.rect.topleft == (10, 10)
    assert toggle.rect.size == (60, 30)
    assert toggle.bg_color == themes["purple_night"].background
    assert toggle.edge_color == themes["purple_night"].foreground
    assert toggle.toggle_color == themes["purple_night"].accent


@pytest.mark.parametrize(
    ("pos", "expected_hover"),
    [
        ((15, 15), True),
        ((100, 100), False),
    ],
)
def test_togglebutton_update_sets_hover_state(small_screen, pos, expected_hover):
    toggle = make_togglebutton(small_screen)

    toggle.update(mousedown=False, pos=pos)
    assert toggle.hover is expected_hover
    assert toggle.active is False


def test_togglebutton_update_click_toggles_state(small_screen):
    toggle = make_togglebutton(small_screen, active=False)
    click_pos = toggle.rect.center

    toggle.update(mousedown=True, pos=click_pos)
    assert toggle.active is True

    toggle.update(mousedown=True, pos=click_pos)
    assert toggle.active is False


def test_togglebutton_click_outside_does_not_toggle_state(small_screen):
    toggle = make_togglebutton(small_screen, active=False)

    toggle.update(mousedown=True, pos=(toggle.rect.right + 20, toggle.rect.bottom + 20))

    assert toggle.active is False


def test_togglebutton_draw_renders_track_color(small_screen):
    toggle = make_togglebutton(small_screen, active=False)

    toggle.draw()
    inactive_pixel = toggle.screen.get_at(toggle.rect.center)
    assert inactive_pixel[:3] == themes["purple_night"].foreground

    toggle.active = True
    toggle.draw()
    active_pixel = toggle.screen.get_at((toggle.rect.x + 4, toggle.rect.centery))
    assert active_pixel[:3] == themes["purple_night"].background
