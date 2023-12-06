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
        self.sio.on('search_lobby', self.on_seach_lobby)
        self.sio.on('new_message', self.on_newMessage)
        self.sio.on('lobby_created', self.on_lobbycreated)
        self.sio.on('register', self.on_register)
        self.sio.on('lobby_management', self.on_playerJoined)
        self.sio.on('logout', self.on_logout)
        self.sio.on('login', self.on_login)
        self.sio.on('receive_track', self.on_receiveTrack)
        self.sio.on('game_start', self.on_gameStart)

        # Initialisierung von Variablen für Erfolg/Misserfolg bei Aktionen
        self.logoutstatus = None
        self.loginstatus = None
        self.registerstatus = None
        self.lobbystatus = None
        self.logincomplete = False

    def on_gameStart(self, data):
        var.gameStart = True

    def on_receiveTrack(self, data):
        if self.sio.connected:
            if data != '':
                var.track = data;

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
        pass

    def on_seach_lobby(self, data):
        if self.sio.connected:
            status = data.get('status')
            message = data.get('message')
            self.lobbystatus = message

    def on_logout(self, data):
        if self.sio.connected:
            status = data.get('status')
            message = data.get('message')
            self.logoutstatus = message

    def on_playerJoined(self, data):
        pass

    def on_login(self, data):
        if self.sio.connected:
            message = data.get('message')
            self.loginstatus = message
            self.logincomplete = True

    def on_register(self, data):
        if self.sio.connected:
            message = data.get('message')
            self.registerstatus = message

    # stellt die Verbindung zum Server her.
    def connect(self):
        try:
            self.sio.connect(self.server_url, transports=['websocket'])
        except ConnectionError as e:
            handle_connection_error(e)

    # sendet Koordinaten
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










