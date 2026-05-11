
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from datetime import datetime
from eventlet.green.threading import Event

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

socketio = SocketIO(app)

# stores chat messages in memory
chat_history = []

@app.route("/")
def index():
    return render_template("index.html")


# send old messages to new users
@socketio.on("connect")
def handle_connect():
    for msg in chat_history:
        send(msg)


# handle incoming chat messages
@socketio.on("message")
def handle_message(msg):

    # anti spam
    if len(msg["text"]) > 300:
        return

    if msg["text"].strip() == "":
        return

    # add timestamp
    msg["time"] = datetime.now().strftime("%H:%M")

    # save message
    chat_history.append(msg)

    # limit history size
    if len(chat_history) > 100:
        chat_history.pop(0)

    print(msg)

    # send to everyone
    send(msg, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)

