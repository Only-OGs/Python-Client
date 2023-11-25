import socketio

# statische Mehtode, um Fehler Verbindungsprobleme zu reagieren.
def handle_connection_error(error):
    print(f"Error connecting to the server: {error}")

#erstellt Client und Serverkommunikation
class SocketIOClient:
    def __init__(self):
        self.server_url = "http://89.58.1.158:8080"
        self.sio = socketio.Client(logger=True, engineio_logger=True)
        # reagiert auf die das angeg. Event
        self.sio.on('connection_success', self.on_connection_success)
        self.sio.on('response', self.on_response)

    def on_connection_success(self, data):
        print(f"Verbindung zum Server mit  Dir ({data}) erfolgreich")


    def on_response(self, data):
        print(f"Server response received: {data}")
        self.process_response(data)

    def process_response(self, data):
        status = data.get('status')
        message = data.get('message')

        if status == 'success':
            print(f"Antwort vom Server: {message}")
        if status == 'register_success':
            print(f"Antwort vom Server: {message}")
        if status == 'login_success':
            print(f"Antwort vom Server: {message}")
        if status == 'login_failed':
            print(f"Antwort vom Server: {message}")
        if status == 'register_failed':
            print(f"Antwort vom Server: {message}")


    #stellt die Verbindung zum Server her.
    def connect(self):
        try:
            self.sio.connect(self.server_url, transports=['websocket'])
        except ConnectionError as e:
            handle_connection_error(e)

    def emit_coordinate(self):
        if self.sio.connected:
            data = {"message1": "Hallo", "message2": "Pascal"}
            self.sio.emit("message", data)

    def send_register_data(self, user, password):
        if self.sio.connected:
            data = {"user": user, "password": password}
            self.sio.emit("register", data)

    def send_login_data(self, user, password):
        if self.sio.connected:
            if len(user) < 3 or len(password) < 5:
                raise Exception("Der Username muss mindestens 3 Zeichen lang sein \nDas Passwort mindestens 5 Zeichen lang sein.")
            else:
                data = {"user": user, "password": password}
                self.sio.emit("login", data)