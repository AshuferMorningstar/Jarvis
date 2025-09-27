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
newsapi = "b118d3d84ba049bbaf0de431143c9f3b"

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
    client = OpenAI(api_key="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",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
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
                            audio_stop = r_stop.listen(source, timeout=1, phrase_time_limit=1)
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
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            print(f"[DEBUG] Wake word recognized: {word}")
            if(word.lower() == "jarvis"):
                speak("Yes Sir")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print(f"[DEBUG] Command recognized: {command}")
                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))


