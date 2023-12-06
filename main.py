import pygame
from rendering.screens import Screens
import rendering.globals_vars as var
from rendering.game import Game
from rendering.utility.util import Util

pygame.init()
pygame.display.set_caption("OG Racer")
run = True

Screens.init_music()
Screens.create_login_input()
Screens.create_register_input()
Screens.create_music_slider()


while run:
    tick = var.clock.tick(var.fps)

    Screens.screen_update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        if var.menu_state == "log_menu":
            var.manager_Login.process_events(event)

        if var.menu_state == "registration_menu":
            var.manager_register.process_events(event)

        if var.menu_state == "option_menu":
            var.manager_option.process_events(event)

    if var.buttons["Einzelspieler"]:
        Game()

    elif var.buttons["Mehrspieler"]:
        var.menu_state = "multiplayer_menu"

    elif var.buttons["Optionen"]:
        var.menu_state = "option_menu"

    elif var.buttons["Zurueck"]:
        var.menu_state = "main_menu"

    elif var.buttons["Jetzt Anmelden"]:
        var.menu_state = "log_menu"

    elif var.buttons["Anmelden"]:
        var.client.send_login_data(var.login_name.get_text(), var.login_password.get_text())
        while not var.client.logincomplete:
            pass
        var.menu_state = "lobby_option"

    elif var.buttons["Schnelles Spiel"] or var.buttons["Lobby erstellen"]:
        var.menu_state = "ingame_lobby"

    elif var.buttons["Jetzt Registrieren"]:
        var.menu_state = "registration_menu"

    elif var.buttons["Abmelden"]:
        var.menu_state = "main_menu"

    elif var.menu_state == "option_menu":
        var.manager_option.update(tick)

    elif var.menu_state == "registration_menu":
        var.manager_register.update(tick)

    elif var.menu_state == "log_menu":
        var.manager_Login.update(tick)

    Util.reset_buttons()
    pygame.display.update()



pygame.quit()
