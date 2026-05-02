import os
import sys

import pygame

from pygets.core.theme import themes
from pygets.utils.colors import colors
from pygets.widgets import Button, Checkbox, Combobox, Popup, Slider, Textbox, Togglebutton


pygame.init()
pygame.key.set_repeat(300, 40)

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Example All Widgets")

theme = themes["dark"]

BASE_DIR = os.path.dirname(__file__)
font_path = os.path.join(BASE_DIR, "assets", "fonts", "Inter.ttf")
image_path = os.path.join(BASE_DIR, "assets", "images", "star.png")

try:
    font = pygame.font.Font(font_path, 22)
    small_font = pygame.font.Font(font_path, 18)
    title_font = pygame.font.Font(font_path, 34)
    popup_title_font = pygame.font.Font(font_path, 28)
    title_font.set_bold(True)
    popup_title_font.set_bold(True)
except FileNotFoundError:
    font = pygame.font.Font(None, 22)
    small_font = pygame.font.Font(None, 18)
    title_font = pygame.font.Font(None, 34)
    popup_title_font = pygame.font.Font(None, 28)

try:
    image = pygame.image.load(image_path).convert_alpha()
except FileNotFoundError:
    print(f"Image not found at {image_path}!")
    image = pygame.Surface((28, 28), pygame.SRCALPHA)
    pygame.draw.polygon(image, colors["GOLD"], [(14, 0), (18, 10), (28, 10), (20, 17), (23, 28), (14, 21), (5, 28), (8, 17), (0, 10), (10, 10)])


def submit_profile():
    # Build the popup content from the current widget state.
    newsletter_status = "Yes" if newsletter_checkbox.checked else "No"
    notifications_status = "Enabled" if notifications_toggle.active else "Disabled"
    experience_value = int(experience_slider.value)

    popup.title = f"Profile ready for {name_input.textbox_content or 'new user'}"
    popup.message = (
        f"Favorite language: {language_combo.value}. "
        f"Experience level: {experience_value}/100. "
        f"Receive newsletter: {newsletter_status}. "
        f"Notifications: {notifications_status}."
    )
    popup.visible = True


name_input = Textbox(
    x=70,
    y=170,
    width=360,
    screen=screen,
    theme=theme,
    font=font,
    function=submit_profile,
    placeholder="Write your name...",
)

# The widgets below form a single settings flow instead of unrelated samples.
language_combo = Combobox(
    x=70,
    y=270,
    width=280,
    height=38,
    screen=screen,
    theme=theme,
    options=["Python", "JavaScript", "Rust", "Go", "C++", "Java"],
    font=font,
    border_radius=10,
)

experience_slider = Slider(
    x=70,
    y=390,
    width=320,
    height=10,
    screen=screen,
    theme=theme,
    min_val=0,
    max_val=100,
    initial_value=65,
)

newsletter_checkbox = Checkbox(
    x=70,
    y=500,
    size=25,
    screen=screen,
    theme=theme,
    checked=True,
    border_radius=5,
)

notifications_toggle = Togglebutton(
    x=70,
    y=560,
    width=70,
    height=34,
    screen=screen,
    theme=theme,
    active=True,
)

save_button = Button(
    x=600,
    y=540,
    width=200,
    height=50,
    theme=theme,
    font=font,
    screen=screen,
    image=image,
    text="Save profile",
)

popup = Popup(
    width=560,
    height=230,
    screen=screen,
    theme=themes["silver"],
    font=font,
    title_font=popup_title_font,
    screen_width=SCREEN_WIDTH,
    screen_height=SCREEN_HEIGHT,
    title="Profile ready",
    message="Your preferences were saved.",
)
popup.visible = False


clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    mouse_down = False
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_down = True
            if save_button.rect.collidepoint(event.pos) and not popup.visible:
                submit_profile()

        # Freeze form interaction while the popup is visible.
        if not popup.visible:
            name_input.handle_event(event)
            language_combo.handle_event(event)
            experience_slider.handle_event(event)
        popup.handle_event(event)

    # Checkbox and toggle use per-frame updates instead of event handlers.
    if not popup.visible:
        name_input.update()
        newsletter_checkbox.update(mouse_down, mouse_pos)
        notifications_toggle.update(mouse_down, mouse_pos)
    popup.update()

    screen.fill(colors["BLUISH_GRAY"])

    title = title_font.render("Developer Profile Setup", True, theme.text)

    screen.blit(title, (70, 30))

    left_panel = pygame.Rect(40, 115, 420, 510)
    right_panel = pygame.Rect(500, 115, 400, 510)
    pygame.draw.rect(screen, theme.background, left_panel, border_radius=18)
    pygame.draw.rect(screen, theme.foreground, left_panel, width=2, border_radius=18)
    pygame.draw.rect(screen, theme.background, right_panel, border_radius=18)
    pygame.draw.rect(screen, theme.foreground, right_panel, width=2, border_radius=18)

    screen.blit(font.render("Name", True, theme.text), (70, 140))
    name_input.draw()


    experience_value = int(experience_slider.value)
    experience_label = font.render(
        f"Experience level: {experience_value}/100",
        True,
        theme.text,
    )
    screen.blit(experience_label, (70, 350))
    experience_slider.draw()

    newsletter_checkbox.draw()
    newsletter_text = font.render("Subscribe to the newsletter", True, theme.text)
    screen.blit(newsletter_text, (110, 500))

    notifications_toggle.draw()
    notifications_text = font.render("Enable product notifications", True, theme.text)
    screen.blit(notifications_text, (155, 564))

    screen.blit(font.render("Favorite language", True, theme.text), (70, 240))
    language_combo.draw()

    # Mirror the current state so the user can test every widget at a glance.
    preview_title = title_font.render("Live preview", True, theme.text)
    preview_name = small_font.render(
        f"Name: {name_input.textbox_content or 'Pending input'}",
        True,
        theme.text,
    )
    preview_language = small_font.render(
        f"Language: {language_combo.value}",
        True,
        theme.text,
    )
    preview_newsletter = small_font.render(
        f"Newsletter: {'Subscribed' if newsletter_checkbox.checked else 'Not subscribed'}",
        True,
        theme.text,
    )
    preview_notifications = small_font.render(
        f"Notifications: {'On' if notifications_toggle.active else 'Off'}",
        True,
        theme.text,
    )
    preview_note = small_font.render(
        "Click the button to see the summary.",
        True,
        theme.text,
    )

    screen.blit(preview_title, (595, 130))
    screen.blit(preview_name, (530, 200))
    screen.blit(preview_language, (530, 240))
    screen.blit(preview_newsletter, (530, 280))
    screen.blit(preview_notifications, (530, 320))
    screen.blit(preview_note, (530, 420))

    save_button.draw()
    popup.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
