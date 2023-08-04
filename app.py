import os
import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pytube import YouTube
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.static_folder = 'data'
port = 5000

scheduler = BackgroundScheduler()
scheduler.start()



# Path to receive download requests
@app.route('/download', methods=['POST'])
def download_video():
    url = request.json['url']
    # Call the function to download the video
    downloaded_videos = download_all_resolutions(url)

    return jsonify(downloaded_videos)

# Get YouTube videos
def download_all_resolutions(url):
    videos = []
    try:
        video = YouTube(url)

        for stream in video.streams.filter(file_extension="mp4"):
            if stream.resolution:
                calidad = stream.resolution

                # Create a folder with the name of the video
                video_folder = f"data/{video.title}"
                os.makedirs(video_folder, exist_ok=True)

                file_name = f"{video.title}_{calidad}.mp4".replace(" ", "_")

                # Save the file in the corresponding folder
                stream.download(output_path=video_folder, filename=file_name)

                videos.append({
                    'title': video.title,
                    'resolution': calidad,
                    'downloadUrl': f"https://{request.host}/download/{video.title}/{file_name}"                })
    except Exception as e:
        print("Error:", e)

    return videos


def clean_old_files():
    max_days = 10  # Set maximum age in days for files

    # Get current date
    actual_date = datetime.datetime.now()

    # Loop through the files in the "data" folder
    carpeta_data = "data"
    for root, _, files in os.walk(carpeta_data):
        for archivo in files:
            archivo_path = os.path.join(root, archivo)

            # Get file modification date
            modify_date = datetime.datetime.fromtimestamp(os.path.getmtime(archivo_path))

            # Calculate the time difference between the current date and the modified date
            time_difference = actual_date - modify_date

            # Check if the file is older than the set limit
            if time_difference.days > max_days:
                # Delete the file
                os.remove(archivo_path)




# Path to serve downloaded files
@app.route('/download/<path:video_title>/<path:filename>', methods=['GET'])
def download_file(video_title, filename):
    return send_file(f"data/{video_title}/{filename}", as_attachment=True)


if __name__ == "__main__":
    scheduler.add_job(clean_old_files, trigger='interval', weeks=1)

    app.run(host='0.0.0.0', port=port)
