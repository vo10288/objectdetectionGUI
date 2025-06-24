#!/opt/virtualenv/computer_vision/bin/python3

# 20250515
# https://tsurugi-linux.org
# by Visi@n

# GRAPHIC INTERFACE  

# LICENSE
# THIS SCRIPT USE FACE_RECOGNITION LIBRARY [https://github.com/ageitgey/face_recognition/blob/master/LICENSE]
# THIS SCRIPT HAS BEEN MODIFIED BY Antonio 'Visi@n' Broi [antonio@tsurugi-linux.org] and it's licensed under the MIT License
# Special thanks to Adam Ageitgey [https://adamgeitgey.com] the creator of face_recognition and to all Python community

from datetime import datetime
from os import listdir
from os.path import isdir, join, isfile, splitext
from  tkinter import *
#import tkinter, Tkconstants, tkFileDialog
import tkinter
from tkinter import filedialog
from tkinter import constants
import tkinter as tk
import sys
import os
import subprocess
from datetime import datetime
from openalpr import Alpr

resolution = 1024

def killobjectdetectionwebcam():
	global killobjectdetectionwebcam
	command = "kill -9 `ps aux | grep '/opt/computer_vision/object_detection_live.py'|awk '{print $2}'`"
	subprocess.Popen(command, shell=True)

def objectdetectionwebcam():
	global objectdetectionwebcam
	command = ('/opt/computer_vision/object_detection_live.py')
	subprocess.Popen(command, shell=True)

def inputvideo():
	global inputvideo
	inputvideo = tkinter.filedialog.asksaveasfilename(initialdir = "~/02.computer_vision/",title = "Select file",filetypes = (("all files","*.*"),("all files","*.avi")))
	print (inputvideo)

def objectdetectionvideo():
	global objectdetectionvideo
	command = ('/opt/computer_vision/object_detection_video.py -v '+inputvideo+' -r '+str(resolution))
	subprocess.Popen(command, shell=True)

def killobjectdetectionvideo():
	global killobjectdetectionvideo
	command = "kill -9 `ps aux | grep '/opt/computer_vision/object_detection_video.py'|awk '{print $2}'`"
	subprocess.Popen(command, shell=True)

def outputvideo():
	global outputvideo
	outputvideo = tkinter.filedialog.asksaveasfilename(initialdir = "~/02.computer_vision/",title = "Select file",filetypes = (("all files","*.*"),("all files","*.avi")))
	print (inputvideo)

def objectdetectionvideowritevideo():
	global objectdetectionvideowritevideo
	command = ('/opt/computer_vision/object_detection_video_write_video.py -v '+inputvideo+' -o '+outputvideo)
	subprocess.Popen(command, shell=True)

def killobjectdetectionvideowritevideo():
	global killobjectdetectionvideowritevideo
	command = "kill -9 `ps aux | grep '/opt/computer_vision/object_detection_video_write_video.py'|awk '{print $2}'`"
	subprocess.Popen(command, shell=True)

def objectdetectionwebcamwritevideo():
	global objectdetectionwebcamwritevideo
	command = ('/opt/computer_vision/object_detection_live_write_video.py -o '+outputvideo+' -r '+str(resolution))
	subprocess.Popen(command, shell=True)

def killobjectdetectionwebcamwritevideo():
	global killobjectdetectionwebcamwritevideo
	command = "kill -9 `ps aux | grep '/opt/computer_vision/object_detection_live_write_video.py'|awk '{print $2}'`"
	subprocess.Popen(command, shell=True)

#####################################

def res():
	global res
	global resolution
	resolution = input('insert the correct width resolution of video \n resolution : ')
	#resolution = str(resolution)
	print('the width resolution now is:'+  str(resolution) + '\n' + str(type(resolution)))


def openalprCARS():
	global openalpr
	os.chdir(os.path.expanduser('~/02.computer_vision/03.reports'))

	filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

	if not os.path.exists('CARS_ALPR'+'_'+filename):
		os.makedirs('CARS_ALPR'+'_'+filename)

	path = ("CARS/")

	filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


	files = os.listdir(path)
	print (files)

	for file in files:
		print (path+'/'+file)

		command = 'alpr -c eu '+path+'/'+file
		subprocess.Popen(command, shell=True)

		command = 'echo '+path+'/'+file+'\n > CARS_ALPR_'+filename+'/'+str(file)+'.csv'
		subprocess.Popen(command, shell=True)	
		command = 'alpr -c eu '+path+'/'+file+' > CARS_ALPR_'+filename+'/'+str(file)+'.csv'
		subprocess.Popen(command, shell=True)

		command = 'echo '+path+'/'+file+'\n >> CARS_ALPR_'+filename+'/'+'ALL.csv'
		subprocess.Popen(command, shell=True)	
		command = 'alpr -c eu '+path+'/'+file+' >> CARS_ALPR_'+filename+'/'+'ALL.csv'
		subprocess.Popen(command, shell=True)

from openalpr import Alpr

def openalpr_python(mode="ALL"):
    folder_path = os.path.expanduser(f"~/02.computer_vision/{mode}/")
    report_dir = os.path.expanduser(f"~/02.computer_vision/03.reports/{mode}_ALPR_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
    os.makedirs(report_dir, exist_ok=True)

    alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
    if not alpr.is_loaded():
        print("Errore: OpenALPR non caricato correttamente.")
        return

    all_results = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not os.path.isfile(file_path):
            continue

        with open(file_path, "rb") as image_file:
            image_data = image_file.read()
            results = alpr.recognize_array(image_data)
            output_file = os.path.join(report_dir, filename + ".csv")
            with open(output_file, "w") as f:
                f.write(f"File: {filename}\n")
                for plate in results['plates']:
                    f.write(f"{plate['characters']}, Confidence: {plate['overall_confidence']}\n")
                    all_results.append(f"{filename},{plate['characters']},{plate['overall_confidence']}")

    # Salva riepilogo generale
    all_csv = os.path.join(report_dir, "ALL.csv")
    with open(all_csv, "w") as f:
        f.write("Filename,Plate,Confidence\n")
        f.writelines("\n".join(all_results))

    alpr.unload()
    print(f"[OK] Riconoscimento completato. Report in: {report_dir}")

####################################

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()
root.wm_title("Object Detection")
root.geometry("350x670")

label = tk.Label(text=".      Object Detection Video files & realtime    .",
				fg="red",
				font=("helvetica",12),
					)
label.pack(ipadx=15, ipady=4, pady=15, padx=10)
label.place(x=0, y=0)

button = tk.Button(frame, 
					text="QUIT",
					fg="#ffffff",
					bg="#000000",
					command=quit)
button.pack(ipadx=125, ipady=4, pady=25)

slogan = tk.Button(frame,
					text="OBJECT DETECTION WEBCAM",
					fg="#ffffff",
					bg="#ff0000",
					command=objectdetectionwebcam)
slogan.pack(ipadx=46, ipady=4, pady=1)

slogan = tk.Button(frame,
					text="KILL O.D.W.",
					fg="#ffffff",
					bg="#000000",
					command=killobjectdetectionwebcam)
slogan.pack(ipadx=104, ipady=4, pady=1)

slogan = tk.Button(frame,
					text="INPUT VIDEO",
					fg="#ffffff",
					bg="#0000ff",
					command=inputvideo)
slogan.pack(ipadx=99, ipady=4, pady=1)

#####################################
slogan = tk.Button(frame,
					text="WIDTH RES",
					fg="#ffffff",
					bg="#000000",
					command=res)
slogan.pack(ipadx=104, ipady=4, pady=1)

#####################################

slogan = tk.Button(frame,
					text="OBJECT DETECTION VIDEO",
					fg="#ffffff",
					bg="#ff0000",
					command=objectdetectionvideo)
slogan.pack(ipadx=55, ipady=4, pady=1)

slogan = tk.Button(frame,
					text="KILL O.D.V.",
					fg="#ffffff",
					bg="#000000",
					command=killobjectdetectionvideo)
slogan.pack(ipadx=104, ipady=4, pady=1)

slogan = tk.Button(frame,
					text="OUTPUT VIDEO",
					fg="#ffffff",
					bg="#0000ff",
					command=outputvideo)
slogan.pack(ipadx=90, ipady=4, pady=1)

slogan = tk.Button(frame,
					text="OBJECT DETECTION VIDEO WRITING VIDEO",
					fg="#ffffff",
					bg="#ff0000",
					command=objectdetectionvideowritevideo)
slogan.pack(ipadx=2, ipady=4, pady=1)

slogan = tk.Button(frame,
					text="KILL O.D.V.W.V",
					fg="#ffffff",
					bg="#000000",
					command=killobjectdetectionvideowritevideo)
slogan.pack(ipadx=92, ipady=4, pady=1)

slogan = tk.Button(frame,
					text="OBJECT DETEC WEBCAM WRITING VIDEO",
					fg="#ffffff",
					bg="#ff0000",
					command=objectdetectionwebcamwritevideo)
slogan.pack(ipadx=6, ipady=4, pady=1)

slogan = tk.Button(frame,
					text="KILL O.D.W.W.V",
					fg="#ffffff",
					bg="#000000",
					command=killobjectdetectionwebcamwritevideo)
slogan.pack(ipadx=89, ipady=4, pady=1)

slogan = tk.Button(frame,
    text="OPENALPR CARS",
    fg="#000000",
    bg="#ffffff",
    command=lambda: openalpr_python("CARS"))
slogan.pack(ipadx=85, ipady=4, pady=1)

slogan = tk.Button(frame,
    text="OPENALPR ALL",
    fg="#000000",
    bg="#ffffff",
    command=lambda: openalpr_python("ALL"))
slogan.pack(ipadx=89, ipady=4, pady=1)


label = tk.Label(text="Visi@n",
				fg="red",
				font=("helvetica",12),
					)
label.pack(ipadx=15, ipady=4, pady=15, padx=10)
label.place(x=290, y=640)

root.mainloop()
