# YouTube Video Downloader using Flask

This is a simple YouTube video downloader built with Flask, a Python web framework. The application allows users to submit a YouTube video URL and download the video in various resolutions (MP4 format). The backend handles the video download and serves the downloadable links to the frontend.

### Requirements
* Python 3.x
* Flask
* Flask-CORS
* pytube
* apscheduler

### Installation
1. Clone this repository to your local machine.

2. Install the required Python packages using pip:

~~~
pip install Flask Flask-CORS pytube apscheduler
~~~
3. Run the Flask app:
~~~
python app.py
~~~
The app will run on <b>'http://localhost:5000'</b> by default. You can access the frontend at this address.

### How it Works
1. The frontend accepts a YouTube video URL from the user.

2. The frontend sends a POST request to the Flask backend with the video URL.

3. The backend uses the <b>'pytube'</b> library to extract information about the video and download it in various resolutions (e.g., 360p, 480p, 720p).

4. The downloaded video files are stored in the data folder on the server.

5. The backend returns a JSON response to the frontend containing information about the downloaded videos, including their titles, resolutions, and download URLs.

6. The frontend displays the list of available video resolutions along with download links.

### Cleaning Old Files
The backend uses the <b>apscheduler</b> library to schedule a task that runs periodically (every week) to clean up old video files that are more than 10 days old. This helps in managing storage space on the server.

### HTTPS Considerations
If you deploy this application to a production server, ensure that it supports HTTPS. Browsers may block mixed content (HTTP and HTTPS) on secure websites. In the provided code, the download URL is constructed using the request.host value, which should include the scheme (https://) when served over HTTPS.

## Authors
#### RibaDev
- GitHub: [@Riba00](https://github.com/Riba00)
- Twitter: [@Riiba00](https://twitter.com/Riiba00)
- LinkedIn: [Jordi RF](https://www.linkedin.com/in/jordi-rf/)