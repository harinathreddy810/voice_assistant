Web-Based Voice Assistant built using Python, Flask, HTML, CSS, and JavaScript. It combines speech recognition, text-to-speech, weather retrieval, general knowledge Q&A, and web search functionalities to assist users. 

Speech Recognition and Synthesis: speech_recognition and pyttsx3 libraries are used for capturing voice commands and converting text responses into speech, respectively.
OpenAI API: Used for processing natural language questions that require more general knowledge or advanced responses.
Weather Information: The requests library is used to get real-time weather information from the OpenWeatherMap API.
Browser Interaction: The webbrowser module opens search results in a new browser window.

Key functions include:

talk: Converts text responses to speech.
listen_to_command: Listens to and captures user voice input.
get_time and get_date: Provide the current time and date.
get_weather: Fetches weather data from OpenWeatherMap based on a given city.
get_general_knowledge_answer: Uses the OpenAI API for more complex questions.
process_command: Parses and processes user commands.

Voice-Activated Commands:

Time and Date: Provides current time and date on request.
Weather Information: Retrieves weather details for specified cities.
General Knowledge: Uses OpenAI’s language model for answering complex questions.
Web Search: Opens a Bing search for custom queries.
Greeting: Offers personalized responses to greetings like “hello.”
