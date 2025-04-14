import os
import speech_recognition as sr
from isl_translator.isl_translator_complete import translate_text_to_sign
from isl_translator.transcribe import transcribe_audio
from isl_translator.imagetotext import extract_text_from_image
import base64
import io
from PIL import Image, ImageTk
import tkinter as tk
from itertools import count
import numpy as np
import matplotlib.pyplot as plt

class ImageLabel(tk.Label):
    """A label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 50

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames and self.winfo_exists():
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            if self.winfo_exists():
                self.after(self.delay, self.next_frame)

def display_signs(sign_paths):
    root = tk.Tk()
    lbl = ImageLabel(root)
    lbl.pack(expand=True, fill=tk.BOTH)

    def show_next_image(index):
        if index < len(sign_paths):
            path = sign_paths[index]
            adjusted_path = path
            if os.path.exists(adjusted_path):
                if adjusted_path.lower().endswith('.gif'):
                    lbl.load(adjusted_path)

                    # root.after(2000, show_next_image, index + 1)
        
                else:
                    img = Image.open(adjusted_path)
                    img = img.resize((400,400), Image.LANCZOS)
                    img = ImageTk.PhotoImage(img)
                    lbl.config(image=img)
                    lbl.image = img
                    root.after(2000, show_next_image, index + 1)
            else:
                print(f"File not found: {adjusted_path}")
        else:
            root.destroy()

    root.after(0, show_next_image, 0)
    root.mainloop()

def option_text_to_sign():
    text = input("Enter text: ")
    sign_paths = translate_text_to_sign(text)
    display_signs(sign_paths)

def option_voice_to_sign():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something and press 'q' to stop recording...")
        audio = recognizer.listen(source, phrase_time_limit=10)
        print("Recording stopped.")
    
    audio_bytes = audio.get_wav_data()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    audio_data = f"data:audio/wav;base64,{audio_base64}"
    
    transcribed_text = transcribe_audio(audio_data)
    print(f"Transcribed Text: {transcribed_text}")
    
    sign_paths = translate_text_to_sign(transcribed_text)
    display_signs(sign_paths)

def option_image_to_sign():
    file_path = input("Enter the image file path: ")
    
    if os.path.exists(file_path):
        with open(file_path, "rb") as image_file:
            image_bytes = image_file.read()
        
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        image_data = f"data:image/png;base64,{image_base64}"
        
        extracted_text = extract_text_from_image(image_data)
        print(f"Extracted Text: {extracted_text}")
        
        sign_paths = translate_text_to_sign(extracted_text)
        display_signs(sign_paths)
    else:
        print("File not found. Please check the path and try again.")

def main():
    while True:
        print("Select an option:")
        print("1. Text to Sign")
        print("2. Voice to Sign")
        print("3. Image to Sign")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            option_text_to_sign()
        elif choice == '2':
            option_voice_to_sign()
        elif choice == '3':
            option_image_to_sign()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
