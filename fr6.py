import tkinter
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia 
import googlesearch
import webbrowser
import os
import smtplib
import random
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
import requests
from datetime import date
import mysql.connector
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import requests 
import bs4 
from functools import partial
import PIL.ImageTk
import threading
import wikipedia
import pycrypto
import boto3


#to establish sql connection   #user is root, sql password is root, host running in same machine-localhost, name of databse is jarvis
#connection to store commands 
conn = mysql.connector.connect(user = 'root', password = 'root', host = 'localhost', database = 'jarvis')

#connection to make set of instruction
data_Input_1 = mysql.connector.connect(user = 'root', password = 'root', host = 'localhost', database = '')


#newsletterapi #information on officialmail
api_key="9501176e75a54a7d8979787da5fcb854"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice', voices[1].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
#To greet the user
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Fryday Sir. Please tell me how may I help you")       
#to take input
def takeCommand():
    #It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        print("Listnening")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        speak("Recognizing")
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

#Send mail
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('lastyearproject47@gmail.com', 'lastyearproject') #mailid,password
    server.sendmail('lastyearproject47@gmail.com', to, content)
    server.close()

#for sql integration
def saveCommands(query,j):
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    strDate = date.today()
     #print(strTime,strDate)
    for i in range(True):
        sql=f'INSERT INTO Executed_commands(S_no, commands, date, time ) VALUES({j}, "{query}","{strDate}", "{strTime}")'
        myc = conn.cursor()
        myc.execute(sql)
        conn.commit()

def news():
    main_url="https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey="+ api_key
    news=requests.get(main_url).json()
    article=news["articles"]
    news_articles=[]
    for arti in article:
        news_articles.append(arti['title'])
    #print(news_articles)
    for i in range(5):
        print (i+1,news_articles[i])
        speak(f'News {i+1} :  {news_articles[i]} ')
        
    return news_articles

def clicked(query):
    while True:
   

        if 'search google' in query:
            speak('What do You wanna search')
            content = takeCommand()
            speak('Searching Google.... errrrr')
            content =  content.replace("google" , " ")
            speak(f"opening {content}.com")
            webbrowser.open(f"{content}.com")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")
            speak("Opening Google")
         
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
            
        elif 'maps' in query:
            speak('Where do you wanna go')
            content = takeCommand()
            speak('Searching Google maos')
            content =  content.replace("google" , " ")
            speak(f"opening route to {content}")
            webbrowser.open(f"https://www.google.com/maps/place/{content}")


        elif 'open songs' in query:
            notePath = "D:\\Raghav\\Raghav\\Songs"
            os.startfile(notePath)
            
        elif 'close friday' in query:
            speak("Thank For Using me Sir")
            
            break

        elif "temperature" in query:
            speak("Please say the name of Place whose temprature you want to know")
            temp=takeCommand().lower()
            url = "https://google.com/search?q=weather+in+" + temp
            speak("Searching Temprature on Google")
            request_result = requests.get( url )
            soup = bs4.BeautifulSoup( request_result.text 
                         , "html.parser" )
            temprature_mod=  soup.find( "div" , class_='BNeawe' ).text 
            print(temprature_mod)
            speak(temprature_mod)
            
  
            
            
            
                
           

if __name__ == "__main__":
    window = tkinter.Tk()
    window.title("Fryday Automation system")
    window.geometry("2000x2000")
    bg = PhotoImage(file = r"D:\123.png")
    my_label12 = Label(window, image = bg)
    my_label12.place(x=0,y=0,relwidth=1,relheight=1)
    my_text = Label(window, text = " Welcome To Fryday Interface", font=("Helvetica 16 bold italic",20,'bold'),
    foreground = 'white', background='black', borderwidth='10' )
    my_text.pack(pady=50)
    #jarvis button control
    
    query = takeCommand().lower()

    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        l4= Text(window, text=results, font = ("Helvetica 16 bold italic",10,'bold'), 
                foreground = 'black', background='white', borderwidth='10')
        l4.place(x = 0, y = 30) 
        speak("According to Wikipedia")
        print(results)
        speak(results)
        mainloop()
    elif 'news' in query:
        news_list = []
        news_list = news()
        for i in range(0,5):
            if (i == 0):
                l4= Text(window, text=news_list[i], font = ("Helvetica 16 bold italic",10,'bold'), 
                    foreground = 'black', background='white', borderwidth='10')
                l4.place(x = 0, y = 30)
            elif (i == 1):
                l5= Text(window, text=news_list[i], font = ("Helvetica 16 bold italic",10,'bold'), 
                    foreground = 'black', background='white', borderwidth='10')
                l5.place(x = 0, y = 32)
            elif (i == 2):
                l6= Text(window, text=news_list[i], font = ("Helvetica 16 bold italic",10,'bold'), 
                    foreground = 'black', background='white', borderwidth='10')
                l6.place(x = 0, y = 34)
            elif ( i == 3):
                l7= Text(window, text=news_list[i], font = ("Helvetica 16 bold italic",10,'bold'), 
                    foreground = 'black', background='white', borderwidth='10')
                l7.place(x = 0, y = 36)
            elif ( i == 4):
                l8= Text(window, text=news_list[i], font = ("Helvetica 16 bold italic",10,'bold'), 
                    foreground = 'black', background='white', borderwidth='10')
                l8.place(x = 0, y = 38)
            mainloop()
    elif "password" in query:
        x=random.randint(1000,9999)
        s=smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login('lastyearproject47@gmail.com', 'lastyearproject')
        speak("Enter your personal mail id")
        L1 = Label(window, text="User Name")
        L1.place(x=0,y=10)
        E1 = Entry(window, bd =5)
        E1.place(x=0,y=15)
        mailid=input("Enter Mail id :  ")
        s.sendmail('lastyearproject47@gmail.com',E1,"this is otp to execute Fryday Commands {}".format(x))
        speak("To Access This feature , Please Enter Passcode")
        print(" Enter the recived fryday otp ")
        L2 = Label(window, text="User Name")
        L2.place(x=5,y=10)
        E2 = Entry(window, bd =5)
        E2.place(x=5,y=15)
        mainloop()
        
        if E2 == x :
            notePath = "D:\\Raghav\\Raghav\\backup"
            os.startfile(notePath)
        else:
            speak("wrong one time password")
        mainloop()
    elif 'track' in query:
        speak("Enter Phone Number")
        E1 = Entry(window, bd =5)
        E1.place(x=0,y=15)
        ch_num = phonenumbers.parse(E1,"CH")
        ser_num = phonenumbers.parse(E1,"RO")
        countryName=(geocoder.description_for_number(ch_num,"en"))
        serviceProviderName=(carrier.name_for_number(ser_num,"en"))
        print(countryName,serviceProviderName)
        speak(countryName)
        speak(serviceProviderName)
        mainloop()
    elif 'send email' in query:
        try:
            speak("What should I say?")
            content = takeCommand()
            speak("Enter Email id")
            to = Entry(window, bd =5)
            to.place(x=0,y=15)
            #to = takeCommand()
            to = input("Enter Email id : ")
            sendEmail(to, content)
            speak("Email has been sent!")
        except Exception as e:
            print(e)
            speak("Sorry Sir. I am not able to send this email")  
        mainloop()
    else:
        query_1 = query


    btn = tkinter.Button(window, text = "To start Fryday", width = 50, command=partial(clicked,query_1))
    btn.place(x = 550, y = 600)
    mainloop()

    
    

