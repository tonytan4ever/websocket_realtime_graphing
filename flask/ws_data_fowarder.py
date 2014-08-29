import os
from threading import Thread

from gevent import monkey
monkey.patch_all()

from flask import Flask, redirect, session, render_template
from flask.ext.socketio import SocketIO, send, emit

import redis

app = Flask(__name__, static_folder=os.path.join(
                            os.path.dirname(
                                os.path.dirname(__file__),
                                ), "static")
                            )
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
redis_subscribe_threads = []

REDIS_HOST_IP = "<your_ip_address>"

redis_connection = redis.Redis(REDIS_HOST_IP)


def subscribe_to_metric(connectionName, metric):
    client = redis_connection.pubsub()
    client.subscribe(metric)
    for item in client.listen():
        if item['type'] == 'message':
            #print item['channel']
            #print item['data']
            if getattr(socketio, "socket_name", None) == connectionName:
                socketio.emit(metric, item['data'],
                           namespace='/start_graphing')


@app.route('/')
def index():
    return render_template("ws_two_metrics_flask_single_chart.html")

@app.route('/multi_charts')
def index_multi_charts():
    return render_template("ws_two_metrics_flask.html")

@app.route('/index')
def redirect_index():
    return redirect("/", code=302)

@app.route('/<connectionName>/<metricName>')
def subscribe(connectionName, metricName):
    global redis_subscribe_threads
    thread = Thread(target=subscribe_to_metric, 
                                args = (connectionName,
                                        metricName))
    thread.start()
    redis_subscribe_threads.append(thread)
    return "Subscribe to metric: %s Successful..." % metricName

@socketio.on('connect', namespace="/start_graphing")
def connect():
    emit('server connected', {'data': 'OK'})
    
@socketio.on('set socket_name', namespace="/start_graphing")
def set_socket_name(message):
    session["socket_name"] = message['data']
    setattr(socketio, "socket_name", message['data'])
    emit('ready', {'data': 'OK'})
    
    

if __name__ == '__main__':
    socketio.run(app)