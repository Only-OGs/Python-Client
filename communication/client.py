from rendering.game import Game
import socketio
import rendering.globals_vars as var
from rendering.utility.car_ai import Cars
from rendering.utility.sprite_generator import SpriteGen


# statische Mehtode, um Fehler Verbindungsprobleme zu reagieren.


# erstellt Client und Serverkommunikation
class SocketIOClient:
    def __init__(self):

        # Serverurl
        self.server_url = "http://89.58.1.158:8080"
        # self.server_url = "http://localhost:8080"
        # Client mit aktivem Logging
        self.sio = socketio.Client(logger=True, engineio_logger=True)

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
        self.timer = None

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


    def game_leave(self):
        if self.sio.connected:
            self.sio.emit('game_leave')


    def on_get_leaderboard(self, data):
        if self.sio.connected:
            if data != '':
                var.leaderboard = data
                var.game_end = True


    def on_playerLeave(self, data):
        if self.sio.connected:
            if data.get('status') == 'left':
                self.lobbyleaft = True

    def on_load_level(self, data):
        if self.sio.connected:
            if data != '':
                var.singleplayer = False
                var.track = data

    def on_load_assets(self, data):
        if self.sio.connected:
            if data != '':
                var.assets = data

    def on_get_lobby(self, data):
        if self.sio.connected:
            self.lobbymessage = data.get("message")
            self.lobbystatus = data.get("status")
            if self.lobbystatus == 'success':
                self.quickLobbyJoined = True

    def on_connection_success(self, data):
        print(f"Verbindung zum Server erfolgreich")

    def on_lobbycreated(self, data):
        if self.sio.connected:
            if data.get('status') == 'lobby_created':
                self.lobbycreated = True
                message = data.get('message')
                self.lobbyid = message

    # erstellt eine Lobby
    def create_lobby(self):
        if self.sio.connected:
            self.sio.emit("create_lobby");

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

    def on_search_lobby(self, data):
        print(data)
        if self.sio.connected:
            self.lobbystatus = data.get("status")
            self.lobbymessage = data.get("message")
            self.lobbyid = data.get("lobby")
            if self.lobbystatus == 'success':
                self.searchlobbyJoined = True

    def on_logout(self, data):
        if self.sio.connected:
            status = data.get('status')
            message = data.get('message')
            self.logoutstatus = message

    def on_playerJoined(self, data):
        if self.sio.connected:
            self.lobbystatus = data.get("status")
            if self.lobbystatus == 'joined':
                self.lobbyJoined = True
            self.lobbyid = data.get("lobby")
            var.id_playerList = data.get("players").split(';')

    def leave_lobby(self):
        self.lobbymessage = ''
        var.id_playerList = []
        self.is_ready = False
        self.timer = None
        self.sio.emit("leave_lobby")

    def get_lobby(self):
        if self.sio.connected:
            self.sio.emit("get_lobby")

    def join_lobby(self, lobbycode):
        if self.sio.connected:
            if lobbycode != '':
                data = {"lobby": lobbycode}
                self.sio.emit("join_lobby", data)
            else:
                self.lobbystatus = "Bitte gib eine LobbyID ein"

    def on_login(self, data):
        if self.sio.connected:
            message = data.get('message')
            self.loginmessage = message
            if data.get('status') == "login_success":
                self.logincomplete = True
            else:
                self.playersname  = ''

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

    # stellt die Verbindung zum Server her.
    def connect(self):
        try:
            self.sio.connect(self.server_url, transports=['websocket'])
        except:
            print("fail")

    def emit_coordinate(self):
        if self.sio.connected:
            data = {"message1": "Hallo", "message2": "Pascal"}
            self.sio.emit("message", data)

    # sendet Registrierungsdaten
    def send_register_data(self, user, password):
        if self.sio.connected:
            if len(user) < 3 or len(password) < 6:
               self.errormessage =  "Der Username muss mindestens 3 Zeichen lang sein. Das Passwort mindestens 6 Zeichen lang sein."

            else:
                data = {"user": user, "password": password}
                self.sio.emit("register", data)

    # sendet Login-Daten
    def send_login_data(self, user, password):
        if self.sio.connected:
            if len(user) < 3 or len(password) < 6:
                self.errormessage =  "Der Username muss mindestens 3 Zeichen lang sein.Das Passwort mindestens 6 Zeichen lang sein."
            else:
                data = {"user": user, "password": password}
                var.client.playersname = user
                var.username = user
                self.sio.emit("login", data)

    # trennt die Verbindung zum Server
    def disconnect(self):
        if self.sio.connected:
            self.sio.disconnect()

    # sendet eine neue Nachricht
    def newMessage(self, message):
        if self.sio.connected:
            self.sio.emit('sent_message', message)

    def on_timer(self, countdown):
        if self.sio.connected:
            self.timer = countdown

    def on_timer_off(self, args):
        if self.sio.connected:
            self.timer = None

    def client_is_ingame(self):
        if self.sio.connected:
            self.sio.emit("client_is_ingame")

    def on_wait_for_start(self, data):
        if self.sio.connected:
            for n in data:
                var.player_cars.append(n)
            SpriteGen.create_Server_cars()
            var.help_car = True

    def on_updated_positions(self, data):
        var.new_car_data.clear()
        for n in data:
            if n.get("id") != var.username:
                var.new_car_data.append(n)
            else:
                Cars.update_player(n)
        Cars.update_server_cars()



    def ingame_pos(self, position, offset):
        if var.olddata != position:
            data = {
                "offset": offset,
                "pos": position
            }
            var.olddata = position
            self.sio.emit("ingame_pos", data)

    def on_start_race(self, data):
        if self.sio.connected:
            var.game_countdown_start = data
            var.gameStart = True
            var.game_start = True
            self.sio.emit("start_watch")

    def on_start_race_timer(self, data):
        if self.sio.connected:
            var.game_countdown_start = data
            print(data)



