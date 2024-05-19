import wget
import os
from PIL import Image , ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip , TextClip
from myapi.s3_service import *
from myapi.logger import mylogger
import uuid
from flask_socketio import emit
from app import socketio
import threading

def process_video(data):

    try:

        video_clip, watermark_logo = createAssets(data)
        sid = data["sid"]
        socketio.emit('progress_update', {'Status': 'createAssets'},  room=sid)
        watermark_text = data["watermark_text"]
        watermark_logo = resize_image("logo.png",video_clip.size)
        watermark_position = calc_watermark_position(watermark_logo.size, video_clip.size)

        # Create a new video clip with the watermark positioned at the bottom-right corner
        video_with_logo = CompositeVideoClip([video_clip, watermark_logo.set_position(watermark_position)], size=video_clip.size)

        text_clip = generateTextClip(watermark_text , video_clip.size , watermark_logo.size) 
        socketio.emit('progress_update', {'status': 'generateTextClip.'}, room=sid)
        # Create a new video clip with the text clip and the video with watermark
        final_video = CompositeVideoClip([video_with_logo, text_clip], size=video_with_logo.size)

        # Set the duration of the new video clip to be the same as the input video
        final_video = final_video.set_duration(video_clip.duration)
        socketio.emit('progress_update', {'Status': 'video_with_watermark'},  room=sid)

        # Write the video file asynchronously
        #threading.Thread(target=write_video_async, args=(final_video,)).start()
        final_video.write_videofile("video_with_watermark.mp4")

        socketio.emit('progress_update', {'Status': 'start uploading'},  room=sid)
        uploaded = uploadVideo()
        #uploaded = False

        cleanupAssets(["logo.png","logo_resized.png","video.mp4" , "text.png" , "video_with_watermark.mp4"])

        if(uploaded is not False):
            socketio.emit('progress_update', {'Status': 'finished' , 'url':uploaded},  room=sid)
            return uploaded
        else:
            
            return False
   
    except Exception as e:
        # Handle exceptions
        socketio.emit('progress_update', {'Status': 'Error'},  room=sid)
        mylogger.error(e)
        return str(e)


def write_video_async(video):
    try:
        video.write_videofile("video_with_watermark.mp4")
    except Exception as e:
        mylogger.error(e)


def cleanupAssets(filenames):
    tmp_directory = ""  # Specify the relative directory
    for filename in filenames:
        file_path = os.path.join(tmp_directory, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)  # Delete the file if it exists
                mylogger.info(f"File '{filename}' deleted successfully.")
            except OSError as e:
                mylogger.error(f"Error deleting file '{filename}': {e}")


def resize_image(image_path, video_size):
        
        image = Image.open(image_path)
        # Get the dimensions of the video
        video_width, video_height = video_size
        # Calculate the new height
        new_height = int(video_height * 0.1)

        # Calculate the new width
        new_width = int(new_height * image.width / image.height)

        # Resize the image
        resized_image = image.resize((new_width, new_height))

        # Save the resized image
        resized_image.save("logo_resized.png")

        # Load the watermark image (replace "logo.png" with your watermark image file)
        watermark = ImageClip("logo_resized.png")

        return watermark

def calc_watermark_position(watermark_size, video_size):
    # Get the dimensions of the video
    video_width, video_height = video_size
    # Get the dimensions of the watermark image
    watermark_width, watermark_height = watermark_size
    # Calculate the position for the watermark at the bottom-right corner
    margin_right = 20
    margin_bottom = 60
    watermark_position = (video_width - watermark_width - margin_right, video_height - watermark_height - margin_bottom)

    return watermark_position


def uploadVideo():
    # Generate a random ID
    random_id = str(uuid.uuid4())[:8] 
    video_file_name = f"video_with_watermark_{random_id}.mp4"
    uploaded = upload_to_s3(f"video_with_watermark.mp4", video_file_name)
    #uploaded = ''
    mylogger.error(uploaded, type(uploaded))

    return uploaded

def createAssets(data):
    try:
        # Download the files
        download_file(data["video_url"], "video.mp4")
        download_file(data["img_url"], "logo.png")

        video_clip = VideoFileClip("video.mp4")
        
        watermark_logo = resize_image("logo.png", video_clip.size)
        
        return (video_clip, watermark_logo) 
    
    except Exception as e:
        # Handle exceptions
        mylogger.error("error downloading assets")
        mylogger.error(e)
        
        raise e
    
def download_file(url, filename):
    """Download a file from the given URL and save it with the specified filename."""
    try:
        wget.download(url, out=filename)
        return filename
    except Exception as e:
        mylogger.error("Error downloading files")
        mylogger.error(e)
        raise RuntimeError(f"Error downloading file from {url}: {e}")    
    
def generateTextClip(clip_txt, video_size , watermark_size):
    try:
        watermark_width, watermark_height = watermark_size
        text_width = int(len(clip_txt)*20 * 0.6 - (20*0.6))
        text_height = 40
        # Create a new image with the desired size
        image = Image.new("RGBA", (text_width,text_height), (0, 0, 0, 0))

        # Get a drawing context
        draw = ImageDraw.Draw(image)

        # Define the font and text color
        font = ImageFont.truetype("Raleway-Bold.ttf", 20)
        text_color = (255, 255, 255)

        # Draw the text on the image
        text_position = (10, 10)
        draw.text(text_position, clip_txt, fill=text_color, font=font)
        # Save the image
        image.save('text.png')
        # Convert the image to a MoviePy ImageClip
        text_clip = ImageClip("text.png")

        # Get the dimensions of the text clip
        text_width, text_height = text_clip.size

        # Calculate the position for the text clip above the previous watermark
        margin_right = 20
        margin_bottom = 60 + watermark_height + 20
        text_position = (video_size[0] - text_width - margin_right, video_size[1] - text_height - margin_bottom)
        text_clip = text_clip.set_position(text_position)

        return text_clip

    except Exception as e:
        # Handle exceptions
        mylogger.error("An error occurred while generating text clip")
        mylogger.error(e)
        raise e
