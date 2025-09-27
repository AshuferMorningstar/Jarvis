import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
# Insert your NewsAPI key below. Example: newsapi = "your_newsapi_key_here"
newsapi = "your_newsapi_key_here"

# Wake word configuration
# Primary wake words (spoken normally)
WAKE_PRIMARY = ["jarvis"]
# Short/fallback variants that should wake Jarvis but should not be mentioned back
FALLBACK_WAKE_WORDS = ["jar", "jarv", "vish"]

def _normalize_text(s: str) -> str:
    import re
    s = (s or "").lower().strip()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    # Insert your OpenAI API key below. Example: api_key="your_openai_api_key_here"
    client = OpenAI(api_key="your_openai_api_key_here")

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    low = c.lower()
    if "open google" in low:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in low:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in low:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in low:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif low.startswith("open "):
        # Generic open handler: announce then try to open a sensible URL
        target = c.split(" ", 1)[1].strip()
        # Spoken title: capitalize nicely
        title = target.title()
        speak(f"Opening {title}")
        # Map some common words to URLs
        mapping = {
            "google": "https://google.com",
            "youtube": "https://youtube.com",
            "facebook": "https://facebook.com",
            "linkedin": "https://linkedin.com",
            "github": "https://github.com",
        }
        t_low = target.lower()
        if t_low in mapping:
            webbrowser.open(mapping[t_low])
        else:
            # If it looks like a URL, open it; otherwise try https://{target}.com
            if t_low.startswith("http://") or t_low.startswith("https://") or "." in t_low:
                webbrowser.open(target if target.startswith("http") else f"https://{target}")
            else:
                webbrowser.open(f"https://{t_low}.com")
    elif c.lower().startswith("play"):
        song = c.split(" ", 1)[1].strip()
        # Case-insensitive lookup
        found = False
        for key in musiclibrary.music:
            if key.lower() == song.lower():
                link = musiclibrary.music[key]
                webbrowser.open(link)
                speak(f"Playing {key}")
                found = True
                break
        if not found:
            speak("Song not found in the library. Searching on YouTube.")
            import urllib.parse
            query = urllib.parse.quote(song)
            youtube_search_url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(youtube_search_url)

    elif "news" in c.lower():
        print(f"[DEBUG] News command detected: {c}")
        topic = None
        if "about" in c.lower():
            parts = c.lower().split("about", 1)
            topic = parts[1].strip()
        elif c.lower().startswith("news "):
            topic = c[5:].strip()
        elif "search news" in c.lower():
            parts = c.lower().split("search news", 1)
            topic = parts[1].strip()
        # Always include country=us for general headlines, use topic for specific
        if topic:
            url = f"https://newsapi.org/v2/top-headlines?q={topic}&country=us&apiKey={newsapi}"
        else:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        print(f"[DEBUG] NewsAPI top-headlines endpoint: {url}")
        r = requests.get(url)
        print(f"[DEBUG] News API status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"[DEBUG] News API response: {data}")
            articles = data.get('articles', [])
            if articles:
                for article in articles:
                    print(f"[DEBUG] Speaking headline: {article['title']}")
                    speak(article['title'])
                    # Listen for 'stop' after each headline
                    print("Say 'stop' to interrupt...")
                    r_stop = sr.Recognizer()
                    with sr.Microphone() as source:
                        try:
                            audio_stop = r_stop.listen(source, timeout=2, phrase_time_limit=1)
                            command_stop = r_stop.recognize_google(audio_stop).lower().strip()
                            if "stop" in command_stop:
                                print("[DEBUG] Stop command detected. Interrupting news.")
                                break
                        except Exception:
                            pass
            else:
                print("[DEBUG] No news articles found.")
                speak("Sorry, no news articles found.")
        else:
            print("[DEBUG] Failed to fetch news.")
            speak("Failed to fetch news.")
    else:
        # Fallback: open YouTube for music/video, Google for other topics
        import urllib.parse
        query = urllib.parse.quote(c)
        if "music" in c.lower() or "song" in c.lower() or "video" in c.lower():
            youtube_search_url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(youtube_search_url)
            speak(f"Searching YouTube for {c}")
        else:
            google_search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(google_search_url)
            speak(f"Searching Google for {c}")





if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for a short phrase, then check for wake variants
        r = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)

            try:
                transcript = r.recognize_google(audio)
            except Exception as e:
                print(f"[DEBUG] Could not decode audio: {e}")
                continue

            print(f"[DEBUG] Transcript: {transcript}")
            norm = _normalize_text(transcript)
            tokens = norm.split()

            # Check primary and fallback wake words
            woke = False
            for w in WAKE_PRIMARY + FALLBACK_WAKE_WORDS:
                if w in tokens:
                    woke = True
                    break

            if woke:
                # Do not echo which wake token was used; keep a neutral acknowledgement
                speak("Yes Sir")
                # Listen for the command following wake
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=8)
                try:
                    command = r.recognize_google(audio)
                    print(f"[DEBUG] Command recognized: {command}")
                    processCommand(command)
                except Exception as e:
                    print(f"[DEBUG] Failed to recognize command: {e}")

        except Exception as e:
            print("Error; {0}".format(e))


