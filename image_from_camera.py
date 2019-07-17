import tkinter as tk
from PIL import ImageTk,Image
import cv2

counter = 0

def captureVideo():
    global camera_img
    global video_source
    global camera_panel
    global counter
    print("Hey you are in the begining")
    print("Catching video")
    counter += 1
    while 1 == 1:
        ret,frame = video_source.read()
        print("Estatus: {}".format(ret))
        camera_tmp_img = Image.fromarray(frame)
        camera_img = ImageTk.PhotoImage(camera_tmp_img)
        camera_panel.config(image=camera_img)
        camera_window.update()
        
        if counter == 2:
            break



#Setup cv2 video capture
video_source = cv2.VideoCapture(0)

#Window setup
camera_window = tk.Tk()
camera_window.title("Geting images from cammera")
camera_window.geometry("600x600")
camera_window.config(bg="#fff")

#Btn Capture setup
btn_capture = tk.Button(camera_window,text="Capture")
btn_capture.place(x=200,y=40,height=60,width=200)
btn_capture.config(bg="#151820",fg="#fff",font=("Open Sans",16),command=captureVideo,relief=tk.RAISED,cursor='hand2')

#Camera image panel setup
camera_panel = tk.Label(camera_window)
camera_panel.place(x=100,y=190,height=400,width=400)
camera_img = None
camera_window.mainloop()