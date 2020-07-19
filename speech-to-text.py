import speech_recognition as sr

r = sr.Recognizer()

#Read axe wav file
with sr.AudioFile('axe.wav') as source:
    
    audio_text = r.listen(source)
    
# using google speech recognition
    try:
        
        text = r.recognize_google(audio_text)
        print('Converting audio transcripts into text ...')
        print(text)
     
    except:
         print('Sorry.. run again...')