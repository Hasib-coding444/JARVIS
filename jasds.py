import datetime
import webbrowser
import os
import smtplib
import speech_recognition as sr
import pyttsx3
import urllib.parse
import requests
from bs4 import BeautifulSoup
import random

# Text-to-speech setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# OpenWeatherMap API key
API_KEY = "0041488485ab7c4696b249a958600136"

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Greet the user
def greet():

    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak(" I am Jarvis. How can I assist you today?")

# Take user command
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 8)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Sorry, I couldn't understand. Can you please repeat?")
        return "None"
    return query

# Process user query and generate response
def process_query(query, weather):
    response = ""
    if 'open youtube' in query:
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube..."
    elif 'open google' in query:
        webbrowser.open("https://www.google.com")
        response = "Opening Google..."
    elif 'search in google' in query:
        speak('What do you want to search for?')
        search_query = take_command()
        encoded_query = urllib.parse.quote(search_query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        webbrowser.open(search_url, new=2, autoraise=False)  # Open in background
        response = f"Searching in Google for {search_query}..."
    elif 'play music' in query:
        music_dir = 'C:\\Music'  # Replace with your music directory path
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
        response = "Playing music..."
    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"The time is {strTime}"
    elif 'send a email' in query:
        try:
            speak("What should I say?")
            content = take_command()
            speak("Who is the recipient?")
            recipient = take_command()
            to = recipient.lower().replace(" ", "") + "@example.com"  # Modify the domain as per your email provider
            # Code to send email using SMTP
            response = "Email has been sent!"
        except Exception as e:
            print(e)
            response = "Sorry, I couldn't send the email."
    elif 'how are you' in query:
        response = "I'm doing well, thank you for asking!"
    elif 'who are you' in query:
        response = "I am Jarvis, your personal assistant."
    elif 'how is the weather' in query:
        response = weather if weather else "I'm sorry, I don't have weather information at the moment."
        if weather:
            suggestions = get_weather_suggestions(weather)
            if suggestions:
                response += "\nHere are some suggestions based on the weather:\n" + "\n".join(suggestions)
    elif 'tell me a joke' in query:
        joke = get_joke()
        response = joke if joke else "I'm sorry, I couldn't fetch a joke at the moment."
    elif 'change voice' in query:
        random_voice = random.choice(voices)
        engine.setProperty('voice', random_voice.id)
        response = "Sure, I have changed my voice!"
    elif 'Goodbye' in query or 'exit' in query or 'see you' in query:
        response = "Goodbye!"
    else:
        response = "I'm sorry, I don't have information about that."

    return response

# Get weather information from OpenWeatherMap API
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        temperature = data['main']['temp']
        condition = data['weather'][0]['description']
        return f"The weather in {city} is {condition} with a temperature of {temperature} degrees Celsius."
    except:
        return None

# Get weather-based suggestions
def get_weather_suggestions(weather):
    
    suggestions = []
    if 'rain' in weather.lower():
        suggestions.append("Carry an umbrella or raincoat.")
        suggestions.append("Stay indoors and enjoy a good book or movie.")
    elif 'cloud' in weather.lower():
        suggestions.append("It might be a good day to go for a walk.")
        suggestions.append("Consider having a picnic with friends or family.")
    elif 'sun' in weather.lower():
        suggestions.append("Take a break and enjoy some time outdoors.")
        suggestions.append("Go for a swim or visit a nearby park.")
    return suggestions

# Get a random joke
def get_joke():
    try:
        url = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(url)
        data = response.json()
        setup = data['setup']
        punchline = data['punchline']
        return f"{setup}\n{punchline}"
    except:
        return None

# Main program loop
if __name__ == "__main__":
    greet()
    while True:
        query = take_command().lower()

        # Get weather information
        weather = get_weather("Tangail")

        # Process user query and generate response
        response = process_query(query, weather)

        # Speak the response
        speak(response)

        if 'goodbye' in query or 'exit' in query or 'Goodbye' in query:
            break
