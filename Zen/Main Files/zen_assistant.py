import speech_recognition as sr
import pyttsx3
import time
import google.generativeai as genai


# Replace this with your actual API key
api_key = 'AIzaSyB-gW9TkxYRPCdcIUT8LGWRtULYj-RiN9E'

# Now pass the key directly to the configure method
genai.configure(api_key=api_key)

# Initialize pyttsx3 TTS engine
engine = pyttsx3.init()

# Configure Zen's voice
voices = engine.getProperty('voices')
# Set to a clear, deep male voice (you can experiment with voices on your system)
engine.setProperty('voice', voices[0].id)  # Change the index if needed
engine.setProperty('rate', 195)  # Adjust speed to sound more formal and clear
engine.setProperty('volume', 1.0)  # Max volume for clear speech

# Zen speaks
def zen_speak(text):
    print(f"Zen: {text}")
    engine.say(text)
    engine.runAndWait()

# Zen listens to the user
def listen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Zen is listening...")
            
            # Adjust for ambient noise with a longer duration
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for 1 second
            
            # Optionally, manually set the energy threshold for background noise
            recognizer.energy_threshold = 5000  # Experiment with different values
            
            # Listen to the source
            audio = recognizer.listen(source)
            try:
                print("Recognizing speech...")
                query = recognizer.recognize_google(audio)
                print(f"You: {query}")
                return query
            except sr.UnknownValueError:
                zen_speak("I didn't quite catch that. Could you please repeat?")
                return None
            except sr.RequestError:
                zen_speak("There was an issue with the network. Please try again.")
                return None
    except OSError:
        zen_speak("Microphone is not available. You can type your command instead.")
        return input("Type your command: ")

# Fallback to text input if the user prefers or microphone fails
def get_user_input(use_microphone):
    if use_microphone:
        user_input = listen()
        if user_input is None:
            zen_speak("You can also type your command if you'd prefer.")
            return input("Type your command: ")
        return user_input
    else:
        return input("Type your command: ")

# Zen interacts with Gemini
def ask_gemini(query, temperature=0.7):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(query, temperature=temperature)

        text_response = response.text

        # Remove formatting characters (bold and italics)
        text_response = text_response.replace("**", "").replace("*", "")
        return text_response
    
    except Exception as e:
        zen_speak(f"An error occurred: {str(e)}")
        return None

# Zen performs a greeting at startup
def greet():
    current_hour = time.localtime().tm_hour
    if current_hour < 12:
        zen_speak("Good morning Tanish, I am Zen, How may I help you?")
    elif 12 <= current_hour < 18:
        zen_speak("Good afternoon Tanish, I am Zen, How may I assist you?")
    else:
        zen_speak("Good evening Tanish, I am Zen, What can I do for you today?")

# Main interaction loop for Zen
if __name__ == "__main__":
    greet()

    while True:
        user_input = get_user_input(True)
        
        response = ask_gemini(user_input)
        if response:
            zen_speak(response)
        if any(phrase in user_input.lower() for phrase in ["stop", "goodbye", "exit"]):
                zen_speak("I'm always here if you need me.")
                break