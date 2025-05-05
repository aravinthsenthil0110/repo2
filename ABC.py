import speech_recognition as sr
import pyttsx3
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

r = sr.Recognizer()
engine = pyttsx3.init()

database = {
    "abhinaya": {"Register Number": 1, "Department": "Information Technology", "Date of Birth": "29 May 2004", "Gender": "Female"},
}

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def process_text(text):
    tokens = word_tokenize(text)
    print(f"Tokens: {tokens}")
    pos_tags = pos_tag(tokens)
    print(f"POS Tags: {pos_tags}")

    names = []
    temp_name = []
    for word, tag in pos_tags:
        if tag == 'NNP':
            temp_name.append(word)
        elif temp_name:
            names.append(" ".join(temp_name))
            temp_name = []
    if temp_name:
        names.append(" ".join(temp_name))

    if names:
        name = names[0].strip().lower()
        print(f"Extracted name: {name}")
        if name in database:
            details = database[name]
            return f"Name: {name.capitalize()}\nRegister Number: {details['Register Number']}\nDepartment: {details['Department']}\nDate of Birth: {details['Date of Birth']}\nGender: {details['Gender']}"
        else:
            return f"Sorry, I couldn't find information about {name.capitalize()}."
    else:
        return "I didn't hear any name. Please try again."

def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    while True:
        text = listen()
        if text:
            if "exit" in text.lower():
                print("Exiting program.")
                speak("Goodbye!")
                break
            response = process_text(text)
            print(response)
            speak(response)
        else:
            speak("Sorry, I couldn't hear you. Please try again.")
