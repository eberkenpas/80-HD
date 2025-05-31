import speech_recognition as sr

# List devices cleanly
mics = sr.Microphone.list_microphone_names()
for index, name in enumerate(mics):
    print(f"Device {index}: {name}")
