import speech_recognition as sr
import pyaudio
import wave

p = pyaudio.PyAudio()

def getAllInputDevices():
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print('Device id ', i, ' - ', p.get_device_info_by_host_api_device_index(0, i).get('name'))

def recordSnippet():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    device_index = 2
    WAVE_OUTPUT_FILENAME = "output.wav"

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def speechToText():
    r = sr.Recognizer()

    #Read axe wav file
    with sr.AudioFile('output.wav') as source:
        
        audio_text = r.listen(source)
        
    # using google speech recognition
        try:
            
            text = r.recognize_google(audio_text)
            print('Converting audio transcripts into text ...')
            print(text)
        
        except Exception:
            print('Sorry.. run again...')

getAllInputDevices()
recordSnippet()
speechToText()