from tkinter import *
from essential_generators import DocumentGenerator
import time
import re

width = 700
height = 400
start = None
prompt = ''
WPM = None
time_elapsed = None
regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

master = Tk()
w = Canvas(master, width=width, height=height)
w.pack()
w.config(bg="#152642")

w.create_text(width/2, height/5, fill="white",font=('Roboto', 24), text="Welcome to Speed Typer!")

def reset_prompt(*args, **kwargs):
    global prompt, start
    gen = DocumentGenerator()
    prompt = gen.sentence().replace("\n", "")
    prompt = re.sub(' +', ' ', prompt)
    if(regex.search(prompt)==None):
        w.create_text(width/2, height/2, width=width, fill="white", font=('Roboto', 16), text=prompt, tag="prompt")
    else:
        prompt = re.sub(regex, '', prompt)
    start = None

def reset_timer(*args, **kwargs):
    global start
    if start == None:
        start = time.time()
        print(start)

def run_input(*args, **kwargs):
    global WPM, time_elapsed
    end = time.time()
    time_elapsed = end-start
    text = user_input.get()
    color = ["green", "yellow", "red"]
    if text != '':
        if text == prompt:
            user_input.delete(0, END)
            WPM = (len(text)/5)/time_elapsed
            if WPM > 1:
                color = color[0]
            elif WPM > 0.5:
                color = color[1]
            else:
                color = color[2]
            w.delete("prompt")
            w.create_text(width/2, height/2, width=width, fill=color, font=('Arial', 15), text="""
            Time elapsed: {}
            WPM: {}
            """.format(time_elapsed, WPM), tag="msg")
            master.update()
            time.sleep(2)
            w.delete("msg")
            reset_prompt()
        else:
            w.delete("prompt")
            w.create_text(width/2, height/2, width=width, fill="red", font=('Arial', 15), text="Sorry, but your text doesn't match!", tag="msg")
            master.update()
            time.sleep(1)
            w.delete("msg")
            w.create_text(width/2, height/2, width=width, fill="white", font=('Arial', 15), text=prompt, tag="prompt")
            master.update()

user_input = Entry(master, width=100)
user_input.pack()
user_input.focus()

user_input.bind("<Key>", reset_timer)
master.bind("<Return>", run_input)
reset_prompt()

mainloop()