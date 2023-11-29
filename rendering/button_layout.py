from rendering.button import Button
from globals import globals


left_buttonx = globals.screen_width / 2 - globals.screen_width / 3
left_buttony = globals.screen_height / 2

middle_buttonx = globals.screen_width / 2
middle_buttony = globals.screen_height / 2 + 50

right_buttonx = globals.screen_width / 2 + globals.screen_width / 3
right_buttony = globals.screen_height / 2

button_image = 'assets/button.png'
button_image_hover = 'assets/button-pressed.png'
button_size = 2
font_size = 20


def linker_button(screen, text):
    button_links = Button(x=left_buttonx, y=left_buttony, image=button_image, size=button_size,
                          hover=button_image_hover)
    button = button_links.draw(screen)
    button_links.text(screen=screen, text=text, size=font_size, color=globals.WHITE)
    if button:
        return True
def mittlerer_button(screen, text):
    button_mittel = Button(x=middle_buttonx, y=middle_buttony, image=button_image, size=button_size,
                          hover=button_image_hover)
    button = button_mittel.draw(screen)
    button_mittel.text(screen=screen, text=text, size=font_size, color=globals.WHITE)
    if button:
        return True

def rechter_button(screen, text):
    button_rechts = Button(x=right_buttonx, y=right_buttony, image=button_image, size=button_size,
                          hover=button_image_hover)
    button = button_rechts.draw(screen)
    button_rechts.text(screen=screen, text=text, size=font_size, color=globals.WHITE)
    if button:
        return True
def log_reg_button(screen, text):
    log_button = Button(x=globals.screen_width -400, y=(globals.screen_height // 2 + 150), image=button_image, size=button_size,
                               hover=button_image_hover)
    button = log_button.draw(screen)
    log_button.text(screen=screen, text=text, size=font_size, color=globals.WHITE)
    if button:
        return True
