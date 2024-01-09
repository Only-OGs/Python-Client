import threading
import pygame
from menu.screens import Screens
import rendering.globals_vars as var
from rendering.game import Game
from rendering.utility.util import Util
from menu.sounds import sounds

pygame.init()
sounds.init_music()
pygame.display.set_caption("OG Racer")
run = True
Screens.create_login_input()
Screens.create_message_output()
Screens.create_register_input()
Screens.create_music_slider()
Screens.create_lobby_search_input()
gameload = False


def lost_connection():
    if not var.client.sio.connected:
        var.menu_state = "main_menu"

while run:
    tick = var.clock.tick(var.fps)
    Util.do_after_await()
    Screens.screen_update()
    lost_connection()
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

        if var.menu_state == "search_for_lobby":
            var.manager_lobby_search.process_events(event)

        if var.menu_state =="ingame_lobby":
            var.manager_chat.process_events(event)

    #Spielt und Pausiert die Musik
    if var.play_music:
        sounds.start_music()
    else:
        sounds.pause_music()

    if var.track is not None and var.singleplayer is not True:
        if not var.is_running:
            var.menu_state = "loading"
            thread = threading.Thread(target=Screens.threaded_function, args=(1, "game"))
            thread.start()
        if var.isgame:
            Game()
            var.isgame = False

    if var.buttons["Einzelspieler"]:
        Game()

    elif var.buttons["Mehrspieler"]:
        var.menu_state = "multiplayer_menu"

    elif var.buttons["Optionen"]:
        var.menu_state = "option_menu"

    elif var.buttons["Zurueck"]:
        var.singleplayer_start = False
        print("  var.singleplayer_start = False in main Zurückbutton: "+ str(var.singleplayer_start))
        var.menu_state = "main_menu"


    elif var.buttons["Jetzt Anmelden"]:
        Util.clear_input("loginname")
        Util.clear_input("loginpw")
        var.menu_state = "log_menu"


    elif var.buttons["Anmelden"]:
        var.client.send_login_data(var.login_name.get_text(), var.login_password.get_text())
        var.is_await = True
        Util.clear_input("loginname")
        Util.clear_input("loginpw")


    elif var.buttons["Schnelles Spiel"] or var.buttons["Lobby erstellen"]:
        if var.buttons["Schnelles Spiel"]:
            var.client.get_lobby()
            var.is_await = True
        elif var.buttons["Lobby erstellen"]:
            var.client.create_lobby()
            var.id_playerList.append(var.client.playersname)
            var.is_await = True

    elif var.buttons["Verlassen"]:
        var.client.leave_lobby()
        var.client.chat_message.clear()
        var.client.chat_player.clear()
        var.menu_state = "lobby_option"
        var.singleplayer_start = False
        print("  var.singleplayer_start = False in main Verlassen: " + str(var.singleplayer_start))
        Util.clear_input("chat")




    elif var.buttons["Bereit"]:
        var.client.notReady()
        var.is_await = True

    elif var.buttons["Nicht Bereit"]:
        var.client.ready()
        var.is_await = True

    elif var.buttons["Senden"]:
        var.client.newMessage(var.chat_massage.get_text())
        Util.clear_input("chat")

    elif var.buttons["Lobby suchen"]:
        var.menu_state = "search_for_lobby"

    elif var.buttons["Suchen"]:
        var.client.join_lobby(var.lobby_search_input.get_text())
        var.is_await = True
        Util.clear_input("search")


    elif var.buttons["Jetzt Registrieren"]:
        Util.clear_input("registerpw")
        Util.clear_input("registername")
        var.menu_state = "registration_menu"

    elif var.buttons["Registrieren"]:
        var.client.send_register_data(var.register_name.get_text(), var.register_password.get_text())
        var.is_await = True
        Util.clear_input("registerpw")
        Util.clear_input("registername")

    elif var.buttons["Abmelden"]:
        var.menu_state = "main_menu"
        var.singleplayer_start = False
        print("  var.singleplayer_start = False in main Abmelden: " + str(var.singleplayer_start))

    elif var.menu_state == "option_menu":
        var.manager_option.update(tick)

    elif var.menu_state == "search_for_lobby":
        var.manager_lobby_search.update(tick)

    elif var.menu_state == "registration_menu":
        var.manager_register.update(tick)

    elif var.menu_state == "log_menu":
        var.manager_Login.update(tick)

    elif var.menu_state == "ingame_lobby":
        var.manager_chat.update(tick)


    Util.reset_buttons()
    pygame.display.update()

pygame.quit()
