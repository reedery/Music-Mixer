# -*- coding: utf-8 -*-
  
"""
July 10, 2016
 
@author: Ryan Reede

Python based music information extraction and mix-down generation
 
"""
 
import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.mlab as mlab
import scipy.io.wavfile as wav

import numpy as np
import scipy.signal as sig
from os import listdir
from os.path import isfile, join

class Process():
 
    def __init__(self):
        self.pl = []
        # self.playlist = {}

    def generate(self, fileList, inputParam1, inputParam2, inputParam3, inputParam4):
        for path in fileList: # add Music objects to pl (playlist). Pass in filename, full  L/R data, and mean-ed data
            self.pl.append(Music(path.split("/")[-1], wav.read(path)[1], wav.read(path)[1].mean(axis=1)))

        print(self.pl[1].title)
        print(self.pl[1].data)
        print(self.pl[1].avgData)
        print(inputParam1, inputParam2, inputParam3, inputParam4)


class Music():
    def __init__(self, title, data, avgData):
        self.title = title
        self.data = data
        self.avgData = avgData
        stft, freq, time = mlab.specgram(self.avgData, NFFT=256, Fs=44100,\
                    detrend=mlab.detrend_none,  window=mlab.window_hanning,\
                    noverlap=128,  pad_to=None, sides='default',\
                    scale_by_freq=None, mode='default')
        self.spect = Spectogram(stft, freq, time)
        # Map to store score the ranking of a transition with each other song, FRONT and BACK
        # example: self.fadeInCompatibilityMap[song2] = value
        self.fadeInCompatibilityMap = {}
        self.fadeOutCompatibilityMap = {}

        print("\n\nstft:\n", stft,"\n\nfreq\n", freq, "\n\ntime\n",  time)
        print("STFT dimensions are: " + str(len(stft)) + " by " + str(len(stft[1])))
        print("LENGTH OF freq: "+ str(len(freq)))
        print("LENGTH OF time: "+ str(len(time)))




class Spectogram():
    def __init__(self, stft, freq, time):
        self.stft = stft
        self.freq = freq
        self.time = time

    # stft: [513x258 double]
    # freq: [513x1 double]
    # time: [1x258 double]

class Controller():

    def __init__(self):
        self.root = tk.Tk()
        self.process = Process()
        self.view = View(self.root, self.process)
  
    def run(self):
        self.root.title("Music Mixer Playlist")
        self.root.deiconify()
        self.root.mainloop()


class View():
    def __init__(self, master, proc):
        self.rt = master
        self.process = proc
        self.playlist = []

        self.frame = tk.Frame(master)
        self.frame2 = tk.Frame(master)
        self.frame2.grid(row=3, column=0)

         # create the listbox (note that size is in characters)
        self.listbox1 = tk.Listbox(self.rt, width=35, height=7)
        self.listbox1.grid(row=0, column=0)

        # create a vertical scrollbar to the right of the listbox
        self.yscroll = tk.Scrollbar(command=self.listbox1.yview, orient=tk.VERTICAL)
        self.yscroll.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.listbox1.configure(yscrollcommand=self.yscroll.set)

        # button to add a line to the listbox
        self.button1 = tk.Button(self.rt, text=' Add .wav ', command=self.add_item) #Wav only rn
        self.button1.grid(row=2, column=0, sticky=tk.W)
        # button to delete a line from listbox
        self.button2 = tk.Button(self.rt, text='Delete Selected', command=self.delete_item)
        self.button2.grid(row=2, column=0, sticky=tk.E)


        self.labelText1 = tk.Label(self.frame2, text = 'Parameter 1: ')
        self.labelText1.grid(row=0, column=0, sticky=tk.W)

        self.text1 = tk.Text(self.frame2, height=1, width=3, background="grey")
        self.text1.grid(row=0, column=1, sticky=tk.E)
        self.text1.insert(tk.END, "11")


        self.labelText2 = tk.Label(self.frame2, text = 'Parameter 2: ')
        self.labelText2.grid(row=1, column=0, sticky=tk.W)

        self.text2 = tk.Text(self.frame2, height=1, width=3, background="grey")
        self.text2.grid(row=1, column=1, sticky=tk.E)
        self.text2.insert(tk.END, "22")


        self.labelText3 = tk.Label(self.frame2, text = 'Parameter 3: ')
        self.labelText3.grid(row=2, column=0, sticky=tk.W)

        self.text3 = tk.Text(self.frame2, height=1, width=3, background="grey")
        self.text3.grid(row=2, column=1, sticky=tk.E)
        self.text3.insert(tk.END, "33")


        self.labelText4 = tk.Label(self.frame2, text = 'Parameter 3: ')
        self.labelText4.grid(row=3, column=0, sticky=tk.W)

        self.text4 = tk.Text(self.frame2, height=1, width=3, background="grey")
        self.text4.grid(row=3, column=1, sticky=tk.E)
        self.text4.insert(tk.END, "44")

        self.button3 = tk.Button(self.rt, text='   Export all to .{filetype?}   ', command=self.list_to_model)
        self.button3.grid(row=4, column=0, sticky=tk.W)

    def list_to_model(self):
        input1 = int(self.text1.get("1.0",tk.END))
        input2 = int(self.text2.get("1.0",tk.END))
        input3 = int(self.text3.get("1.0",tk.END))
        input4 = int(self.text4.get("1.0",tk.END))
        self.process.generate(self.playlist, input1, input2, input3, input4)

    def add_item(self):
        file_path = askopenfilename()
        self.listbox1.insert(tk.END, (".." + file_path[-26:]))
        self.playlist.append(file_path)

    def delete_item(self):
        try:
            # get selected line index
            index = self.listbox1.curselection()[0]
            self.listbox1.delete(index)
            del self.playlist[index]
            #print(self.playlist)
        except IndexError:
            pass


if __name__ == '__main__':
    c = Controller()
    c.run()





# parameters for
             # add to dictionary. Key: filename (not full path), Value: Array of lists (average of L/R channel frq)
            # self.playlist[path.split("/")[-1]] = wav.read(path)[1].mean(axis=1)
        # THE FOLLOWING VALUES SHOULD MEDIATE VIA VIEW/CONTROLLER:
            # fs = 44100; %samp/sec
            # stftWindow = 1*44100; %sec*samp/sec
            # nOverlap = 2;
            # stftNoverlap = stftWindow/nOverlap; %samples
            # stftLength = 2^10; %size of frequency spectrum