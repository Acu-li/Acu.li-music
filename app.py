from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

MUSIC_FOLDER = './music'
PASSWORD = "yourpassword"  # Setze hier dein Passwort

if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER)

# Index-Seite für den Music Player im Windows 95 Stil
@app.route('/')
def index():
    songs = [song.replace('.mp3', '') for song in os.listdir(MUSIC_FOLDER)]
    songs = os.listdir(MUSIC_FOLDER)
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Music Player</title>
        <style>
            body {
                background-color: #C0C0C0; /* Windows 95 Standard-Hintergrundfarbe */
                font-family: "MS Sans Serif", Geneva, sans-serif;
                margin: 50px;
            }
            #player-container {
                background-color: #E0E0E0;
                border: 2px solid #000000;
                padding: 10px;
                width: 300px;
            }
            h1 {
                font-size: 14px;
                font-weight: bold;
                color: #000000;
                margin-bottom: 20px;
            }
            button {
                font-family: "MS Sans Serif";
                font-size: 12px;
                background-color: #D3D3D3;
                border: 2px solid #A0A0A0;
                padding: 5px;
                margin-right: 5px;
                cursor: pointer;
                width: 70px;
            }
            button:active {
                border: 2px solid #505050;
            }
            input[type=range] {
                width: 100%;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div id="player-container">
            <h1 id="song-title">{{ songs[0] if songs else 'No songs available' }}</h1>
            <audio id="audio-player" style="display:none;">
                <source id="audio-source" src="/music/{{ songs[0] }}" type="audio/mpeg">
            </audio>
            <button onclick="previousSong()">Back</button>
            <button onclick="togglePlay()">Play</button>
            <button onclick="nextSong()">Next</button>
            <input type="range" id="volume-slider" min="0" max="1" step="0.01" value="1" onchange="setVolume(this.value)">
        </div>
        <script>
            let songs = {{ songs|tojson }};
            let currentSongIndex = 0;
            let audioPlayer = document.getElementById('audio-player');
            let songTitle = document.getElementById('song-title');
            
            function setVolume(volume) {
                audioPlayer.volume = volume;
            }

            function previousSong() {
                if (songs.length > 0) {
                    currentSongIndex = (currentSongIndex - 1 + songs.length) % songs.length;
                    changeSong();
                }
            }

            function nextSong() {
                if (songs.length > 0) {
                    currentSongIndex = (currentSongIndex + 1) % songs.length;
                    changeSong();
                }
            }

            function togglePlay() {
                if (audioPlayer.paused) {
                    audioPlayer.play();
                } else {
                    audioPlayer.pause();
                }
            }

            function changeSong() {
                let newSong = songs[currentSongIndex];
                audioPlayer.src = '/music/' + newSong;
                songTitle.innerText = newSong;
                audioPlayer.play();
            }
        </script>
    </body>
    </html>
    ''', songs=songs)

# Admin-Seite zum Hochladen von Songs bleibt unverändert
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if request.form['password'] != PASSWORD:
            return "Unauthorized", 401
        if 'file' not in request.files or request.files['file'].filename == '':
            return redirect(request.url)
        file = request.files['file']
        if file:
            file.save(os.path.join(MUSIC_FOLDER, file.filename))
            return redirect(url_for('index'))
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload Song</title>
    </head>
    <body>
        <h1>Upload a new song</h1>
        <form method="post" enctype="multipart/form-data">
            <input type="password" name="password" placeholder="Enter password">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    </body>
    </html>
    ''')

# Route zum Bereitstellen der Musikdateien
@app.route('/music/<filename>')
def music(filename):
    return send_from_directory(MUSIC_FOLDER, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
