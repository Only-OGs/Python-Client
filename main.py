import threading
import pygame
import globals_vars as global_var
import menu.menu_vars as menu_var
import rendering.game_vars as game_var
from menu.button import Button
from menu.screens import Screens
from menu.components import Components
from rendering.game import Game
from menu.sounds import sounds

# Initialisert die Musik und die Eingabefelder
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

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        # Je nach aktuellem Menüzustand werden die Ereignisse an die entsprechenden Manager weitergeleitet
        if global_var.menu_state == "log_menu":
            menu_var.manager_Login.process_events(event)

        if global_var.menu_state == "registration_menu":
            menu_var.manager_register.process_events(event)

        if global_var.menu_state == "option_menu":
            menu_var.manager_option.process_events(event)

        if global_var.menu_state == "search_for_lobby":
            menu_var.manager_lobby_search.process_events(event)

        if global_var.menu_state =="ingame_lobby":
            menu_var.manager_chat.process_events(event)

    tick = global_var.clock.tick(global_var.fps)
    Components.do_after_await()

    # Aktualisiert den Bildschirm basierend auf dem aktuellen Menüzustand
    Screens.screen_update()

    # Überprüft, ob ein Spiel gestartet werden soll (Singleplayer oder Multiplayer)
    if game_var.track is not None and global_var.singleplayer is not True:
        if not menu_var.is_running:
            global_var.menu_state = "loading"
            thread = threading.Thread(target=Components.start_timer_in_thread, args=(1, "game"))
            thread.start()
        if global_var.isgame:
            Game()
            global_var.isgame = False

    # Startet das Einzelspieler-Spiel, wenn der entsprechende Button gedrückt wurde
    if menu_var.buttons["Einzelspieler"]:
        Game()
    # Ändert den Menüzustand basierend auf den gedrückten Buttons
    elif menu_var.buttons["Mehrspieler"]:
        global_var.menu_state = "multiplayer_menu"

    elif menu_var.buttons["Optionen"]:
        global_var.menu_state = "option_menu"

    elif menu_var.buttons["Zurueck"]:
        global_var.singleplayer_start = False
        global_var.menu_state = "main_menu"


    elif menu_var.buttons["Jetzt Anmelden"]:
        Components.clear_input("loginname")
        Components.clear_input("loginpw")
        global_var.menu_state = "log_menu"


    elif menu_var.buttons["Anmelden"]: # Sendet die Anmeldedaten an den Server
        global_var.client.send_login_data(menu_var.login_name.get_text(), menu_var.login_password.get_text())
        menu_var.is_await = True
        Components.clear_input("loginname")
        Components.clear_input("loginpw")


    elif menu_var.buttons["Schnelles Spiel"] or menu_var.buttons["Lobby erstellen"]:
        if menu_var.buttons["Schnelles Spiel"]:
            global_var.client.get_lobby() # Sucht die nächte offene Lobby
            menu_var.is_await = True
        elif menu_var.buttons["Lobby erstellen"]:
            global_var.client.create_lobby() # Erstellt eigene Lobby
            global_var.id_playerList.append(global_var.client.playersname)
            menu_var.is_await = True

    elif menu_var.buttons["Verlassen"]:
        global_var.client.leave_lobby() #Verlässt die Lobby
        global_var.client.chat_message.clear()
        global_var.client.chat_player.clear()
        global_var.menu_state = "lobby_option"
        Components.clear_input("chat")


    elif menu_var.buttons["Bereit"]:
        global_var.client.notReady()
        menu_var.is_await = True

    elif menu_var.buttons["Nicht Bereit"]:
        global_var.client.ready()
        menu_var.is_await = True

    elif menu_var.buttons["Senden"]:
        global_var.client.newMessage(menu_var.chat_massage.get_text())
        Components.clear_input("chat")

    elif menu_var.buttons["Lobby suchen"]:
        global_var.menu_state = "search_for_lobby"  # Führt zum "Suche Lobby"-Bildschirm

    elif menu_var.buttons["Suchen"]:
        global_var.client.join_lobby(menu_var.lobby_search_input.get_text())
        menu_var.is_await = True
        Components.clear_input("search")


    elif menu_var.buttons["Jetzt Registrieren"]:
        Components.clear_input("registerpw")
        Components.clear_input("registername")
        global_var.menu_state = "registration_menu"

    elif menu_var.buttons["Registrieren"]:
        global_var.client.send_register_data(menu_var.register_name.get_text(), menu_var.register_password.get_text())
        menu_var.is_await = True
        Components.clear_input("registerpw")
        Components.clear_input("registername")

    elif menu_var.buttons["Abmelden"]:
        global_var.menu_state = "main_menu"
        global_var.singleplayer_start = False

    elif global_var.menu_state == "option_menu":
        menu_var.manager_option.update(tick)

    elif global_var.menu_state == "search_for_lobby":
        menu_var.manager_lobby_search.update(tick)

    elif global_var.menu_state == "registration_menu":
        menu_var.manager_register.update(tick)

    elif global_var.menu_state == "log_menu":
        menu_var.manager_Login.update(tick)

    elif global_var.menu_state == "ingame_lobby":
        menu_var.manager_chat.update(tick)


    Button.reset_buttons()
    pygame.display.update()

pygame.quit()
