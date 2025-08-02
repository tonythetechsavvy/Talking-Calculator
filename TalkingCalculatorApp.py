import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
import speech_recognition as sr
import pyttsx3
import re

# Set app theme
Window.clearcolor = (0.05, 0.05, 0.05, 1)  # Dark background

# voice engine setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  

def speak(text):
    engine.say(text)
    engine.runAndWait()

def parse_spoken_input(spoken_text):
    # Convert spoken words to math expression
    spoken_text = spoken_text.lower()
    replacements = {
        "plus": "+", "minus": "-", "times": "*", "x": "*", 
        "divided by": "/", "divide": "/", "over": "/", 
        "equals": "=", "equal": "=", "power": "**"
    }
    for word, symbol in replacements.items():
        spoken_text = spoken_text.replace(word, symbol)
    spoken_text = re.sub(r'[a-zA-Z]', '', spoken_text)  # Remove other words
    return spoken_text.strip()

class CalculatorApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10)

        self.display = TextInput(font_size=32, size_hint=(1, 0.3),
                                 background_color=(0.1, 0.1, 0.1, 1),
                                 foreground_color=(0, 1, 0.6, 1), readonly=True)
        self.add_widget(self.display)

        btn_layout = BoxLayout(orientation='vertical', spacing=10)
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"]
        ]
        for row in buttons:
            h_layout = BoxLayout(spacing=10)
            for label in row:
                btn = Button(text=label, font_size=24, background_color=(0.15, 0.15, 0.15, 1),
                             color=(1, 1, 1, 1), on_press=self.on_button_press)
                h_layout.add_widget(btn)
            btn_layout.add_widget(h_layout)

        self.add_widget(btn_layout)

        bottom_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        clear_btn = Button(text="Clear", on_press=self.clear_display, background_color=(0.8, 0, 0, 1))
        speak_btn = Button(text=" Speak", on_press=self.listen_command, background_color=(0, 0.5, 1, 1))
        bottom_layout.add_widget(clear_btn)
        bottom_layout.add_widget(speak_btn)
        self.add_widget(bottom_layout)

    def on_button_press(self, instance):
        text = instance.text
        if text == "=":
            try:
                result = str(eval(self.display.text))
                self.display.text = result
                speak(f"Here’s your result, It's {result}")
            except:
                self.display.text = "Error"
                speak("Apologies , there was an error.")
        else:
            self.display.text += text

    def clear_display(self, _):
        self.display.text = ""
        speak("Clearing input.")

    def listen_command(self, _):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            speak("I’m listening")
            try:
                audio = recognizer.listen(source, timeout=5)
                voice_text = recognizer.recognize_google(audio)
                print("Heard:", voice_text)

                if "clear" in voice_text:
                    self.clear_display(None)
                    return
                if "exit" in voice_text:
                    speak("Goodbye.")
                    App.get_running_app().stop()
                    return

                math_expr = parse_spoken_input(voice_text)
                print("Parsed:", math_expr)
                self.display.text = math_expr
                try:
                    result = str(eval(math_expr))
                    self.display.text = result
                    speak(f"Here’s your result,  It's {result}")
                except:
                    self.display.text = "Error"
                    speak("Sorry sir, I couldn't calculate that.")
            except sr.UnknownValueError:
                speak("I couldn’t understand, Mr. Stark.")
            except sr.WaitTimeoutError:
                speak("No input detected, sir.")

class Calculator(App):
    def build(self):
        self.title = "Talking Calculator"
        self.author = "All rights reserved, Tony the Tech Guy"
        return CalculatorApp()

if __name__ == '__main__':
    Calculator().run()
