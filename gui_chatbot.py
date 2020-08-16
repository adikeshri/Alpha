import speech_recognition as sr
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import pyttsx3
import requests
from bs4 import BeautifulSoup
import html5lib
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
import spacy
from pygame import mixer
import subprocess
import os
import time
from Actions import getWeather,getTime,sendTextWhatsapp,getNews,calc
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
nlp=spacy.load("en_core_web_lg")



def doAction(tag,message):
    doc=nlp(message)
    if tag=="weather":
        entities=doc.ents
        for entity in entities:
            if entity.label_=="GPE":
                return getWeather.getWeather(entity.text)

    if tag=="playMusic":
        #subprocess.call("spotify")
        #time.sleep(10)
        playPause=os.popen("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause")
    if tag=="time":
        entities=doc.ents
        for entity in entities:
            if entity.label_=="GPE":
                t=getTime.getTime(entity.text)
                return ("It's " + t + " in "+entity.text)
        return getTime.getTime("")

    if tag=="text":
        msg=message.split()
        x=""
        y=""
        for i in range(len(msg)):
            if msg[i]=="to":
                index=-1
                for j in range(i+1,len(msg)):
                    if msg[j]=="saying":
                        index=j
                        break
                    x+=msg[j]+" "
                for j in range(index+1,len(msg)):
                    y+=msg[j]+" "
                x=x.strip()
                y=y.strip()
                break
        return sendTextWhatsapp.sendTextWhatsapp(x,y)

    if tag=="news":
        return getNews.getNews()

    if tag=="calculation":

        return str(calc.calc(message))
    return ""



def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for words that exist in sentence
def bag_of_words(sentence, words, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,word in enumerate(words):
            if word == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % word)
    return(np.array(bag))

def predict_class(sentence):
    # filter below  threshold predictions
    p = bag_of_words(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json,message):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            actionString=doAction(tag,message)
            result+="\n"+str(actionString)
            #actionString=doAction(tag)
            break
    return result




def send(msg):

    if msg != '':
        ints = predict_class(msg)
        res = getResponse(ints, intents,msg)
        return res



print("Alpha has started")
engine=pyttsx3.init()
engine.setProperty('rate', 170)
mixer.init()
mixer.music.load("Sounds/beep.mp3")
while True:
    try:
        rObject=sr.Recognizer()
        with sr.Microphone() as source:
            audio=rObject.listen(source,phrase_time_limit=10)
            text=rObject.recognize_google(audio,language="en-US")
            if "Alpha" not in text and "alpha" not in text:
                print(text)
                continue
            else:
                mixer.music.play()
                audio=rObject.listen(source,phrase_time_limit=10)
                text=rObject.recognize_google(audio,language="en-US")
                print("YOU: " + text)
                result=send(text)
                print("Alpha: "+result)


                engine.say(result)
                engine.runAndWait()
    except KeyboardInterrupt:
        exit()
    except:
        continue
