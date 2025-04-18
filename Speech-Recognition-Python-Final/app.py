from flask import Flask, render_template, request, redirect
import speech_recognition as sr
from pydub import AudioSegment
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            # Convert the MP3 file to WAV using pydub
            audio = AudioSegment.from_mp3(file)
            wav_io = io.BytesIO()
            audio.export(wav_io, format="wav")
            wav_io.seek(0)  # Go to the beginning of the BytesIO object

            # Recognize speech from the WAV data
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_io) as source:
                data = recognizer.record(source)

            try:
                transcript = recognizer.recognize_google(data, key=None)
            except sr.UnknownValueError:
                transcript = "Google Speech Recognition could not understand the audio"
            except sr.RequestError as e:
                transcript = f"Could not request results from Google Speech Recognition service; {e}"

    return render_template('index.html', transcript=transcript)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)