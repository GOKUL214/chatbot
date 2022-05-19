import tkinter
from tkinter import *

def send():
    msg = Entry.get('1.0', 'end-1c').strip()
    Entry.delete('0.0', END)

    if msg!='':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12))

        res = chatbot_respose(msg)
        ChatLog.insert(END, 'Bot: ' + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

base = Tk()
base.title("Chatbot")
base.geometry("400x500")
base.resizable(width=False,height=False)
ChatLog = Text(base, bd=0, bg='white', height="8", width="50",font="Arial")
ChatLog.config(state=DISABLED)

def chatbot_respose():
    pass