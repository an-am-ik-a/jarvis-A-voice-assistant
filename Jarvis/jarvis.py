import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import pyjokes
import requests
import datetime
recognizer=sr.Recognizer()  #recognizer object(recognize whatever we speak)
engine=pyttsx3.init() #initialize pyttsx
def speak(text): #speak function which will take text and speak
    engine.say(text)
    engine.runAndWait()
def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            audio = r.listen(source)
            command=r.recognize_google(audio)
        return command
    except Exception as e:
            print("error; {0}".format(e))


def get_news():
    api_key = "a0d7ae5e2a274c0682338c3c54c0fd45"  # 🔑 Replace this with your real API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if data["status"] == "ok":
            articles = data["articles"]
            speak("Here are the top news headlines.")
            for i, article in enumerate(articles[:5], start=1):
                title = article.get("title", "No Title")
                print(f"{i}. {title}")
                speak(title)
        else:
            print("Error from NewsAPI:", data.get("message"))
            speak("Sorry, I couldn't fetch the news.")
    except Exception as e:
        print("An error occurred:", str(e))
        speak("Something went wrong while fetching the news.")
def get_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")  # e.g., 05:17 PM
    return f"The current time is {current_time}"

def get_date():
    today = datetime.datetime.today()
    date = today.strftime("%B %d, %Y")  # e.g., July 09, 2025
    return f"Today's date is {date}"

def get_day():
    day = datetime.datetime.today().strftime("%A")  # e.g., Wednesday
    return f"Today is {day}"



def get_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather = response.text
            print(weather)
            speak(f"Here is the weather: {weather}")
        else:
            speak("Sorry, I couldn't fetch the weather.")
    except:
        speak("An error occurred while fetching the weather.")
    
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        if "search" in c.lower():
            speak("what do you want to search on youtube")
            command=listen()
            webbrowser.open(f"https://www.youtube.com/results?search_query={command}")
        else:
            webbrowser.open("https://youtube.com")
            
            
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://whatsapp.com")
    elif "play" in c.lower():
        if "sad" in c.lower() or "romantic" in c.lower() or "party" in c.lower() or "motivational" in c.lower() or "classic" in c.lower:
            mood= c.lower().split(" ") [1]
            speak("here are some songs according to your mood")
            for name,url in musicLibrary.bollywood_songs[mood].items():
                print(name)
            speak("which song do you want to play")
            song=listen()
            if song in musicLibrary.bollywood_songs[mood]:
                webbrowser.open(musicLibrary.bollywood_songs[mood][song])
            else:
                speak("song is not in the list")

        else:
            music=c.lower.split(" ",1)[1]
            if music in musicLibrary.songs:
                webbrowser.open(musicLibrary.songs[music])
    elif "joke" in c.lower():
        tell_joke()
    elif "weather" in c.lower():
        speak("tell me the city name ")
        city=listen()
        get_weather(city)
    elif "news" in c.lower():
        get_news()
    elif "date" in c.lower():
        print(get_date())
        speak(get_date)
    elif "day" in c.lower():
        print(get_day())
        speak(get_day())
    elif "time" in c.lower():
        print(get_time())
        speak(get_time())
    
    

        
if (__name__ == "__main__"):
    speak("Initializing jarvis.......")
    #listen for the wake word for "jarvis"
    while True:
        r = sr.Recognizer()
        try:

            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source,timeout=2,phrase_time_limit=2) #timeout=2 secs

            command = r.recognize_google(audio)
            if ("jarvis" in command.lower()):
                speak("yes")
                #listen for command
                print("jarvis listening.....")
                command=listen()
                processCommand(command)
        except Exception as e:
            print("error; {0}".format(e))