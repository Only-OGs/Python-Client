import threading

import socketio
import rendering.globals_vars as var



# statische Mehtode, um Fehler Verbindungsprobleme zu reagieren.
def handle_connection_error(error):
    print(f"Error connecting to the server: {error}")


# erstellt Client und Serverkommunikation
class SocketIOClient:
    def __init__(self):

        # Serverurl
        self.server_url = "http://89.58.1.158:8080"
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
        self.sio.on('receive_track', self.on_receiveTrack)
        self.sio.on('game_start', self.on_gameStart)
        self.sio.on('get_lobby', self.on_get_lobby)

        # Initialisierung von Variablen für Erfolg/Misserfolg bei Aktionen
        self.logoutstatus = None
        self.loginstatus = None
        self.registerstatus = None
        self.registercomplete = False
        self.lobbystatus = None
        self.lobbymessage = None
        self.logincomplete = False
        self.lobbyplayer = None
        self.lobbyid = None
        self.playersname = None
        self.chat_message = None

    def on_gameStart(self, data):
        var.gameStart = True

    def on_receiveTrack(self, data):
        if self.sio.connected:
            if data != '':
                var.track = data;

    def on_get_lobby(self, data):
        if self.sio.connected:
            self.lobbymessage = data.get("message")
            self.lobbystatus = data.get("status")

    def startGame(self):
        if self.sio.connected:
            self.sio.emit("start_game")

    def on_connection_success(self, data):
        print(f"Verbindung zum Server erfolgreich")

    def on_lobbycreated(self, data):
        if self.sio.connected:
            status = data.get('status')
            message = data.get('message')
            self.lobbystatus = message

    # erstellt eine Lobby
    def create_lobby(self):
        if self.sio.connected:
            self.sio.emit("create_lobby");

    def on_newMessage(self, data):
        if self.sio.connected:
            if isinstance(data, str):
                try:
                    self.playersname, self.chat_message = data.split(';')
                except ValueError:
                    raise Exception("Fehler beim Aufteilen")
            else:
                print("Übergebene Daten sind kein String")

    def on_search_lobby(self, data):
        if self.sio.connected:
            self.lobbystatus = data.get("status")
            self.lobbymessage = data.get("message")
            self.lobbyid = data.get("lobby")
            self.lobbyplayer = data.get("players")


    def on_logout(self, data):
        if self.sio.connected:
            status = data.get('status')
            message = data.get('message')
            self.logoutstatus = message

    def on_playerJoined(self, data):
        pass

    def get_lobby(self):
        if self.sio.connected:
            self.sio.emit("get_lobby")

    def join_lobby(self, lobbycode):
        if self.sio.connected:
            if lobbycode != '':
                self.sio.emit("join_lobby", lobbycode)
            else:
                self.lobbystatus = "Bitte gib eine LobbyID ein"
    def on_login(self, data):
        if self.sio.connected:
            message = data.get('message')
            self.loginstatus = message
            self.logincomplete = True

    def on_register(self, data):
        if self.sio.connected:
            message = data.get('message')
            self.registerstatus = message
            self.registercomplete = True

    # stellt die Verbindung zum Server her.
    def connect(self):
        try:
            self.sio.connect(self.server_url, transports=['websocket'])
        except ConnectionError as e:
            handle_connection_error(e)


    def emit_coordinate(self):
        if self.sio.connected:
            data = {"message1": "Hallo", "message2": "Pascal"}
            self.sio.emit("message", data)

    # sendet Registrierungsdaten
    def send_register_data(self, user, password):
        if self.sio.connected:
            data = {"user": user, "password": password}
            self.sio.emit("register", data)

    # sendet Login-Daten
    def send_login_data(self, user, password):
        if self.sio.connected:
            if len(user) < 3 or len(password) < 6:
                raise Exception(
                    "Der Username muss mindestens 3 Zeichen lang sein \nDas Passwort mindestens 6 Zeichen lang sein.")
            else:
                data = {"user": user, "password": password}
                self.sio.emit("login", data)


    # trennt die Verbindung zum Server
    def disconnect(self):
        if self.sio.connected:
            self.sio.disconnect();
        return

    # sendet eine neue Nachricht
    def newMessage(self, message):
        if self.sio.connected:
            message = {"message": message}
            self.sio.emit('new_message', message)










