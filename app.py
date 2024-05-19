from flask import Flask
from dotenv import load_dotenv
from flask_socketio import SocketIO

# Initialize SocketIO
socketio = SocketIO()

def create_app(test_config=None):
    # create and configure the app
    load_dotenv()

    app = Flask(__name__)

    socketio.init_app(app)  # Initialize SocketIO

    with app.app_context():
        from myapi.logger import mylogger
        # Register the blueprint
        from myapi.routes import api
        app.register_blueprint(api, url_prefix='/api')
        mylogger.info('Application Started')
    return app