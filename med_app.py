""" A simple meditation timer for python. """

from threading import Timer
import tkinter
from tkinter import ttk
import wave
import pyaudio


class MedApp(ttk.Frame):
    """ App, GUI, and functions. """
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()

    def on_quit(self):
        """ Exits program. """
        quit()

    def play_wav(self):
        """ Plays WAV file and restores button. """
        chunk = 1024
        wav_f = wave.open("temple_bell.wav", 'rb')
        wav_p = pyaudio.PyAudio()
        stream = wav_p.open(format=wav_p.get_format_from_width(wav_f.getsampwidth()),
                            channels=wav_f.getnchannels(),
                            rate=wav_f.getframerate(),
                            output=True)
        data = wav_f.readframes(chunk)

        while data:
            stream.write(data)
            data = wav_f.readframes(chunk)
        stream.stop_stream()
        stream.close()
        wav_p.terminate()
        self.start_button.config(text='Start', state='normal')
        self.start_button.update()

    def med_timer(self):
        """ Timer and disables button. """
        self.start_button.config(text='Sit', state='disabled')
        self.start_button.update()
        if self.mins.get() == "":
            num_mins = 0
        else:
            num_mins = float(self.mins.get())
        time_in_seconds = num_mins * 60
        t = Timer(time_in_seconds, self.play_wav)
        t.start()

    def init_gui(self):
        """ Builds GUI. """
        self.root.title('Meditation Timer')
        self.root.option_add('*tearOff', 'FALSE')

        self.grid(column=0, row=0, sticky='nsew')

        self.menubar = tkinter.Menu(self.root)
        self.menu_file = tkinter.Menu(self.menubar)
        self.menu_file.add_command(label='Exit', command=self.on_quit)
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.root.config(menu=self.menubar)

        self.mins = ttk.Entry(self, width=5)
        self.mins.grid(column=1, row=2)

        self.start_button = ttk.Button(self, text='Start',
                                       command=self.med_timer)
        self.start_button.grid(column=0, row=3, columnspan=4)

        ttk.Label(self, text='Meditation Timer').grid(column=0, row=0,
                                                      columnspan=4)
        ttk.Label(self, text='Minutes').grid(column=0, row=2,
                                             sticky='w')

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

if __name__ == '__main__':
    root = tkinter.Tk()
    MedApp(root)
    root.mainloop()
