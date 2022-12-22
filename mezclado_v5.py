# ESTABLISH  16-46

"""
    Notebook for streaming data from a microphone in realtime

    audio is captured using pyaudio
    then converted from binary data to ints using struct
    then displayed using matplotlib

    scipy.fftpack computes the FFT

    if you don't have pyaudio, then run

    pip install pyaudio

    note: with 2048 samples per chunk, I'm getting 20FPS
    when also running the spectrum, its about 15FPS
"""
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import threading
# from pyqtgraph.Qt import QtGui, QtCore
# import pyqtgraph as pg
import struct
# from scipy.fftpack import fft
import sys
import time
import datetime
import wave
import time
from config import Settings, Routes 

class AudioStream(object):
    def __init__(self):
        self.routes = Routes()
        self.FRAMES = []
        # stream constants
        self.CHUNK = 1024 * 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.pause = False
        self.CHUNK2 = 1024
        self.STATUS = 0
        self.RECORD_SECONDS = 5
        #datetimes = str(datetime.datetime.now().strftime("%d_%m_%y__%H-%M-%S")) + ".wav"
        self.filenames = self.random_name("record") 

        #WAVE_OUTPUT_FILENAME = self.routes.base_audio_url + self.routes.file_wav + ".wav"
        WAVE_OUTPUT_FILENAME =  self.routes.base_audio_url + self.filenames + ".wav"             
        # guardamos en self.routes.base_audio = 
        self.p = pyaudio.PyAudio()
        self.ESTADO = 0
        # stream object

        self.STREAM = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        #print("* recording")

        # self.init_plots()
        #self.routes.create_mkdir
        self.start_frame(0,True , datetimer=WAVE_OUTPUT_FILENAME)

    def random_name(name_base):
 
        #suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join([name_base, suffix])
        return filename

    def start_frame(self, Contador, val , datetimer):
     
        FRAMES = []
        stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            # output=True,
            frames_per_buffer=self.CHUNK)

        # while  self.ESTADO == 1:

         #while not self.pause:

        data = stream.read(self.CHUNK)
        data_int = np.frombuffer(data, dtype='h')
        data_np = np.array(data_int, dtype='h')

        if 400 <= np.amax(data_np) <= 4033:
            print("estas hablando= " + str(np.amax(data_np)))
            #self.ESTADO = 1
            #self.start_frame()
            
            #print(" recording 5 seg" )
            #for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            while val == True:   
                #print(str(Contador))  
                data = stream.read(self.CHUNK)
                data_int = np.frombuffer(data, dtype='h')
                data_np = np.array(data_int, dtype='h')
                FRAMES.append(data)
                #print(str(np.amax(data_np)))
                if np.amax(data_np) <= 333:
                    
                    Contador +=1
                    if Contador > 60:
                        val = False
                        #print("no estas hablando...")
                elif 400 <= np.amax(data_np) <= 1000 :
                    Contador = 0
                    #print(" estas hablando...")  

            print(" record end: " + str(datetime.datetime.now().strftime("%d %m %y_%H %M %S")))
            #print("* done recording")
            stream.stop_stream()
            stream.close()
            self.p.terminate()
            wf = wave.open(datetimer, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(FRAMES))
            wf.close()



    # def stop_frame(self):
    #     self.ESTADO = 0
    #     print("RETURN STATUS 0 ")


if __name__ == '__main__':
    print("Init...")
    while True:
        AudioStream()


