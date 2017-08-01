import os
import time
import serial
import subprocess
import pygame.mixer

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

BASEDIR = os.path.abspath(os.path.dirname(__file__))
ser = serial.Serial('/dev/ttyUSB0', 38400)

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if os.path.basename(event.src_path) == 'record.wav':
            lame_cmd = "lame -b 16 record.wav record.mp3"
            subprocess.call(lame_cmd, shell=True)
            print "start transfar audio data"
            ser.write("<<SENDFILE>>\n")
            readline = lambda : iter(lambda:ser.read(1),"\n")
            ser.write(open("record.mp3","rb").read())
            ser.write("\n<<EOF>>\n")
            print "end transfar audio data"
            return
        elif os.path.basename(event.src_path) == 'watchdog_flag':
            pygame.mixer.music.load("copy.mp3")
            pygame.mixer.music.play(1)
            time.sleep(1)
            pygame.mixer.music.stop()
            return

if __name__ in '__main__':
    pygame.mixer.init()
    while 1:
        event_handler = ChangeHandler()
        observer = Observer()
        observer.schedule(event_handler,BASEDIR,recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
