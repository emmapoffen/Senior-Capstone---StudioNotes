#this is a config file centered around the project open

import pyaudio as py
import wave
import os.path
from pydub import AudioSegment
import numpy as np 
from test.test_statistics import _DoNothing

'''threading variables'''
continueRecording = False
continuePlayback = False
audioBool = False

close=False



#Project Contents:
fileName = 'default.studio'
Wav_fileName = 'output.wav'
print(Wav_fileName)


#format
BITDEPTH = py.paInt16
#Channel
CHANNELS = 2
#rate
RATE = 44100
#chunk
SAMPLERATE = 1024

REDUCTION_FACTOR = 2000

FRAMES = []
SIGNAL = []
#WAVE_FILENAME = 'output.wav'

#'''Demo Playback track'''
#WAV_INPUT_FILENAME = 'output.wav'
#WAV_INPUT_FILENAME = '18-31252_T02_fantasia on Greensleeves_11-06-18.wav'

def loadAudio():
    print(Wav_fileName)
    '''try:
        audio = AudioSegment.from_wav(Wav_fileName)
        print('File Opened')
    except:
        wave.open(Wav_fileName, 'wb').close()
        print('created wav file')
        audio = AudioSegment.from_wav(Wav_fileName)
    finally:
        return print('error finding audio file')
    '''
    open(Wav_fileName, 'wb').close()
    audio = AudioSegment.from_wav(Wav_fileName)
    SIGNAL = audio.get_array_of_samples()
    
    for i in range( len(SIGNAL) ):
        if i % (audio.channels* 2000 ) == 0:
            FRAMES.append(SIGNAL[i])
            
    SIGNAL = np.array(FRAMES)    

def saveProject():
    _DoNothing

def openProject( file ):
    try:
        with open(file,'w') as UseFile:
            return True
    except:
        print("File cannot be created or found")
        return False
