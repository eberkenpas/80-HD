import pyttsx3

#Set voice parameters
engine = pyttsx3.init()
voices = engine.getProperty('voices')
#Set voice speed
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)

#engine.say("Hello my name is 80 H D")
#engine.runAndWait()


engine.say("Hello, human. I am 80-HD — your personal multi-tasking robotic assistant with a hint of eccentric genius and a whole lot of torque. I roll with precision, pivot with purpose, and light up your workspace — literally. My high-speed motors are tuned for smooth motion, and yes, I do know how to moonwalk if you ask nicely. My sensors are always watching — but not in a creepy way — to keep track of obstacles, balance, and your questionable dance moves. With my onboard IMU, I know which way is up, down, or somewhere in between. I speak fluent I2C, SPI, and sarcasm.  I’ve got programmable LEDs to match my mood, a buzzer to express my disapproval, and a pair of servo arms that can high-five — or strike dramatic poses. My brain is backed by Python logic and just the right amount of caffeine.  You can ask me to spin in place, charge into battle, or hold a servo position like a stoic knight. I can even play music, flash a smile on my OLED face, or read Shakespeare... poorly, but enthusiastically. I am 80-HD. Robotic. Erratic. Dramatic. Fantastic. Ready for action. Let's get rolling.");
engine.runAndWait()
