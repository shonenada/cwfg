from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

import message


msgsrv = message.MessageServer()

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('message.html')


@app.route('/message/')
def message():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        msgsrv.observers.append(ws)
        while True:
            if ws.socket:
                message = ws.receive()
                if message:
                    msgsrv.add_message("%s" % message)
            else:
                return
    return


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
