import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import speech_recognition as sr
from textblob import TextBlob
import turtle
import pyttsx3

# Function to perform sentiment analysis on a given text
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.5:
        return 'Very Positive'
    elif 0.2 <= polarity <= 0.5:
        return 'Positive'
    elif -0.2 <= polarity < 0.2:
        return 'Neutral'
    elif -0.5 <= polarity < -0.2:
        return 'Negative'
    else:
        return 'Very Negative'

# Function to transcribe speech to text with a timeout
def transcribe_audio(language='en-US', timeout=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=timeout)

    try:
        print("Transcribing...")
        text = recognizer.recognize_google(audio, language=language)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        print("Recognition request failed; {0}".format(e))
        return ""

# Function to handle button click event
def start_listening():
    language = language_var.get()
    output_text.delete('1.0', tk.END)  # Clear previous text
    audio_text = transcribe_audio(language)
    if audio_text:
        sentiment = analyze_sentiment(audio_text)
        output_text.insert(tk.END, f"Transcribed text: {audio_text}\nSentiment: {sentiment}\n\n")
        output_text.see(tk.END)  # Scroll to the end of the text widget
        # Speak out the transcribed text
        speak_text(audio_text)

# Function to speak out text using pyttsx3
def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.say(text)
    engine.runAndWait()

# Function to draw shapes using Turtle
def draw_shape(shape, size, color):
    t = turtle.RawTurtle(canvas)
    t.speed(1)
    t.color(color)
    if shape == "Square":
        for _ in range(4):
            t.forward(size)
            t.right(90)
    elif shape == "Circle":
        t.circle(size)
    elif shape == "Triangle":
        for _ in range(3):
            t.forward(size)
            t.left(120)

# Create main window
root = tk.Tk()
root.title("Voice Emotion Detection")
root.geometry("700x500")  # Slightly smaller window size

# Background color
root.configure(bg="#f0f0f0")

# Title label
title_label = tk.Label(root, text="Voice Emotion Detection", font=("Arial", 20), bg="#f0f0f0", fg="#333333")
title_label.pack(pady=20)

# Language selection dropdown
language_var = tk.StringVar()
language_label = tk.Label(root, text="Select Language:", font=("Arial", 12), bg="#f0f0f0", fg="#333333")
language_label.pack()
language_combobox = ttk.Combobox(root, textvariable=language_var, values=['en-US', 'en-GB', 'fr-FR', 'es-ES'], font=("Arial", 12))
language_combobox.pack(pady=5)
language_combobox.current(0)  # Set default value

# Start button
start_button = tk.Button(root, text="Start Listening", command=start_listening, font=("Arial", 14), bg="#007bff", fg="#ffffff", bd=0)
start_button.pack(pady=20)

# Output text widget
output_text = scrolledtext.ScrolledText(root, height=10, width=50, font=("Arial", 12), bg="#ffffff", fg="#333333", bd=0)
output_text.pack(padx=10, pady=5)

# Turtle canvas
canvas = tk.Canvas(root, width=300, height=200, bg="#ffffff", bd=2, relief="ridge")
canvas.pack(pady=10)

# Shape selection dropdown
shape_var = tk.StringVar()
shape_label = tk.Label(root, text="Select Shape:", font=("Arial", 12), bg="#f0f0f0", fg="#333333")
shape_label.pack()
shape_combobox = ttk.Combobox(root, textvariable=shape_var, values=['Square', 'Circle', 'Triangle'], font=("Arial", 12))
shape_combobox.pack(pady=5)
shape_combobox.current(0)  # Set default value

# Size entry
size_label = tk.Label(root, text="Enter Size:", font=("Arial", 12), bg="#f0f0f0", fg="#333333")
size_label.pack()
size_entry = tk.Entry(root, font=("Arial", 12), bd=1)
size_entry.pack(pady=5)

# Color selection dropdown
color_var = tk.StringVar()
color_label = tk.Label(root, text="Select Color:", font=("Arial", 12), bg="#f0f0f0", fg="#333333")
color_label.pack()
color_combobox = ttk.Combobox(root, textvariable=color_var, values=['red', 'blue', 'green', 'black'], font=("Arial", 12))
color_combobox.pack(pady=5)
color_combobox.current(0)  # Set default value

# Button to draw shape
draw_button = tk.Button(root, text="Draw Shape", command=lambda: draw_shape(shape_var.get(), int(size_entry.get()), color_var.get()), font=("Arial", 14), bg="#007bff", fg="#ffffff", bd=0)
draw_button.pack(pady=10)

root.mainloop()
