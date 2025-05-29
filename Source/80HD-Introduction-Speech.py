import pyttsx3

#Set voice parameters
engine = pyttsx3.init()
voices = engine.getProperty('voices')
#Set voice speed
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)
engine.setProperty('voice', voices[2].id)  # Try different indexes

#engine.say("Hello my name is 80 H D")
#engine.runAndWait()


engine.say("Hello humans I am 80 HD");
engine.runAndWait()
