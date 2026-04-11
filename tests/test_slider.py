import pygame

from pygets.widgets.slider import Slider
from pygets.core.theme import themes


def make_slider(screen, **kwargs):
    return Slider(
        x=10,
        y=10,
        width=120,
        height=20,
        screen=screen,
        min_val=0,
        max_val=100,
        initial_value=50,
        theme=themes["ocean"],
        **kwargs,
    )


def test_slider_initialization(small_screen):
    slider = make_slider(small_screen)

    assert slider.min_val == 0
    assert slider.max_val == 100
    assert slider.value == 50
    assert slider.dragging is False
    assert slider.handle_rect.width == slider.handle_width
    assert slider.handle_rect.height == slider.handle_height
    assert slider.rect.topleft == (10, 10)
    assert slider.theme == themes["ocean"]


def test_slider_handle_event_click_on_handle_starts_dragging_and_releases(small_screen):
    slider = make_slider(small_screen)

    click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=slider.handle_rect.center)
    slider.handle_event(click_event)

    assert slider.dragging is True

    motion_event = pygame.event.Event(pygame.MOUSEMOTION, pos=(75, slider.handle_rect.centery))
    slider.handle_event(motion_event)

    assert slider.value > 50
    assert slider.handle_rect.centerx == 75

    release_event = pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(75, slider.handle_rect.centery))
    slider.handle_event(release_event)

    assert slider.dragging is False


def test_slider_handle_event_click_on_bar_moves_handle_and_updates_value(small_screen):
    slider = make_slider(small_screen)

    click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(slider.rect.x + 25, slider.rect.centery))
    slider.handle_event(click_event)

    assert slider.dragging is True
    assert slider.value < 50
    assert slider.handle_rect.centerx == slider.rect.x + 25


def test_slider_handle_event_drag_keeps_value_within_bounds(small_screen):
    slider = make_slider(small_screen)
    start_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=slider.handle_rect.center)
    slider.handle_event(start_click)

    motion_event = pygame.event.Event(pygame.MOUSEMOTION, pos=(slider.rect.right + 50, slider.handle_rect.centery))
    slider.handle_event(motion_event)

    assert slider.value == slider.max_val
    assert slider.handle_rect.right == slider.rect.right

    slider.handle_event(pygame.event.Event(pygame.MOUSEBUTTONUP, button=1))
    assert slider.dragging is False


def test_slider_draw_renders_handle_and_bar(small_screen):
    slider = make_slider(small_screen)

    slider.draw()
    handle_pixel = slider.screen.get_at(slider.handle_rect.center)
    assert handle_pixel[:3] == slider.color_handle

    bar_pixel = slider.screen.get_at(
        ((slider.handle_rect.right + slider.rect.right) // 2, slider.rect.centery)
    )
    assert bar_pixel[:3] == slider.color_bar
