import socketio
import globals_vars as global_var
import rendering.game_vars as game_var

from rendering.utility.car_ai import Cars
from rendering.utility.sprite_generator import SpriteGen

'''Die SocketIOClient-Klasse dient als Schnittstelle für die Kommunikation zwischen dem Client und dem Server über 
Socket.IO. '''


class SocketIOClient:
    def __init__(self):
        # Serverurl
        self.server_url = "http://89.58.1.158:8080"
        # Client mit aktivem Logging
        self.sio = socketio.Client(logger=False, engineio_logger=False)

        # reagiert auf die das angeg. Event
        self.sio.on('connection_success', self.on_connection_success)
        self.sio.on('search_lobby', self.on_search_lobby)
        self.sio.on('new_message', self.on_newMessage)
        self.sio.on('lobby_created', self.on_lobbycreated)
        self.sio.on('register', self.on_register)
        self.sio.on('lobby_management', self.on_playerJoined)
        self.sio.on('logout', self.on_logout)
        self.sio.on('login', self.on_login)
        self.sio.on('get_lobby', self.on_get_lobby)
        self.sio.on('player_leave', self.on_playerLeave)
        self.sio.on('timer_countdown', self.on_timer)
        self.sio.on('timer_abrupt', self.on_timer_off)
        self.sio.on('load_level', self.on_load_level)
        self.sio.on('load_assets', self.on_load_assets)
        self.sio.on('wait_for_start', self.on_wait_for_start)
        self.sio.on('updated_positions', self.on_updated_positions)
        self.sio.on('start_race', self.on_start_race)
        self.sio.on('start_race_timer', self.on_start_race_timer)
        self.sio.on('get_leaderboard', self.on_get_leaderboard)

        # Initialisierung von Variablen für Erfolg/Misserfolg bei Aktionen
        self.logoutstatus = None
        self.loginstatus = None
        self.loginmessage = None
        self.logincomplete = False
        self.registerstatus = None
        self.registercomplete = False
        self.lobbystatus = None
        self.lobbymessage = None
        self.timer = ""
        self.lobbycreated = False
        self.lobbyleaft = False
        self.lobbyJoined = False
        self.searchlobbyJoined = False
        self.quickLobbyJoined = False
        self.lobbyplayer = None
        self.lobbyid = None
        self.playersname = None
        self.chat_player = []
        self.chat_message = []
        self.errormessage = ""
        self.is_ready = False
        self.olddata = 0
        self.leaderboard = []
        self.new_car_data = []

    '''aktualisiert das Leaderboard, wenn Daten empfangen werden.'''
    def on_get_leaderboard(self, data):
        if self.sio.connected:
            if data != '':
                self.leaderboard = data
                global_var.game_end = True

    '''wenn ein Spieler die Lobby verlässt.'''
    def on_playerLeave(self, data):
        if self.sio.connected:
            if data.get('status') == 'left':
                self.lobbyleaft = True

    '''setzt die Variable mit den erhaltenen Strecke.'''
    def on_load_level(self, data):
        if self.sio.connected:
            if data != '':
                global_var.singleplayer = False
                game_var.track = data

    '''setzt die Variable mit den erhaltenen Bildern.'''
    def on_load_assets(self, data):
        if self.sio.connected:
            if data != '':
                global_var.assets = data

    '''eine Lobby wird über schnelle Spiel gefunden'''
    def on_get_lobby(self, data):
        if self.sio.connected:
            self.lobbymessage = data.get("message")
            self.lobbystatus = data.get("status")
            if self.lobbystatus == 'success':
                self.quickLobbyJoined = True
    '''Wenn die Lobby erfolgreich erstellt wurde, wird die LobbyID gespeichert.'''
    def on_lobbycreated(self, data):
        if self.sio.connected:
            if data.get('status') == 'lobby_created':
                self.lobbycreated = True
                message = data.get('message')
                self.lobbyid = message

    def on_connection_success(self, data):
        pass

    '''verarbeitet eingehende Chatnachrichten.'''
    def on_newMessage(self, data):
        if self.sio.connected:
            if isinstance(data, str):
                try:
                    user, message = data.split(';')
                    self.chat_player.append(user)
                    self.chat_message.append(message)
                except ValueError:
                    raise Exception("Fehler beim Aufteilen")
            else:
                print("Übergebene Daten sind kein String")

    '''Ein Lobby wurde gefunden'''
    def on_search_lobby(self, data):
        if self.sio.connected:
            self.lobbystatus = data.get("status")
            self.lobbymessage = data.get("message")
            self.lobbyid = data.get("lobby")
            if self.lobbystatus == 'success':
                self.searchlobbyJoined = True

    def on_logout(self, data):
        if self.sio.connected:
            message = data.get('message')
            self.logoutstatus = message

    '''Wenn eine Spierler der Lobby betritt'''
    def on_playerJoined(self, data):
        if self.sio.connected:
            self.lobbystatus = data.get("status")
            if self.lobbystatus == 'joined':
                self.lobbyJoined = True
            self.lobbyid = data.get("lobby")
            global_var.id_playerList = data.get("players").split(';')

    '''Statusmeldung für das Einloggen '''
    def on_login(self, data):
        if self.sio.connected:
            message = data.get('message')
            self.loginmessage = message
            if data.get('status') == "login_success":
                self.logincomplete = True
            else:
                self.playersname = ''

    '''Statusmeldung für die Registrierung'''
    def on_register(self, data):
        if self.sio.connected:
            message = data.get('message')
            self.registerstatus = message
            if data.get('status') == "register_success":
                self.registercomplete = True


    def ready(self):
        if self.sio.connected:
            self.sio.emit("is_ready")
            self.is_ready = True

    def notReady(self):
        if self.sio.connected:
            self.sio.emit("not_ready")
            self.is_ready = False


    def on_timer(self, countdown):
        if self.sio.connected:
            self.timer = countdown

    def on_timer_off(self):
        if self.sio.connected:
            self.timer = None

    def on_wait_for_start(self, data):
        if self.sio.connected:
            for n in data:
                global_var.player_cars.append(n)
            SpriteGen.create_Server_cars()
            global_var.help_car = True

    '''Aktualsiert die Positionen, etc der AI Autos und der anderen Mitspieler'''
    def on_updated_positions(self, data):
        self.new_car_data.clear()
        for n in data:
            if n.get("id") != global_var.username:
                self.new_car_data.append(n)
            else:
                Cars.update_player(n)
        Cars.update_server_cars()

    '''Signalisiert, dass das RENNEN startet'''
    def on_start_race(self, data):
        if self.sio.connected:
            global_var.game_countdown_start = data
            game_var.gameStart = True
            global_var.game_start = True
            self.sio.emit("start_watch")
    '''Countdown der bis zum START des Spiels übermittelt wird'''
    def on_start_race_timer(self, data):
        if self.sio.connected:
            global_var.game_countdown_start = data


    def client_is_ingame(self):
        if self.sio.connected:
            self.sio.emit("client_is_ingame")
    '''Verbindungsaufbau mit dem Server'''
    def connect(self):
        try:
            self.sio.connect(self.server_url, transports=['websocket'])
        except:
            print("Verbindung fehlgeschlagen")

    '''Registrieren'''
    def send_register_data(self, user, password):
        if self.sio.connected:
            if len(user) < 3 or len(password) < 6:
                self.errormessage = "Der Username muss mindestens 3 Zeichen lang sein. Das Passwort mindestens 6 Zeichen lang sein."

            else:
                data = {"user": user, "password": password}
                self.sio.emit("register", data)
    '''Anmelden'''
    def send_login_data(self, user, password):
        if self.sio.connected:
            if len(user) < 3 or len(password) < 6:
                self.errormessage = "Der Username muss mindestens 3 Zeichen lang sein.Das Passwort mindestens 6 Zeichen lang sein."
            else:
                data = {"user": user, "password": password}
                self.playersname = user
                global_var.username = user
                self.sio.emit("login", data)
    '''Verbindungsabbruch'''
    def disconnect(self):
        if self.sio.connected:
            self.sio.disconnect()

    def newMessage(self, message):
        if self.sio.connected:
            self.sio.emit('sent_message', message)
    '''Verlässt die Lobby'''
    def leave_lobby(self):
        self.lobbymessage = ''
        global_var.id_playerList = []
        self.is_ready = False
        self.timer = None
        self.sio.emit("leave_lobby")
    '''Sucht ein schnelles Spiel'''
    def get_lobby(self):
        if self.sio.connected:
            self.sio.emit("get_lobby")
    '''Sendet einen übergegebenn Lobbycode ab'''
    def join_lobby(self, lobbycode):
        if self.sio.connected:
            if lobbycode != '':
                data = {"lobby": lobbycode}
                self.sio.emit("join_lobby", data)
            else:
                self.lobbystatus = "Bitte gib eine LobbyID ein"

    '''Erstellt eine eigene Lobby'''
    def create_lobby(self):
        if self.sio.connected:
            self.sio.emit("create_lobby")
    '''Teilt den anderen mit, dass man selbst das Spiel verlässt'''
    def game_leave(self):
        if self.sio.connected:
            self.sio.emit('game_leave')
    '''Übermittelt die eigene Position'''
    def ingame_pos(self, position, offset):
        if self.olddata != position:
            data = {
                "offset": offset,
                "pos": position
            }
            self.olddata = position
            self.sio.emit("ingame_pos", data)
