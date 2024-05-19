from flask import Flask
from dotenv import load_dotenv
from myapi.routes import api
from app import socketio  # Import socketio

load_dotenv()

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(api, url_prefix='/api')

  
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)  # Use socketio.run instead of app.run

