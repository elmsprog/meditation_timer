import pyaudio
import time
import tkinter
from tkinter import ttk
import wave


class MedApp(ttk.Frame):
    """The app gui and functions."""
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()

    def on_quit(self):
        """Exits program."""
        quit()

    def play_wav(self, wav_location):
        """Plays wave file."""
        chunk = 1024
        wav_f = wave.open(wav_location, 'rb')
        wav_p = pyaudio.PyAudio()
        stream = wav_p.open(format = wav_p.get_format_from_width(wav_f.getsampwidth()),
                            channels = wav_f.getnchannels(),
                            rate = wav_f.getframerate(), 
                            output = True)
        data = wav_f.readframes(chunk)

        while data:
            stream.write(data)
            data = wav_f.readframes(chunk)
        stream.stop_stream()
        stream.close()
        wav_p.terminate()

    def sleep_timer(self, time_in_minutes):
        """Time delay."""
        time_in_seconds = time_in_minutes * 60
        time.sleep(time_in_seconds)

    def med_timer(self):
        """Gets input and runs methods."""
        if self.mins.get() == "":
            num_mins = 0
        else:
            num_mins = float(self.mins.get())
        self.sleep_timer(num_mins)
        self.play_wav("temple_bell.wav")

    def init_gui(self):
        """Builds GUI."""
        self.root.title('Meditation Timer')
        self.root.option_add('*tearOff', 'FALSE')

        self.grid(column=0, row=0, sticky='nsew')

        self.menubar = tkinter.Menu(self.root)

        self.menu_file = tkinter.Menu(self.menubar)
        self.menu_file.add_command(label='Exit', command=self.on_quit)

        self.menubar.add_cascade(menu=self.menu_file, label='File')

        self.root.config(menu=self.menubar)

        self.mins = ttk.Entry(self, width=5)
        self.mins.grid(column=1, row = 2)

        self.start_button = ttk.Button(self, text='Start',
                command=self.med_timer)
        self.start_button.grid(column=0, row=3, columnspan=4)

        # Labels that remain constant throughout execution.
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


'''BUGS
    -pushing start repeatedly causes the program to queue up plays.
    
'''