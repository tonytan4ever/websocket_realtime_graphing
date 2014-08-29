from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("ws_two_metrics_flask.html")

@socketio.on('connect', namespace="/start_graphing")
def test_connect(message):
    emit('my response', {'data': 'got it!'})

if __name__ == '__main__':
    socketio.run(app)