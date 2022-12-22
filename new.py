import matplotlib.pyplot as plt
import numpy as np
import pyaudio
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import struct
from scipy.fftpack import fft
import sys
import time

# creacion del objeto principal para la captura de audio
class AudioStream(object):
    def _init_(self):

        # constantes para capturar el audio
        self.CHUNK = 1024 * 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 48000  # Fs
        self.pause = False

        # creando el objeto que permite capturar el audio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )
        self.init_plots()
        self.start_plot()

    def init_plot(self):

        # variables para gráficar x para tiempo Xs para frecuencia
        x = np.arange(0, 2 * self.CHUNK, 2)
        xf = np.linspace(0, self.RATE, self.CHUNK)

        # creando la figura con las 2 gráficas dentro
        self.fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
        self.fig.canvas.mp1_connect('button_press_event', self.onClick)

        # graficando datos aleatorios en la gráfica de audio mientras no se reciba nada
        self.line, = ax1.plot(x, np.random.rand(self.CHUNK), '-', lw=2)

        # graficando datos aleatorios en la gráfica de frecuencia mientras no se recibe nada
        self.line_fft, = ax2.plot(xf, np.random.rand(self.CHUNK), '-', lw=2)

        # definiendo los límites de la gráfica de audio en el dominio del tiempo
        ax1.set_title('señal de audio (dominio del tiempo)')
        ax1.set_ylabel('volumen')
        ax1.set_ylim(-10000, 10000)
        ax1.set_xlim(0, 2 * self.CHUNK)
        plt.setp(
            ax1, yticks=[0],
            xticks=[0, self.CHUNK, 2 * self.CHUNK], )
        # Definiendo los limites de la gráfica de audio en el dominio de la frecuencia
        ax2.set_title('señal de audio en el dominio de la frecuencia')
        ax2.set_xlabel('frecuencia')
        ax2.set_ylabel('amplitud')

        ax2.set_xlim(20, self.RATE / 12)
        plt.setp(
            ax2, yticks=[0, 5, 10, 15, 20],
            xticks=[0, 100, 200, 300, 1000, 3000, 4000], )
        # mostrando ventana y definiendo sus dimensiones
        thismanager = plt.get_current_fig_manager()
        thismanager.window.setGeometry(5, 120, 1910, 1070)
        plt.show(block=False)

    # actulizar las graficas en tiempo real
    def start_plot(self):

        print('stream started')
        frame_count = 0
        start_time = time.time()

        while not self.pause:
            # leyendo valores del microfono
            data = self.stream.read(self.CHUNK)

            # convirtiendo estos valores a enteros para poder usarlos
            data_int = np.frombuffer(data, dtype='h')

            # poniendo los valores enteros de dataint en un arreglo
            data_np = np.array(data_int, dtype='h')

            # agregando los valores a la grafica de audio en el dominio del tiempo (self.line)
            self.line.set_ydata(data_np)

            # calculo de la FFT
            yf = np.fft.fft(data_int)

            # agregar los valores de la FFT al gráfico (self.line_FTT)
            self.line_fft.set_ydata(
                np.abs(yf[0:self.CHUNK]) / (128 * self.CHUNK))

            # Identificacion del pico de la frecuencia mas grande de todo el vector de la FFT
            f_vec = self.RATE * np.arange(self.CHUNK / 2) / self.CHUNK  # Vector de frecuencia
            mic_low_freq = 40  # sensibilidad minima del microfono
            low_freq_loc = np.argmin(np.abs(f_vec - mic_low_freq))
            fft_data = (np.abs(np.fft.fft(data_int))[0:int(np.floor(self.CHUNK / 2))]) / self.CHUNK

            # Esta valiriable contiene el pico mas grande
            max_loc = np.argmax(fft_data[low_freq_loc:]) + low_freq_loc

            # prueba find peaks
            # thresh=0.5
            # peak_idx, _=find_peaks(fft_data,height=thresh)

            # print(f_vec[max_loc])

            # deteccion de la nota musical en un minimo de rengo de frecuencia
            if 980 <= f_vec[max_loc] <= 990:
                print("B5 Si")
            if 865 <= f_vec[max_loc] <= 895:
                print("A5 La")
            if 775 <= f_vec[max_loc] <= 800:
                print("G5 Sol")
            if 690 <= f_vec[max_loc] <= 710:
                print("F5 Fa")
            if 650 <= f_vec[max_loc] <= 670:
                print("E5 Mi")
            if 585 <= f_vec[max_loc] <= 595:
                print("D5 Re")
            if 515 <= f_vec[max_loc] <= 550:
                print("C5 Do")
            if 490 <= f_vec[max_loc] <= 500:
                print("B4 Si")
            if 437 <= f_vec[max_loc] <= 447:
                print("A5 La")
            if 390 <= f_vec[max_loc] <= 400:
                print("G4 Sol")
            if 345 <= f_vec[max_loc] <= 355:
                print("F4 Fa")
            if 325 <= f_vec[max_loc] <= 335:
                print("E4 Mi")
            if 290 <= f_vec[max_loc] <= 300:
                print("D4 Re")
            if 255 <= f_vec[max_loc] <= 280:
                print("C4 Do")
            if 243 <= f_vec[max_loc] <= 253:
                print("B3 Si")
            if 215 <= f_vec[max_loc] <= 225:
                print("A3 La")
            if 192 <= f_vec[max_loc] <= 202:
                print("G3 Sol")
            if 172 <= f_vec[max_loc] <= 177:
                print("F3 Fa")
            if 162 <= f_vec[max_loc] <= 167:
                print("E3 Mi")
            if 144 <= f_vec[max_loc] <= 150:
                print("D3 Re")
            if 127 <= f_vec[max_loc] <= 133:
                print("C3 Do")

            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            frame_count += 1


        else:

            self.fr = frame_count / (time.time() - start_time)

            print('average frame rate = {:.0f} FPS'.format(self.fr))

            self.exit_app()

    def exit_app(self):

        print('stream closed')

        self.p.close(self.stream)

    def onClick(self, event):

        self.pause = True


if __name__ == '__main__':
    AudioStream()