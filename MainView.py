'''
Created on Dec 3, 2018
View and GUI Builder for the main window of Studio Notes

@author: Emma Poffenberger
'''

from Recording import Recording
from Playback import Playback
from FileManagerView import FileView
import Project

from tkinter import *
from tkinter.ttk import Progressbar

import threading

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider

#from Example
import random
import json
import numpy as np
from pydub import AudioSegment
from pydub.utils import make_chunks
import pyaudio
from threading import Lock, Thread

from test.test_statistics import _DoNothing


#startup - have popup window to select directory and set name then open main view
class View():
    def __init__(self):

        #fileView = FileView()

        self.rec = Recording()        
        self.play = Playback()

        #Temp 
        self.play.openPlayback()
        self.np = np
                
        #Window Settings
        self.root = Tk()
        self.root.state('zoomed')
        self.root.wm_minsize(400, self.root.winfo_screenheight()-150)
        matplotlib.use('TkAgg')

        self.root.rowconfigure(0, weight = 1 )
        self.root.rowconfigure(1, weight = 1 )
        self.root.columnconfigure(1, weight = 1 )

        self.OpenSequence()
        
        
    def OpenSequence(self):
        
        self.root.title("StudioNotes - " + Project.fileName )
        
        #Menu Bar for top of window         - Method Call
        menuBar = self.Menu(self.root)        
        #Status Bar at bottom of window     - Method Call 
        statusBar = self.Status(self.root, "") 
        #Tool Bar at side of window         - Method Call
        toolBar = self.Tool(self.root)        
        #Audio Frame - Placeholder for audio Files
        audioFrame = self.AudioArea(self.root)        
        #NoteModel Frame Text widget for notes
        noteFrame = self.NoteArea(self.root)

        
        if Project.close == True:
            self.root.destroy()
                
        self.root.mainloop()
        
    ''' GUI for the top menu bar ''' 
    def Menu(self, root):
        menuBar = Menu(root)
        
        #File drop-down menu for the menu bar
        fileMenu = Menu( menuBar, bg ='white', tearoff = 0 )
        menuBar.add_cascade(label='File', menu=fileMenu)
        fileMenu.add_command(label = 'New Project',     command = _DoNothing )
        fileMenu.add_command(label = 'Open Project',    command = _DoNothing )
        fileMenu.add_command(label = 'Import Audio',    command = _DoNothing )
        fileMenu.add_command(label = 'Export Project',  command = _DoNothing )
        fileMenu.add_command(label = 'Save',            command = _DoNothing )
        fileMenu.add_command(label = 'Save As',         command = _DoNothing )
        fileMenu.add_command(label = 'Close',           command = _DoNothing )
        fileMenu.add_separator()
        fileMenu.add_command(label = 'Exit',            command=root.quit )       
        
        #Edit drop-down menu for the menu bar
        editMenu = Menu( menuBar, bg ='white', tearoff = 0 )
        menuBar.add_cascade(label = 'Edit', menu = editMenu )
        editMenu.add_command(label = 'Undo',            command = _DoNothing )
        editMenu.add_command(label = 'Redo',            command = _DoNothing )
        editMenu.add_separator()
        editMenu.add_command(label = 'Cut',             command = _DoNothing )
        editMenu.add_command(label = 'Copy',            command = _DoNothing )
        editMenu.add_command(label = 'Paste',           command = _DoNothing )  
        editMenu.add_separator()
        
        #Tools for audio editing drop down menu
        toolMenu = Menu( menuBar, bg ='white', tearoff = 0 )
        audioEdit = Menu( toolMenu, tearoff = 0 )
        noteEdit = Menu( toolMenu, tearoff = 0 )
        menuBar.add_cascade(label = 'Tools', menu=toolMenu)
        toolMenu.add_command(label = 'Settings', command = _DoNothing )
        toolMenu.add_separator()
        toolMenu.add_cascade(label='Audio', menu = audioEdit )
        audioEdit.add_command(label = 'Open Recording File',         command = self.rec.openRec )
        audioEdit.add_command(label = 'Close Recording File',            command = self.rec.closeRec )
        audioEdit.add_separator()
        audioEdit.add_command(label = 'Open Playback File',      command = self.play.openPlayback )
        audioEdit.add_command(label = 'Close Playback File',        command = self.play.closePlayback )
        audioEdit.add_separator()
        audioEdit.add_command(label = 'Fade In',       command = _DoNothing )
        audioEdit.add_command(label = 'Fade Out',       command = _DoNothing )
        audioEdit.add_separator()
        audioEdit.add_command(label = 'Zoom In',        command = _DoNothing )
        audioEdit.add_command(label = 'Zoom Out',       command = _DoNothing )
        
        
        toolMenu.add_cascade(label='Notes', menu = noteEdit )
        noteEdit.add_command(label = 'New Note',   command = _DoNothing )
        noteEdit.add_separator()
        noteEdit.add_command(label = 'Undo',            command = _DoNothing )
        noteEdit.add_command(label = 'Redo',            command = _DoNothing )
        
        #Help menu
        helpMenu = Menu(menuBar, bg ='white', tearoff = 0 )
        menuBar.add_cascade(label = 'Help', menu=helpMenu)
        helpMenu.add_command(label = 'Tutorial',       command = _DoNothing )
        
        root.config(menu=menuBar)
    
    
    ''' GUI for the bottom status bar '''   
    def Status(self, root, text):
        status = Label(root, text=text, bg = 'white', bd=1, relief=SUNKEN, anchor=W )  
        status.grid( row=2, column =0, columnspan = 2, sticky = S + E + W )
        status.columnconfigure(0, weight = 1)
            
    ''' GUI for left-side tool bar '''
    def Tool(self, baseFrame):  
        toolFrame = Frame( baseFrame, bg='white', bd=1, relief=RIDGE )
        
        blankLabel1 = Label(toolFrame, text=' ', bg='white', height=2 )
        blankLabel1.grid(row=0)

        audioLabel = Label(toolFrame, text='Audio Tools:', bg='white', width=20)
        audioLabel.grid(row=1, columnspan=2, sticky=W) # (side=TOP, padx=2, pady =2)
        blankLabel2 = Label(toolFrame, text=' ', bg='white', height=0 )
        blankLabel2.grid(row=2)
        
        #Audio Tools buttons
        #openREC = Button(toolFrame, text='Open Recording', width=13, command = self.rec.openRec )
        #openREC.grid( row=3, column=0, sticky=W, padx=5, pady=3 )
        #closeREC = Button(toolFrame, text='Close Recording', width=13, command = self.rec.closeRec )
        #closeREC.grid( row=3, column=1, sticky=W, padx=5, pady=3 )
        
        #openPLAY = Button(toolFrame, text='Open Playback', width=13, command = self.play.openPlayback )
        #openPLAY.grid( row=4, column=0, sticky=W, padx=5, pady=3 )
        #closePLAY = Button(toolFrame, text='Close Playback', width=13, command = self.play.closePlayback )
        #closePLAY.grid( row=4, column=1, sticky=W, padx=5, pady=3 )
        
        select = Button(toolFrame, text='Select', width=8 )
        #select.grid( row=5, columnspan=2, sticky=W, padx=5, pady=3 )
        select.grid( row=3, columnspan=2, sticky=W, padx=5, pady=3 )
        
        cutTool = Button(toolFrame, text='Cut', width=8 )
        #cutTool.grid( row=6, columnspan=2, sticky=W, padx=5, pady=3 )
        cutTool.grid( row=4, columnspan=2, sticky=W, padx=5, pady=3 )
        
        norm = Button(toolFrame, text='Normalize', width=8 )
        #norm.grid( row=7, columnspan=2, sticky=W, padx=5, pady=3 )
        norm.grid( row=5, columnspan=2, sticky=W, padx=5, pady=3 )
        
        fadeIn = Button(toolFrame, text='Fade In',  width=8 )
        #fadeIn.grid( row=8, column=0, sticky=W, padx=5, pady=3 )
        fadeIn.grid( row=6, column=0, sticky=W, padx=5, pady=3 )
        fadeOut = Button(toolFrame, text='Fade Out', width=8)
        #fadeOut.grid( row=8, column=1, sticky=W, padx=5, pady=3 )
        fadeOut.grid( row=6, column=1, sticky=W, padx=5, pady=3 )
        
        zoomIn = Button(toolFrame, text='Zoom In', width=8 )
        #zoomIn.grid( row=9, column=0, sticky=W, padx=5, pady=3 )
        zoomIn.grid( row=7, column=0, sticky=W, padx=5, pady=3 )
        zoomOut = Button(toolFrame, text='Zoom Out', width=8 )
        #zoomOut.grid( row=9, column=1, sticky=W, padx=5, pady=3 )
        zoomOut.grid( row=7, column=1, sticky=W, padx=5, pady=3 )
        
        #NoteModel tools Buttons
        blankLabel3 = Label(toolFrame, text=' ', bg='white', height=11 )
        #blankLabel3.grid(row=10)
        blankLabel3.grid(row=8)
        noteLable = Label(toolFrame, text='Note Tools:', bg='white', width=20)
        #noteLable.grid( row=11, columnspan=2, sticky=W,)
        noteLable.grid( row=9, columnspan=2, sticky=W,)
        blankLabel4 = Label(toolFrame, text=' ', bg='white', height=1 )
        #blankLabel4.grid(row=12)
        blankLabel4.grid(row=10)
        
        note = Button(toolFrame, text='New Note', width=8, command = lambda: self.noteButton(self.root, self.textArea) )
        #note.grid( row=13, columnspan=2, sticky=W, padx=5, pady=3)
        note.grid( row=11, columnspan=2, sticky=W, padx=5, pady=3)
        
        undo = Button(toolFrame, text='Undo', width=8 )
        #undo.grid( row=14, column=0, sticky=W, padx=5, pady=3 )
        undo.grid( row=12, column=0, sticky=W, padx=5, pady=3 )
        redo = Button(toolFrame, text='Redo', width=8 )
        #redo.grid( row=14, column=1, sticky=W, padx=5, pady=3 )
        redo.grid( row=12, column=1, sticky=W, padx=5, pady=3 )
        
        #toolFrame.pack(side=LEFT, fill=Y)
        
        toolFrame.grid(row=0, rowspan = 2,column=0, sticky="nsw", padx=5, pady =2 )
        toolFrame.columnconfigure(0, weight = 1)
    
    def noteButton(self, root, textArea):
        length = textArea.get(1.0, END)
        if( length is None):
            return textArea.insert( END, '[00:00]')
        else:
            return textArea.insert( END, '\n\n[00:00]')
        
        
    ''' GUI for the Audio '''   
    def AudioArea(self, baseFrame):
        audioFrame = Frame( baseFrame, bg='blue', bd=1, relief=RIDGE )
        
        audioFrame.rowconfigure(0, weight = 1 )
        audioFrame.rowconfigure(1, weight = 1 )
        audioFrame.rowconfigure(2, weight = 1 )
        audioFrame.columnconfigure(0, weight = 1 )
        audioFrame.columnconfigure(1, weight = 1 )

        '''a'''
        '''
        wavFrame = Frame( audioFrame, bg='white', bd=1, relief=RIDGE)
        wavFrame.rowconfigure(0, weight = 1 )
        wavFrame.columnconfigure(0, weight = 1 )        
        
        #canvas for Figure
        audio = AudioSegment.from_wav('output.wav')
        duration =int( audio.duration_seconds * 22 )
        if duration == 0:
            duration = 1
        maxLoudness = audio.max
        
        
        self.fig = plt.Figure(figsize=(20, 3))
        canvas = FigureCanvasTkAgg(self.fig, wavFrame)
        canvas.get_tk_widget().grid(row=0, column=0, sticky="NWE", pady = 10, padx = 10 )

        self.ax=self.fig.add_subplot(111)
        #self.fig.subplots_adjust(bottom=0.25)

        Project.RATE = audio.frame_rate
        Project.SIGNAL = audio.get_array_of_samples()
        final_signal = []
        for i in range(len(Project.SIGNAL)):
            if i % (audio.channels*Project.REDUCTION_FACTOR) == 0:
                final_signal.append(Project.SIGNAL[i])
        Project.SIGNAL = np.array(final_signal)

        self.ax.axis([0, duration, -maxLoudness, maxLoudness])
        self.ax.plot(Project.SIGNAL)

        #ax_time = self.fig.add_axes([0.12, 0.1, 0.78, 0.03])
        #WHAT IS A SAMPLE
        cursor = SnaptoCursor(self.ax, range(len(Project.SIGNAL)), Project.RATE/Project.REDUCTION_FACTOR)
        canvas.mpl_connect('motion_notify_event', cursor.mouse_move)
        #self.fig.mpl_connect('motion_notify_event', cursor.mouse_move)

        cursor_player = CursorPlayer(audio, range(len(Project.SIGNAL)), self.ax, Project.RATE/Project.REDUCTION_FACTOR)
        canvas.mpl_connect('button_press_event', cursor_player.onclick)
        #self.fig.mpl_connect('button_press_event', cursor_player.onclick)
        #canvas.mpl_show()
        #canvas.draw()
        plt.show()'''
        
        wavFrame.grid(row=0, column = 0, columnspan = 2, sticky="WES", pady = 5, padx = 5 )        
       
        '''a'''
        playbackControlFrame = Frame( audioFrame, bg='light gray', bd=1, relief=RIDGE)
        playbackControlFrame.rowconfigure(0, weight = 1 )
        playbackControlFrame.rowconfigure(1, weight = 1 )
        playbackControlFrame.columnconfigure(0, weight = 1 )
        playbackControlFrame.columnconfigure(1, weight = 1 )
        playbackControlFrame.columnconfigure(2, weight = 1 )
        playbackControlFrame.columnconfigure(3, weight = 1 )
        
        reverse = Button( playbackControlFrame, text='Reverse', width=10, bg='white' )
        reverse.grid( row= 0, column=0, sticky=E, padx=5, pady=5 )

        self.playPause = Button( playbackControlFrame, text='Play', width=10, bg='white', command = self.handelerPlayback )
        self.playPause.grid( row= 0, column=1, sticky=E, padx=5, pady=5 )
        
        forward = Button( playbackControlFrame, text='Forward', width=10, bg='white' )
        forward.grid( row= 0, column=2, sticky=E, padx=5, pady=5 )

        self.record = Button(playbackControlFrame, text='Record', width=10, bg='white')#, command = self.handelerRecording )
        self.record.grid( row= 0, column=3, sticky=E, padx=30, pady=5 )
        
        playbackControlFrame.grid(row=1, column = 0, columnspan = 2, sticky="WE", pady = 3, padx = 3 )
            
            
        playbackFrame = Frame( audioFrame, bg='white', bd=1, relief= RIDGE )
        playbackFrame.columnconfigure(1, weight = 1 )
        
        #label for current time
        #self.playbackCurrentTime(playbackFrame)

        self.progress = Progressbar(playbackFrame, length = playbackFrame.winfo_width() )
        self.progress.grid( row = 0, column = 1, sticky = "WE", pady = 5, padx = 5)
        
        #label for total time
        #self.playbackEndTime(playbackFrame)
        
        playbackFrame.grid(row=2, column = 0, columnspan = 2, sticky="WES", pady=3, padx=3 )
        
        audioFrame.grid(row=0, column = 1, columnspan = 2, sticky="WNE", pady = 3, padx = 5 ) 

    
    ''' GUI for the NoteModel Section '''
    def NoteArea(self, baseFrame):
        noteFrame = Frame( baseFrame, bg='white', bd=1, relief = RIDGE )
        
        noteFrame.rowconfigure(0, weight = 1)
        noteFrame.rowconfigure(1, weight = 1 )
        noteFrame.columnconfigure(0, weight = 1 )
        noteFrame.columnconfigure(1, weight = 1 )
        
        
        self.textArea = Text(noteFrame )
        self.textArea.config(highlightbackground = 'black', highlightthickness = 1 )
        scroll = Scrollbar(noteFrame)
        self.textArea.configure(yscrollcommand=scroll.set)
        self.textArea.grid(row=0, column=0, columnspan =2, sticky=W+E+S, padx=5, pady=10)
        self.textArea.columnconfigure(1, weight = 1 )
        scroll.grid(row=0, column = 2, sticky = "NSE")
        
        noteFrame.grid(row=1, column = 1, sticky="WSE", pady = 5, padx = 5 )
       
    
    
    ''''''
    
    def playbackCurrentTime(self, playbackFrame):
        currentTime = self.play.getCurrentTime()
        startTime = Label(playbackFrame, text=currentTime, bg = 'white', bd=1, relief=SUNKEN, anchor=E)
        startTime.grid( row=0, column = 0, sticky = E, pady=10, padx=10)
                
    def playbackEndTime(self, playbackFrame):
        time = self.play.getEndTime()
        endTime = Label(playbackFrame, text=time, bg = 'white', bd=1, relief=SUNKEN, anchor=W )  
        endTime.grid( row=0, column =2,  sticky = W, pady=10, padx=10 )
        

    def changeState(self):
        #check to see if playback or recording button was pressed
        if Project.audioBool == True:
            Project.audioBool = False
        else:
            Project.audioBool = True

    def changeStateRecording(self):
        if Project.continueRecording == True:
            Project.continueRecording = False
            self.record.config( relief = RAISED)
            self.Status(self.root, "Recording Ended")
            self.rec.closeRec()
        elif Project.continueRecording == False and Project.continuePlayback == False:
            Project.continueRecording = True
            self.record.config( relief = SUNKEN)
            self.Status(self.root, "Recording Started")
            self.rec.openRec()
        else:
            self.Status(self.root, 'Cannot start Recording - Playback in progress')
            
    def changeStatePlayback(self):
        if Project.continuePlayback == True:
            Project.continuePlayback = False
            self.Status(self.root, "Playback Paused")
            self.play.closePlayback()
            
        elif Project.continuePlayback == False and Project.continueRecording == False:
            Project.continuePlayback = True
            self.Status(self.root, "Playing " + Project.Wav_fileName )
            self.play.openPlayback()
            #self.play.play()
        else:
            self.Status(self.root, 'Cannot start Playback - Recording in progress')       
        
    def handelerRecording(self):
        if Project.continuePlayback == False:
            self.changeStateRecording()
            threading.Thread(target=self.rec.record).start()
    
    def handelerPlayback(self):
        self.changeStatePlayback()
        playThread = threading.Thread(target= self.play.playback)
        if Project.continuePlayback == True:
            print( 'playback Thread started')
            playThread.start()
        else:
            print( 'playback thread stopped')
            playThread._stop()
            '''
    
class CursorPlayer(object):

    def __init__(self, audio, x, ax, rate):
        self.audio = audio
        self.seg = make_chunks(audio, Project.SAMPLERATE)
        self.x = x
        self.ly = ax.axvline(color='k', alpha=0.25)
        self.isPlaying = False
        self.sem1 = Lock()
        self.sem2 = Lock()
        self.rate = rate

    def onclick(self, event):
        self.sem1.acquire()
        self.isPlaying = False
        self.sem1.release()
        self.sem2.acquire()
        x = event.xdata
        if event.button == 1 and x is not None:
            if x < 0:
                x = 0
            t = Thread(target=self.play, args=(self.seg, self.audio, x,))
            t.daemon = True
            self.sem1.acquire()
            if not self.isPlaying:
                self.isPlaying = True
                t.start()
            self.sem1.release()
        self.sem2.release()

    def play(self, seg, audio, pos):
        self.sem2.acquire()
        pos = pos/self.rate
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(audio.sample_width),
                        channels=audio.channels,
                        rate=audio.frame_rate,
                        output=True)
        for chunk in seg[int(pos * (1000/Project.SAMPLERATE)):]:
            self.sem1.acquire()
            if not self.isPlaying:
                self.sem1.release()
                break
            else:
                self.sem1.release()
                t = Thread(target=self.move_cursor, args=(seg.index(chunk) * (20*(Project.SAMPLERATE/100.)),))
                t.start()
                stream.write(chunk._data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        self.sem2.release()

    def move_cursor(self, x):
        if x % (100 * (100./Project.SAMPLERATE)) == 0:
            self.ly.set_xdata(x * self.rate / (100 * (100./Project.SAMPLERATE)))
            t = Thread(target= plt.draw)
            t.start()

class SnaptoCursor(object):

    def __init__(self, ax, x, rate):
        self.ax = ax
        self.ly = ax.axvline(color='k', ls='dashed', alpha=0.75)
        self.x = x
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)
        self.rate = rate

    def mouse_move(self, event):
        if not event.inaxes:
            return
        x = event.xdata
        if x < 0:
            x = 0
        self.ly.set_xdata(x)
        self.txt.set_text('sec = %1.0f' % (x/self.rate))
        plt.draw()'''


View() 