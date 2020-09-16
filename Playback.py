'''
Created on Feb 25, 2019
Updated Feb 28, 2019
    - Intergrated Recording from project AudioRecordingSample

@author: Emma Poffenberger

    Will hold the logic for updating the Graphics on the MainView.py GUI

'''
#import Recording
#import MainView

import wave
import numpy
from test.test_statistics import _DoNothing
import pyaudio
import Project
from pydub.audio_segment import AudioSegment

class Playback():

    def openPlayback(self, file = "18-31252_T02_fantasia on Greensleeves_11-06-18.wav"):
        self.wf = wave.open(file, 'rb')
        self.py = pyaudio.PyAudio()
        self.chunk = 1024
        
        
        self.stream = self.py.open(
            format = self.py.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )
        
        self.data = self.wf.readframes(self.chunk)
        
    def playback(self):
        while self.stream.is_active():
            
            while self.data != '':
                self.stream.write(self.data)
                self.data = self.wf.readframes(self.chunk)
    
    
    def play(self):
        if self.data == '':
            self.stream.close()
        else:
            self.stream.start_stream()
            tm = self.stream.get_time()
            timeSec = tm /60
            timeMin = timeSec / 60
            print (str(timeMin) + ":" + str(timeSec)) 
        
    
    def pause(self):
        self.stream.stop_stream()
        
    def closePlayback(self):
        self.wf.close()  
