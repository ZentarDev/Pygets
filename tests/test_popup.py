import pygame

from pygets.widgets.popup import Popup
from pygets.core.theme import themes

def make_popup(screen, font, title_font, **kwargs):
    params = {
        "message": "Hello world",
        **kwargs,
    }
    return Popup(
        title="Test Popup",
        font=font,
        title_font=title_font,
        screen_width=800,
        screen_height=600,
        width=300,
        height=150,
        screen=screen,
        theme=themes["light"],
        **params,
    )


def test_popup_initial_state(large_screen, font, title_font):
    popup = make_popup(large_screen, font, title_font)

    assert popup.visible is True
    assert popup.title == "Test Popup"
    assert popup.message == "Hello world"
    assert popup.rect.width == 300
    assert popup.rect.height == 150
    assert popup.rect.center == (400, 300)


def test_popup_update_keeps_close_button_attached_to_top_right(large_screen, font, title_font):
    popup = make_popup(large_screen, font, title_font)
    popup.update()

    expected_left = popup.rect.right - popup.close_button.rect.width - 5
    expected_top = popup.rect.top + 5

    assert popup.close_button.rect.topleft == (expected_left, expected_top)


def test_popup_draw_renders_background(large_screen, font, title_font):
    popup = make_popup(large_screen, font, title_font)
    popup.update()
    popup.draw()

    title_bar_height = popup.title_font.get_height() + 15

    x = popup.rect.x + 5
    y = popup.rect.y + title_bar_height + 5

    pixel = popup.screen.get_at((x, y))
    assert pixel[:3] == popup.background_color


def test_popup_close_button_hides_popup(large_screen, font, title_font):
    popup = make_popup(large_screen, font, title_font)
    popup.update()
    click_pos = popup.close_button.rect.center

    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        {"pos": click_pos, "button": 1}
    )

    popup.handle_event(event)

    assert popup.visible is False


def test_popup_hidden_state_prevents_drawing(large_screen, font, title_font):
    popup = make_popup(large_screen, font, title_font)
    popup.visible = False
    popup.screen.fill((123, 123, 123))

    popup.draw()

    pixel = popup.screen.get_at((10, 10))
    assert pixel[:3] == (123, 123, 123)


def test_popup_wrap_text_creates_multiple_lines(large_screen, font, title_font):
    long_text = "This is a very long text that should wrap into multiple lines properly inside the popup"
    popup = make_popup(large_screen, font, title_font, message=long_text)

    lines = popup._wrap_text(
        long_text,
        popup.font,
        max_width=150,
        max_height=100
    )

    assert len(lines) > 1


def test_popup_wrap_text_adds_ellipsis_when_overflow(large_screen, font, title_font):
    very_long_text = " ".join(["word"] * 100)
    popup = make_popup(large_screen, font, title_font, message=very_long_text)

    lines = popup._wrap_text(
        very_long_text,
        popup.font,
        max_width=150,
        max_height=40
    )

    assert lines[-1].endswith("...")
