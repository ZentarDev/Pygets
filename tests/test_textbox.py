import pygame
import pytest

from pygets.widgets.textbox import Textbox
from pygets.core.theme import themes

def make_textbox(screen, font, **kwargs):
    return Textbox(
        x=10,
        y=10,
        screen=screen,
        font=font,
        theme=themes["sunset"],
        **kwargs,
    )


def test_textbox_initialization(medium_screen, font):
    textbox = make_textbox(medium_screen, font, placeholder="Enter text...", width=300, max_characters=50)

    assert textbox.textbox_content == ""
    assert textbox.active is False
    assert textbox.cursor_position == 0
    assert textbox.placeholder == "Enter text..."
    assert textbox.max_characters == 50
    assert textbox.rect.width == 300
    assert textbox.rect.height >= font.get_height() + 10
    assert textbox.bg_color == themes["sunset"].background
    assert textbox.text_color == themes["sunset"].text
    assert textbox.placeholder_color == themes["sunset"].idle


def test_textbox_mouse_click_activation_and_deactivation(medium_screen, font):
    textbox = make_textbox(medium_screen, font)

    inside_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(textbox.rect.x + 5, textbox.rect.y + 5))
    textbox.handle_event(inside_event)
    assert textbox.active is True
    assert textbox.cursor_visible is True

    outside_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(textbox.rect.right + 20, textbox.rect.bottom + 20))
    textbox.handle_event(outside_event)
    assert textbox.active is False


def test_textbox_typing_respects_max_characters(medium_screen, font):
    textbox = make_textbox(medium_screen, font, max_characters=3)
    textbox.active = True

    for char in "abcd":
        event = pygame.event.Event(pygame.KEYDOWN, unicode=char, key=ord(char), mod=0)
        textbox.handle_event(event)

    assert textbox.textbox_content == "abc"
    assert textbox.cursor_position == 3


@pytest.mark.parametrize(
    ("keys", "expected_text", "expected_position"),
    [
        (["a", "b", "c"], "abc", 3),
        (["1", "2"], "12", 2),
        (["x", "y", "z"], "xyz", 3),
    ],
)
def test_textbox_typing_inserts_characters_and_updates_cursor(medium_screen, font, keys, expected_text, expected_position):
    textbox = make_textbox(medium_screen, font)
    textbox.active = True

    for char in keys:
        event = pygame.event.Event(pygame.KEYDOWN, unicode=char, key=ord(char), mod=0)
        textbox.handle_event(event)

    assert textbox.textbox_content == expected_text
    assert textbox.cursor_position == expected_position


def test_textbox_backspace_delete_and_cursor_navigation(medium_screen, font):
    textbox = make_textbox(medium_screen, font)
    textbox.active = True
    textbox.textbox_content = "abcd"
    textbox.cursor_position = 4

    backspace_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, mod=0)
    textbox.handle_event(backspace_event)
    assert textbox.textbox_content == "abc"
    assert textbox.cursor_position == 3

    left_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, mod=0)
    textbox.handle_event(left_event)
    assert textbox.cursor_position == 2

    delete_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DELETE, mod=0)
    textbox.handle_event(delete_event)
    assert textbox.textbox_content == "ab"
    assert textbox.cursor_position == 2

    right_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, mod=0)
    textbox.handle_event(right_event)
    assert textbox.cursor_position == 2

    home_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_HOME, mod=0)
    textbox.handle_event(home_event)
    assert textbox.cursor_position == 0

    end_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_END, mod=0)
    textbox.handle_event(end_event)
    assert textbox.cursor_position == len(textbox.textbox_content)


def test_textbox_ctrl_v_pastes_text(monkeypatch, medium_screen, font):
    textbox = make_textbox(medium_screen, font, max_characters=20)
    textbox.active = True

    monkeypatch.setattr(pygame.key, "get_mods", lambda: pygame.KMOD_CTRL)
    monkeypatch.setattr("pygets.widgets.textbox.pyperclip.paste", lambda: "hello")

    paste_event = pygame.event.Event(
        pygame.KEYDOWN,
        key=pygame.K_v,
        unicode="v",
        mod=pygame.KMOD_CTRL,
    )
    textbox.handle_event(paste_event)

    assert textbox.textbox_content == "hello"
    assert textbox.cursor_position == 5


def test_textbox_enter_key_deactivates_and_calls_function(medium_screen, font):
    called = {"count": 0}

    def submit():
        called["count"] += 1

    textbox = make_textbox(medium_screen, font, function=submit)
    textbox.active = True
    textbox.textbox_content = "hello"
    textbox.cursor_position = 5

    enter_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0)
    textbox.handle_event(enter_event)

    assert textbox.active is False
    assert called["count"] == 1


def test_textbox_update_toggles_cursor_visibility(monkeypatch, medium_screen, font):
    textbox = make_textbox(medium_screen, font)
    textbox.active = True
    textbox.cursor_visible = True
    textbox.blink_time = 100

    monkeypatch.setattr(pygame.time, "get_ticks", lambda: 700)
    textbox.update()

    assert textbox.cursor_visible is False
    assert textbox.blink_time == 700


def test_textbox_draw_preserves_content(monkeypatch, medium_screen, font):
    textbox = make_textbox(medium_screen, font)
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (textbox.rect.right + 20, textbox.rect.bottom + 20))
    textbox.draw()

    textbox.active = True
    textbox.textbox_content = "Test text"
    textbox.cursor_position = len(textbox.textbox_content)
    textbox.draw()
    assert textbox.hover in (True, False)
    assert textbox.textbox_content == "Test text"
