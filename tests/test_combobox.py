import pygame

from pygets.widgets.combobox import Combobox
from pygets.core.theme import themes

def make_combobox(screen, font, **kwargs):
    params = {
        "options": ["Option 1", "Option 2", "Option 3"],
        **kwargs,
    }
    return Combobox(
        x=0,
        y=0,
        width=100,
        height=30,
        screen=screen,
        font=font,
        theme=themes["forest"],
        **params,
    )


def test_combobox_initialization(small_screen, font):
    combobox = make_combobox(small_screen, font)

    assert combobox.options == ["Option 1", "Option 2", "Option 3"]
    assert combobox.selected_index == 0
    assert combobox.value == "Option 1"
    assert combobox.open is False
    assert combobox.hover_option == -1
    assert combobox.rect.topleft == (0, 0)
    assert combobox.rect.size == (100, 30)
    assert combobox.bg_color == themes["forest"].background
    assert combobox.edge_color == themes["forest"].foreground
    assert combobox.text_color == themes["forest"].text


def test_combobox_toggle_open_state_on_main_box_click(small_screen, font):
    combobox = make_combobox(small_screen, font, options=["Option 1", "Option 2"])
    click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=combobox.rect.center)

    combobox.handle_event(click_event)
    assert combobox.open is True

    combobox.handle_event(click_event)
    assert combobox.open is False


def test_combobox_selects_option_and_closes_when_open(small_screen, font):
    combobox = make_combobox(small_screen, font, options=["Option 1", "Option 2"])
    combobox.open = True

    second_option_center = (
        combobox.rect.centerx,
        combobox.rect.bottom + combobox.height_option + combobox.height_option // 2,
    )
    select_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=second_option_center)

    combobox.handle_event(select_event)
    assert combobox.selected_index == 1
    assert combobox.value == "Option 2"
    assert combobox.open is False


def test_combobox_closes_when_click_outside_open_options(small_screen, font):
    combobox = make_combobox(small_screen, font, options=["Option 1", "Option 2"])
    combobox.open = True
    outside_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=(combobox.rect.right + 20, combobox.rect.bottom + 20),
    )

    combobox.handle_event(outside_event)
    assert combobox.open is False
    assert combobox.selected_index == 0


def test_combobox_update_hover_sets_main_hover(monkeypatch, small_screen, font):
    combobox = make_combobox(small_screen, font, options=["Option 1", "Option 2"])

    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: combobox.rect.center)
    combobox.update_hover()

    assert combobox.hover is True
    assert combobox.hover_option == -1


def test_combobox_update_hover_sets_hover_option(monkeypatch, small_screen, font):
    combobox = make_combobox(small_screen, font, options=["Option 1", "Option 2"])
    combobox.open = True
    point_over_second_option = (
        combobox.rect.centerx,
        combobox.rect.bottom + combobox.height_option + combobox.height_option // 2,
    )

    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: point_over_second_option)
    combobox.update_hover()

    assert combobox.hover is False
    assert combobox.hover_option == 1


def test_combobox_draw_renders_main_box(monkeypatch, small_screen, font):
    combobox = make_combobox(small_screen, font, options=["Option 1", "Option 2"])
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (combobox.rect.right + 20, combobox.rect.bottom + 20))

    combobox.draw()
    pixel = combobox.screen.get_at((combobox.rect.right - 25, combobox.rect.y + 4))
    assert pixel[:3] == combobox.bg_color
