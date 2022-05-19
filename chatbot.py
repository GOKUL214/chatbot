import random
import json
import pickle
import numpy as np
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("intents.json").read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

def clean_up_sentences(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentences(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i , word in enumerate(words):
            if word == w :
                bag[i] = 1
    return np.array(bag)



def predict_class(sentence, model):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THIRESHOLD = 0.25
    result = [[i, r] for i,r in enumerate(res)  if r > ERROR_THIRESHOLD]

    result.sort(key = lambda x:x[1], reverse=True)
    return_list = []
    for r in result:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intent_list, intent_json):
    tag = intent_list[0]['intent']
    list_of_intent = intent_json['intents']
    for i in list_of_intent:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

# print("GO ! BOT IS RUNNING...  ")

# while True:
#     message = input("")
#     ints = predict_class(message)
#     res = get_response(ints, intents)
#     print(res)

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = get_response(ints, intents)
    return res

#creating GUI with tkinder


import tkinter
from tkinter import *


def send():
    msg = EntryBox.get('1.0', 'end-1c').strip()
    EntryBox.delete('0.0', END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12))

        res = chatbot_response(msg)
        ChatLog.insert(END, 'Bot: ' + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


base = Tk()
base.title("Chatbot")
base.geometry("400x500")
base.resizable(width=False, height=False)
ChatLog = Text(base, bd=0, bg='white', height="8", width="50", font="Arial")
ChatLog.config(state=DISABLED)

scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand']=scrollbar.set

SendButton = Button(base, font=("Verdana", 12, 'bold'), text="Send", width='12', height=5, bd=0, bg='#25cdf7', activebackground='#3c9d9b', fg='#ffffff', command=send)

EntryBox = Text(base, bd=0,bg= 'white', width="29", height="5", font="Arial")

scrollbar.place(x=376, y=6, height=386)
ChatLog.place(x=6, y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

base.mainloop()






