import pygame

from pygets.widgets.button import Button
from pygets.core.theme import themes

def make_button(screen, font, **kwargs):
    params = {
        "text": "Click",
        **kwargs,
    }
    return Button(
        x=10,
        y=10,
        font=font,
        screen=screen,
        theme=themes["light"],
        **params,
    )


def test_button_initialization_uses_content_based_dimensions(small_screen, font):
    button = make_button(small_screen, font)

    assert button.text_pygame is not None
    assert button.text == "Click"
    assert button.width >= 100  # type: ignore[operator]
    assert button.height == button.text_pygame.get_height() + 10
    assert button.rect.width == button.width
    assert button.rect.height == button.height
    assert button.bg_color == themes["light"].background
    assert button.hover is False


def test_button_initialization_respects_explicit_dimensions(small_screen, font):
    button = make_button(small_screen, font, width=160, height=48, text="Wide")

    assert button.width == 160
    assert button.height == 48
    assert button.rect.size == (160, 48)


def test_button_update_hover_changes_hover_state(monkeypatch, small_screen, font):
    button = make_button(small_screen, font, text="Hover")

    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (button.rect.centerx, button.rect.centery))
    button.update_hover()
    assert button.hover is True

    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (button.rect.right + 20, button.rect.bottom + 20))
    button.update_hover()
    assert button.hover is False


def test_button_draw_fills_button_area_with_background_color(monkeypatch, small_screen, font):
    button = make_button(small_screen, font)
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (button.rect.right + 20, button.rect.bottom + 20))
    button.draw()

    interior_pixel = button.screen.get_at(
        (button.rect.x + 6, button.rect.y + 6)
    )
    assert interior_pixel[:3] == button.bg_color
    assert button.hover is False


def test_button_draw_updates_hover_when_pointer_is_inside(monkeypatch, small_screen, font):
    button = make_button(small_screen, font)

    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: button.rect.center)
    button.draw()

    assert button.hover is True
