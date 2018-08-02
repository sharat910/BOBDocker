from tkinter import *
import os, glob
import subprocess
from datetime import datetime

ROOT_PATH = "C:\\BOBDocker"
BACKUP_PATH = ROOT_PATH + '\\BOB-Backend\\data_backup'
running_p = None

def run():
    global running_p
    os.chdir(ROOT_PATH)
    print("Starting application... To quit press CTRL + C")
    running_p = subprocess.Popen(["docker-compose","up"], shell=True)
    

def stop():
    global running_p
    print(running_p)
    if running_p:
        os.chdir(ROOT_PATH)
        subprocess.run(["docker-compose","down"], shell=True)
        running_p.terminate()
    else:
        print("Please run the application first.")

def migrate():
    os.chdir(ROOT_PATH)
    subprocess.run(["docker-compose","run","backend","python","manage.py","migrate"])
    print("Migrate complete!")

def take_backup():
    global running_p
    if running_p:
        os.chdir(ROOT_PATH)
        date = datetime.today().date().strftime("%d-%m-%Y")
        print("Saving data into %s.json..." % date)
        command = "python manage.py dumpdata main > data_backup/%s.json"%date
        subprocess.run(["docker-compose","exec", "backend","sh", "-c", command], shell=True)
        print("\nBackup complete!")
    else:
        print("Please run the application first.")

def get_latest_file():
    list_of_files = glob.glob(BACKUP_PATH + "\\*.json")
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def restore_last_backup():
    global running_p
    if running_p:
        os.chdir(ROOT_PATH)
        latest_file_path = get_latest_file()
        latest_file_name = latest_file_path.split("\\")[-1]
        print("restoring from",latest_file_name)
        subprocess.run(["docker-compose","exec", "backend", "python", "manage.py", "loaddata", "data_backup/%s"%latest_file_name], shell=True)
        print("\Restore complete!")
    else:
        print("Please run the application first.")
    
def update():
    if running_p:
        print("Stop the application using CTRL + C before updating..")
        return
    print("Updating application...")
    os.chdir(ROOT_PATH)
    subprocess.run(['git','pull'])
    os.chdir("BOB-Backend")
    subprocess.run(['git','pull'])
    os.chdir(ROOT_PATH)
    os.chdir("BOB-Frontend")
    subprocess.run(['git','pull'])
    os.chdir(ROOT_PATH)
    subprocess.run(['docker-compose','build'])
    print("Update completed!")



window = Tk()
window.title("BOB Application")

window.geometry("400x50")

frame = Frame(window)
frame.pack()

button_1 = Button(frame,text="Run", width=10,command=run)
button_1.pack(side=LEFT)

button_2 = Button(frame,text="Update", width=10,command=update)
button_2.pack(side=LEFT)

button_3 = Button(frame,text="Backup", width=10,command=take_backup)
button_3.pack(side=LEFT)

button_4 = Button(frame,text="Restore", width=10,command=restore_last_backup)
button_4.pack(side=LEFT)

window.mainloop()