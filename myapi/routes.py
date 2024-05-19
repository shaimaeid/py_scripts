# routes.py
from flask import jsonify,request, Blueprint, send_from_directory, send_file
from flask import current_app as app
from myapi.db import *
from myapi.campaign_service import *
from myapi.insights_service import *
from myapi.video_service import *
from myapi.tiktok_service import *
#from myapi.azure_db import *
from myapi.mongo_db import *
from myapi.logger import mylogger
from flask_cors import CORS
from functools import wraps
from flask_socketio import emit
from app import socketio
import threading
import time

# Create a Blueprint for the routes
api = Blueprint('api', __name__)
CORS(api)
# Get API secret key from environment variable
api_secret_key = os.environ.get('SECRET_KEY')
valid_api_keys = [api_secret_key]


def requires_api_key(view_func):
    @wraps(view_func)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("Api-Key")
        if api_key in valid_api_keys:
            return view_func(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized"}), 401
        
    return decorated

def check_referer():
    # Check Referer header
    referer = request.headers.get("Referer")
    if referer and "yourwebsite.com" in referer:
        return jsonify({"message": "You have access to this secure endpoint!"})
    else:
        return jsonify({"error": "Unauthorized"}), 401
    
@api.route('/')
def index():
    return 'Hello, this is the response from digifi app test route'

@api.route('/get_users', methods= ['GET','POST'])
@requires_api_key
def get_users():
    
    result = get_users_data()
    result = result.replace(to_replace=np.nan, value=None)
    result = jsonify(result.to_dict(orient='records'))
    print(type(result))
    return result

    
@api.route('/download_logs', methods= ['GET'])
@requires_api_key
def download_logs():
    log_file_path = '/app/api.log'  # Replace with the actual path to your log file

    try:
        return send_file(log_file_path, as_attachment=True)
    except FileNotFoundError:
        return "API Message :: Log file not found", 404
    
    
@api.route('/test_tiktok', methods= ['POST'])
@requires_api_key
def create_tiktok_campaign_route():
    if request.method == 'POST':
        data = request.get_json() 
        result = create_tiktok_campaign(data)
        return jsonify(result)  
    
@api.route('/generate_wm_video', methods= ['POST'])
@requires_api_key
def generate_video_watermark():
    data = {}
    if request.method == 'POST':
        data = request.get_json() 
        
        #result = process_video(data)
        #return {"video_url" : result}
        # Start the process in a separate thread
        threading.Thread(target=process_video, args=(data,)).start()
        return jsonify({"status": "Processing video..."})

    return jsonify(data)

# HTTP route to start the asynchronous task
@api.route('/start_task', methods=['GET'])
def start_task():
    sid = request.args.get('sid')
    # Start the asynchronous task in a separate thread
    threading.Thread(target=do_something_async, args=(sid,)).start()
    return jsonify({'status': 'Task Started.'})

# Dummy asynchronous function to simulate progress
def do_something_async(sid):
    for i in range(10):
        # Simulating some time-consuming task
        time.sleep(1)
        # Emitting progress to connected client identified by sid
        socketio.emit('progress_update', {'status': f'Progress: {i*10}%'}, room=sid)
    # Emitting completion status after finishing the task
    socketio.emit('progress_update', {'status': 'Task completed.'}, room=sid)


@app.route('/.well-known/acme-challenge/<filename>')
def serve_challenge(filename):
    return send_from_directory('.well-known/acme-challenge', filename)

# Define Socket.IO event
@socketio.on('connect')
def handle_connect():
    sid = request.sid
    payload = dict(sid=sid)
    emit('log', payload, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    payload = dict(data='disconnect')
    emit('log', payload, broadcast=True)
    

