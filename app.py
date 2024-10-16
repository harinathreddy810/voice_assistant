from flask import Flask, render_template, request, jsonify
import datetime
import requests
import openai  # Make sure to install the OpenAI library
import re  # Import regex for command parsing
import speech_recognition as sr
import pyttsx3
import webbrowser  # Import webbrowser to open search results
import time

app = Flask(__name__)

# Initialize OpenAI API
openai.api_key = "your_openai_api_key_here"  # Insert your OpenAI API key

# Initialize the speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def talk(response):
    engine.say(response)
    engine.runAndWait()

# Function to listen to voice commands
def listen_to_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand your voice.")
            return ""
        except sr.RequestError:
            print("Network error. Please try again.")
            return ""

# Function to get the current time
def get_time():
    return datetime.datetime.now().strftime("%H:%M")

# Function to get today's date
def get_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

# Function to get weather information
def get_weather(city):
    api_key = "your_openweathermap_api_key_here"  # Insert your OpenWeatherMap API key
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(weather_url)
        response.raise_for_status()  # Raise an error for bad responses

        data = response.json()
        if data["cod"] == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"The current temperature in {city} is {temp}°C with {description}."
        else:
            return "I couldn't retrieve weather information for that city."
    except Exception as e:
        return f"There was an error retrieving the weather: {str(e)}"

# Function to get general knowledge answers using OpenAI
def get_general_knowledge_answer(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return "I'm unable to answer that right now. Please try again later."

# Process user commands
def process_command(command):
    command = command.lower()  # Normalize command to lowercase

    # Use regex to capture specific commands
    time_regex = re.compile(r'\btime\b')
    date_regex = re.compile(r'\bdate\b')
    weather_regex = re.compile(r'weather in (\w+)')
    search_regex = re.compile(r'\b(search|find)\s+(.*)')

    if time_regex.search(command):
        return f"The current time is {get_time()}."
    elif date_regex.search(command):
        return f"Today's date is {get_date()}."
    elif weather_match := weather_regex.search(command):
        city = weather_match.group(1)
        return get_weather(city)
    elif search_match := search_regex.search(command):
        query = search_match.group(2)
        # Open the search in the default web browser (could be Chrome or any other)
        webbrowser.open(f"https://www.bing.com/search?q={query}")
        return f"Searching for '{query}' on Bing."
    elif 'what is' in command or 'who is' in command or 'tell me about' in command:
        return get_general_knowledge_answer(command)
    elif 'hello' in command:
        return "Hello! How can I assist you today?"
    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase your request?"

# Main function to run the voice assistant
def voice_assistant():
    talk("Voice assistant activated. How can I assist you?")

    while True:
        command = listen_to_command()
        if command:
            response = process_command(command)
            talk(response)  # Respond using text-to-speech
            if "bye" in command or "exit" in command:
                talk("Goodbye!")
                break

# Route for the home page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle commands from the frontend
@app.route('/process-command', methods=['POST'])
def handle_command():
    data = request.get_json()
    command = data.get('command')
    response = process_command(command)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
