from app import create_app, config

from flask_socketio import SocketIO

app = create_app(config=config.DevelopmentConfig())

socketio = SocketIO(logger=True)
socketio.init_app(app)

# for testing only
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

print("Starting Socketio")

socketio.run(
    app=app,
    port=5000,
    debug=True,
    log_output=True,
    use_reloader=False
)

print("Socket Closed")