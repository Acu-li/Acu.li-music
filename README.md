1.  make /music folder

1.5 change password for uploading in app.py

2.  docker build -t music-player .

3.  docker run -p 5000:5000 -v C:/{urlink}/music:/app/music music-player

4. upload on ``theip:5000/upload`` with password and mp3 file
