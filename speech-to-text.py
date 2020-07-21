import speech_recognition as recognition
import pyaudio
import wave

audio = pyaudio.PyAudio()

def getAllInputDevices():
    info = audio.get_host_api_info_by_index(0)
    numberOfDevices = info.get('deviceCount')
    for i in range(0, numberOfDevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print('Device id ', i, ' - ', audio.get_device_info_by_host_api_device_index(0, i).get('name'))

def recordSnippet():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    device_index = 2
    WAVE_OUTPUT_FILENAME = "output.wav"

    stream = audio.open(format=FORMAT,
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
    audio.terminate()

    create = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    create.setnchannels(CHANNELS)
    create.setsampwidth(audio.get_sample_size(FORMAT))
    create.setframerate(RATE)
    create.writeframes(b''.join(frames))
    create.close()

def speechToText():
    recogniser = recognition.Recognizer()

    #Read axe wav file
    with recognition.AudioFile('output.wav') as source:
        
        audio_text = recogniser.listen(source)
        
    # using google speech recognition
        try:
            
            text = recogniser.recognize_google(audio_text)
            print('Converting audio transcripts into text ...')
            print(text)
        
        except Exception:
            print('Sorry.. run again...')

getAllInputDevices()
recordSnippet()
speechToText()