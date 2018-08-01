from tkinter import *
import os
import subprocess
from datetime import datetime

ROOT_PATH = "C:\\BOBDocker"
running_p = None

def run():
    os.chdir(ROOT_PATH)
    running_p = subprocess.Popen(["docker-compose","up"], shell=True)

def stop():
    if running_p:
        os.chdir(ROOT_PATH)
        subprocess.run(["docker-compose","down"], shell=True)
        running_p.terminate()
    else:
        print("Please run the application first.")

def take_backup():
    if running_p:
        os.chdir(ROOT_PATH)
        os.chdir("C:\\")
        date = datetime.today().date().strftime("%d-%m-%Y")
        subprocess.run(["docker-compose","exec", "backend", "python", "manage.py", "dumpdata", "--format=json","main",">","data_backup/%s.json"%date], shell=True)
    else:
        print("Please run the application first.")


window = Tk()
window.title("BOB Application")

window.geometry("400x50")

frame = Frame(window)
frame.pack()

button_1 = Button(frame,text="Run", width=15,command=run)
button_1.pack(side=LEFT)

button_2 = Button(frame,text="Stop", width=15,command=stop)
button_2.pack(side=LEFT)

button_3 = Button(frame,text="Backup", width=15,command=take_backup)
button_3.pack(side=LEFT)

window.mainloop()