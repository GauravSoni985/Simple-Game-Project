from tkinter import *
from time import strftime

root = Tk()
root.title("DIGITAL_WATCH")
root.attributes('-fullscreen', True)  #  Fullscreen mode
root.config(bg="#1e1e2f")

use_24hr = True

def toggle_format():
    global use_24hr
    use_24hr = not use_24hr

def update_theme():
    hour = int(strftime('%H'))
    if 6 <= hour < 18:
        label.config(foreground="#00ffcc")
    else:
        label.config(foreground="#ff4d4d")

def show_greeting():
    hour = int(strftime('%H'))
    if hour < 12:
        greet = "Good Morning 🌅"
    elif hour < 18:
        greet = "Good Afternoon ☀️"
    else:
        greet = "Good Evening 🌙"
    greeting.config(text=greet)

def update():
    if use_24hr:
        time_string = strftime('%H:%M:%S')
    else:
        time_string = strftime('%I:%M:%S %p')
    
    date_string = strftime('%A, %d %B %Y')
    
    label.config(text=time_string)
    date_label.config(text=date_string)
    update_theme()
    show_greeting()
    label.after(1000, update)

#  Greeting
greeting = Label(root, font=("Arial", 40), bg="#1e1e2f", fg="#ffaa00")
greeting.pack(pady=20)

#  Time Label
label = Label(root, font=("DS-DIGIT", 100), bg="#1e1e2f", fg="#00ffcc")
label.pack(pady=20)

#  Date Label
date_label = Label(root, font=("Arial", 30), bg="#1e1e2f", fg="white")
date_label.pack(pady=10)

#  Toggle Button
toggle_btn = Button(root, text="Toggle 12/24hr", font=("Arial", 20), command=toggle_format)
toggle_btn.pack(pady=20)

#  Press Esc to Exit Fullscreen
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

update()

root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)
mainloop()
