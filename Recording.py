'''
Created on Feb 25, 2019
Updated Feb 28, 2019
    - Intergrated Recording from project AudioRecordingSample
Updated March 12, 2019
    - Fixed and finally added threads!!!

@author: Emma Poffenberger

    Will hold the logic for recording and process the actual recording
    Will hold logic for updating graphics while recording
'''

import Project
import wave
import pyaudio

class Recording():
  
    def openRec(self):
        '''WHEN THIS HAPPENS:
            I need to have a call to clear the wav forms if i can 
            get playback audio to work
        '''
        self.py = pyaudio.PyAudio()
        self.stream = self.py.open( format = Project.BITDEPTH,
                               channels = Project.CHANNELS,
                               rate = Project.RATE,
                               input = True,
                               frames_per_buffer = Project.SAMPLERATE )
        
        self.wf = wave.open(Project.Wav_fileName, 'wb')
        self.wf.setnchannels(Project.CHANNELS)
        self.wf.setsampwidth(self.py.get_sample_size(Project.BITDEPTH))
        self.wf.setframerate(Project.RATE)
    
    Project.FRAMES = []    
           
    def record(self):
        
        while Project.continueRecording:
            self.data = self.stream.read(Project.SAMPLERATE)
            Project.FRAMES.append(self.data)
            print('**')
        
        #or does this need to be moved?????
        #This will propbably need to be moved to close project file
        #This will nedd to be moved to a close project method
        #to continue recording to a already created wav file do i need this to append frames instead of write?
                #research
    def closeRec(self):
        self.wf.writeframes(b''.join(Project.FRAMES))
        self.wf.close()
    