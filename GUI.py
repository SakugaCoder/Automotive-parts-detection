#Main libraries
import tkinter as tk
from PIL import ImageTk, Image
import os
import time
import cv2
import numpy as np
import tensorflow as tf
import random
import information_window
from datetime import datetime

#Model variables
model = tf.keras.models.load_model("parts_detection_model.h5")
clases = ['bateria','bujia','piston','radiador']
accuracy = 0.0
correct_predictions = 0
total_predictions = 0

#Main variables
correct_prediction = True
incorrect_prediction = False
actual_result_image = correct_prediction

video_source = cv2.VideoCapture(0)
mfb_functions = ['STOP','RECORD','CAPTURE']
mfb_function = mfb_functions[0]
start_record = False
counter = 0
img_size = 48


#Change the text of the textvar of the information frame

def completNumber(num):
	if num < 9:
		str_num = '0'+str(num)
		return str_num
	else:
		return str(num)


def changePiceInfo(piece):
    global info_title
    global info_description
    global info_material
    global info_price

    #Battery
    if piece == 0:
        info_title.set("Battery")
        info_description.set("Used to supply the auto's system")
        info_material.set("Plastic, lithhium")
        info_price.set("400 MXN - 4000 MXN")

    #Spark plug
    elif piece == 1:
        info_title.set("Spark plug")
        info_description.set("Used to frezee the motor")
        info_material.set("Plastic, aluminium")
        info_price.set("40 MXN - 600 MXN")

    #Piston
    elif piece == 2:
        info_title.set("Piston")
        info_description.set("Is one of the motor's main parts")
        info_material.set("Aluminium")
        info_price.set("120 MXN - 1350 MXN")

    #Radiador
    elif piece == 3:
        info_title.set("Radiador")
        info_description.set("Used to cool the system")
        info_material.set("Metal, aluminium")
        info_price.set("1200 MXN - 8000 MXN")

    window.update()

def changeSource():
    global pc_source_mode
    global btnMF
    if pc_source_mode.get() == 1:
        btnMF.config(state="disabled")

    else:
        btnMF.config(state="normal")
    window.update()

def changeMode():
    global btnPredict
    global mfb_functions
    global mfb_function
    global radio_btn
    global radio_btn_simg
    global radio_btn_folder
    global cc_mode
    global radio_btn_camera_img
    global radio_btn_camera_video

    #If folder option is selected
    if source.get() == 0:
        radio_btn_simg.config(state='normal')
        radio_btn_folder.config(state='normal')
        btnMF.config(text="STOP")
        mfb_function = mfb_functions[0]
        btnPredict.config(state='normal')
        btnMF.config(state='normal')
        radio_btn_camera_img.config(state='disabled')
        radio_btn_camera_video.config(state='disabled')

    #if camera option is selected
    elif source.get() == 1:
        radio_btn_simg.config(state='disabled')
        radio_btn_folder.config(state='disabled')
        btnMF.config(text="RECORD")
        mfb_function = mfb_functions[1]
        btnPredict.config(state='disabled')
        btnMF.config(state='normal')
        radio_btn_camera_img.config(state='normal')
        radio_btn_camera_video.config(state='normal')

def mfbAcction():
    global stop
    global mfb_functions
    global mfb_function
    global start_record
    global panel_b
    global white_img
    global cc_mode

    if mfb_function == 'STOP' and stop == False:
        stop = True
        btnMF.config(text="STOP")
        print("Process has been canceled")
    elif mfb_function == 'RECORD':
        start_record = True
        mfb_function = mfb_functions[2]
        if cc_mode.get() == 1:
            btnMF.config(text='STOP')
        else:
            btnMF.config(text='CAPTURE')
        panel_b.config(image=white_img)
        print("Starting to capture img")
        getImgURL()
    elif mfb_function == 'CAPTURE':
        mfb_function = mfb_functions[1]
        start_record = False
        btnMF.config(text="RECORD")
        print("Getting image")

def getImgURL():
    global counter
    global panel_a_img
    global panel_b_img
    global img_size
    global source
    global accuracy
    global correct_predictions
    global total_predictions
    global stop
    global pc_source_mode
    global delay_entry

    delay = float(delay_entry.get())

    if counter == 0:
        panel_a.config(bg='#fff')
        panel_b.config(bg='#fff')
        counter += 1
    print(entryImgURL.get())
    main_directory = entryImgURL.get()

    if source.get() == 0:
        if pc_source_mode.get() == 0:
            print("Mode: Folder")
            stop = False
            for img in os.listdir(main_directory):
                if stop:
                    break
                total_predictions += 1
                directory = main_directory+"/"+img
                print(directory)
                panel_a_tmp_img = cv2.imread(directory,cv2.IMREAD_GRAYSCALE)
                panel_a_tmp_img = cv2.resize(panel_a_tmp_img,(280,250))
                panel_a_img = transformImg(panel_a_tmp_img)
                panel_a.config(image=panel_a_img)


                #getting prediction from imported model
                input_image_tmp = cv2.imread(directory,cv2.IMREAD_GRAYSCALE)
                input_image_tmp = cv2.resize(input_image_tmp,(img_size,img_size))
                input_image = np.array(input_image_tmp)
                input_image = np.expand_dims(input_image,2)
                input_image = np.expand_dims(input_image,0)

                predict_piece(input_image,0,dir)
        
                time.sleep(delay)
                window.update()
        elif pc_source_mode.get() == 1:
            print("Mode single image")
            panel_a_tmp_img = cv2.imread(main_directory,cv2.IMREAD_GRAYSCALE)
            panel_a_tmp_img = cv2.resize(panel_a_tmp_img,(280,250))
            panel_a_img = transformImg(panel_a_tmp_img)
            panel_a.config(image=panel_a_img)


            #getting prediction from imported model
            input_image_tmp = cv2.imread(main_directory,cv2.IMREAD_GRAYSCALE)
            input_image_tmp = cv2.resize(input_image_tmp,(img_size,img_size))
            input_image = np.array(input_image_tmp)
            input_image = np.expand_dims(input_image,2)
            input_image = np.expand_dims(input_image,0)

            predict_piece(input_image,0,dir)
    
            time.sleep(delay)
            window.update()
    elif source.get() == 1:
        print("Mode: Camera")
        captureVideo()

def transformImg(image):
    global panel_a
    ti = Image.fromarray(image)
    real_img = ImageTk.PhotoImage(ti)
    return real_img

def captureVideo():
    global camera_img
    global video_source
    global panel_a_img
    global img_size
    global result_panel
    global accuracy_label
    global start_record

    global info_title
    global info_description
    global info_material
    global info_price
    global cc_mode

    result_panel.config(image=white_img)
    accuracy_label.config(text=" ")
    print("Hey you are in the begining")
    print("Catching video")

    info_title.set("Piece name")
    info_description.set("")
    info_material.set("")
    info_price.set("")
    input_image = None
    frame = None



    while start_record:
        ret,frame = video_source.read(cv2.IMREAD_GRAYSCALE)

        print("Estatus: {}".format(ret))
        camera_tmp_img = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        camera_img = ImageTk.PhotoImage(camera_tmp_img)
        panel_a.config(image=camera_img)

        input_image_tmp = cv2.resize(frame,(img_size,img_size))
        input_image_tmp = cv2.cvtColor(input_image_tmp,cv2.COLOR_BGR2GRAY)
        input_image = np.array(input_image_tmp)
        input_image = np.expand_dims(input_image,2)
        input_image = np.expand_dims(input_image,0)
        print(input_image.shape)
        if cc_mode.get() == 1:
            predict_piece(input_image,1,None)
        window.update()



    if cc_mode.get() == 0:
        actual_datetime = datetime.now()
        year = completNumber(actual_datetime.year)
        month= completNumber(actual_datetime.month)
        day = completNumber(actual_datetime.day)

        hour = completNumber(actual_datetime.hour)
        minute = completNumber(actual_datetime.minute)
        second = completNumber(actual_datetime.second)
        microsecond = str(actual_datetime.microsecond)
        
        str_datetime = year+month+day+'_'+hour+minute+second+'_'+microsecond
        print(str_datetime)
        img_name = "Images/Saved/CAPTURE{}.jpg".format(str_datetime)
        cv2.imwrite(img_name,frame)
        predict_piece(input_image,1,None)

def predict_piece(input_image,source,dir=None):
    global accuracy
    global correct_predictions
    global total_predictions
    global panel_b_img 
    global accuracy_label
    global result_panel

    prediction_results = model.predict(input_image)
    prediction_label = clases[np.argmax(prediction_results)]
    print("Prediction results:")
    print(prediction_results*100)
    print("Image label: {}".format(prediction_label))

    """
    if prediction_label == dir and source == 0:
        print("Predicción correcta")
        result_panel.config(image=ok_img)
        correct_predictions += 1
    elif  not (prediction_label == dir) and source == 0:
        print("Predicción erronea")
        result_panel.config(image=error_img)

    if correct_predictions == 0:
        accuracy = 0
    else:
        accuracy = (correct_predictions / total_predictions) * 100
    accuracy_str = "Accuracy: "+str(accuracy)+"%"
    accuracy_str_var = tk.StringVar(window,value=accuracy_str)
    """
    blank_str_var = tk.StringVar(window,value=" ")
    class_n1_label_str = "Class 'battery' prob: "+str((prediction_results[0][0]*100))+"%"
    class_n1_label_str_var = tk.StringVar(window,value=class_n1_label_str)

    class_n2_label_str = "Class 'spark plug' prob: "+str((prediction_results[0][1]*100))+"%"
    class_n2_label_str_var = tk.StringVar(window,value=class_n2_label_str)

    class_n3_label_str = "Class 'piston' prob: "+str((prediction_results[0][2]*100))+"%"
    class_n3_label_str_var = tk.StringVar(window,value=class_n3_label_str)

    class_n4_label_str = "Class 'radiador' prob: "+str((prediction_results[0][3]*100))+"%"
    class_n4_label_str_var = tk.StringVar(window,value=class_n4_label_str)
    """
    if source == 0:
        accuracy_label.config(textvariable=accuracy_str_var)
    else:
    """
    accuracy_label.config(textvariable=blank_str_var) # <- Tab
    class_n1_label.config(textvariable=class_n1_label_str_var)
    class_n2_label.config(textvariable=class_n2_label_str_var)
    class_n3_label.config(textvariable=class_n3_label_str_var)
    class_n4_label.config(textvariable=class_n4_label_str_var)
    panel_b_img_dir = 'Images/Clases/'+prediction_label+'.jpg'
    panel_b_tmp_img = cv2.imread(panel_b_img_dir,cv2.IMREAD_GRAYSCALE)
    panel_b_tmp_img = cv2.resize(panel_b_tmp_img,(280,250))
    #panel_b_tmp_img = cv2.cvtColor(panel_b_tmp_img,cv2.COLOR_BGR2RGB)
    panel_b_img = transformImg(panel_b_tmp_img)
    panel_b.config(image=panel_b_img)

    #Change piece info
    changePiceInfo(np.argmax(prediction_results))


#Creating a no resizable window of 900 x 600 px
window = tk.Tk()
window.title("Automotive Parts Detection")
window.geometry("1300x600")
window.config(bg="#fff")
window.resizable(0,0)

#Create the main title
titleStr = tk.StringVar(window,value="Automotive Parts Detection")
title = tk.Label(window,textvar=titleStr,bg="#fff",fg="#000", font=('Open Sans',20))
title.pack()

#Create images folder entry
strEntryImgURL = tk.StringVar(window,value="Images/Rapid test")
entryImgURL = tk.Entry(window,textvariable=strEntryImgURL,bd=2,font=("Open Sans", 16),justify="center",selectborderwidth=2)
entryImgURL.place(x=300,y=100,height=50,width=300)

#Radio buttons for egine selector
source = tk.IntVar()
radio_btn_pc = tk.Radiobutton(window,text="PC",font=("Open Sans bold",10),variable=source,value=0,bg="#fff",command=changeMode)
radio_btn_camera = tk.Radiobutton(window,text="Camera",font=("Open Sans",10),variable=source,value=1,bg="#fff",command=changeMode)
radio_btn_pc.place(x=10,y=30)
radio_btn_camera.place(x=10,y=50)

#Radio buttons for pc modes
pc_source_mode = tk.IntVar()
radio_btn_folder = tk.Radiobutton(window,text="Folder",font=("Open Sans",10),variable=pc_source_mode,value=0,bg="#fff",command=changeSource)
radio_btn_simg = tk.Radiobutton(window,text="Single image",font=("Open Sans",10),variable=pc_source_mode,value=1,bg="#fff",command=changeSource)
radio_btn_folder.place(x=10,y=80)
radio_btn_simg.place(x=10,y=100)


#Radio buttons for camera capture modes
cc_mode = tk.IntVar()
radio_btn_camera_img = tk.Radiobutton(window,text="Photo",font=("Open Sans",10),variable=cc_mode,value=0,bg="#fff")
radio_btn_camera_video = tk.Radiobutton(window,text="Video",font=("Open Sans",10),variable=cc_mode,value=1,bg="#fff")
radio_btn_camera_img.place(x=120,y=80)
radio_btn_camera_video.place(x=120,y=100)
radio_btn_camera_img.config(state='disabled')
radio_btn_camera_video.config(state='disabled')

#Entry for prediction results delay
dsv = tk.StringVar(window,value="1")
delay_entry_label = tk.Label(window,text="Delay:",bg="#fff",font=("Open Sans",10))
delay_entry_label.place(x=10,y=140)
delay_entry= tk.Entry(window,bg="#fff",bd=1,justify="center",textvariable=dsv)
delay_entry.place(x=60,y=145,height=20,width=50)

#Create btn Predict
btnPredict = tk.Button(window,text="PREDICT")
btnPredict.config(bg="#5041f4",fg="#fff",font=("Open Sans",14),bd=0,relief=tk.RAISED,cursor='hand2',command=getImgURL)
btnPredict.place(x=310,y=200,height=40,width=280)

#Create btn stop
btnMF = tk.Button(window,text="STOP")
btnMF.config(bg="#f44242",fg="#fff",font=("Open Sans",12),bd=0,relief=tk.RAISED,cursor="hand2",command=mfbAcction)
btnMF.place(x=370,y=250,height=30,width=150)
stop = None

#Create main image pannels
camera_img = None
panel_a_tmp_img = Image.open("ok.jpg")
panel_a_tmp_img = panel_a_tmp_img.resize((250,250),Image.ANTIALIAS)
panel_a_img = ImageTk.PhotoImage(panel_a_tmp_img)

panel_a = tk.Label(window)
panel_a.place(x=20,y=300,height=280,width=250)
panel_a_label = tk.Label(window,text="Real image")
panel_a_label.config(font=("Open Sans",12),bg="#fff")
panel_a_label.place(x=100,y=270)

panel_b_tmp_img = Image.open("error.jpg")
panel_b_tmp_img = panel_b_tmp_img.resize((250,250),Image.ANTIALIAS)
panel_b_img = ImageTk.PhotoImage(panel_b_tmp_img)

panel_b = tk.Label(window)
panel_b.place(x=630,y=300,height=280,width=250)
panel_b_label = tk.Label(window,text="Prediction")
panel_b_label.config(font=("Open Sans",12),bg="#fff")
panel_b_label.place(x=710,y=270)

#Create the result image
ok_tmp_img = Image.open("ok.jpg")
#ok_tmp_img = ok_tmp_img.resize((96,96),Image.ANTIALIAS)
ok_img = ImageTk.PhotoImage(ok_tmp_img)

error_tmp_img = Image.open("error.jpg")
error_img = ImageTk.PhotoImage(error_tmp_img)

white_tmp_img = Image.open("white.jpg")
white_img = ImageTk.PhotoImage(white_tmp_img)

result_panel = tk.Label(window,bg='#fff')
result_panel.place(x=402,y=380,height=96,width=96)


#Create prediction lables
class_n1_label = tk.Label(window,text="Class 'battery' prob: 0%")
class_n2_label = tk.Label(window,text="Class 'spark plug' prob: 0%")
class_n3_label = tk.Label(window,text="Class 'piston' prob: 0%")
class_n4_label = tk.Label(window,text="Class 'radiador' prob: 0%")

class_n1_label.place(x=340,y=400)
class_n1_label.config(bg="#fff",font=('Open Sans',10))
class_n2_label.place(x=340,y=420)
class_n2_label.config(bg="#fff",font=('Open Sans',10))
class_n3_label.place(x=340,y=440)
class_n3_label.config(bg="#fff",font=('Open Sans',10))
class_n4_label.place(x=340,y=460)
class_n4_label.config(bg="#fff",font=('Open Sans',10))

#Accuracy label
accuracy_label = tk.Label(window,text="",font=('Open Sans',11))
accuracy_label.config(bg="#fff")
accuracy_label.place(x=350,y=575)


#Bar separator
bar_tmp_img = Image.open("vertical_separator.png")
bar_img = ImageTk.PhotoImage(bar_tmp_img)
bar_label = tk.Label(window,image=bar_img)
bar_label.place(x=905,y=50,height=500,width=10)

#Information frame
info_window = tk.Frame(window,bg="#fff")
info_window.config(bd=2)
info_window.place(x=912,y=100,height=400,width=430)

def startMap():
    print("Starting map")
    os.system("parts_location_tomtom.html")


#String variables
info_title = tk.StringVar(info_window,value="Pice name")
info_description = tk.StringVar(info_window,value="")
info_material =  tk.StringVar(info_window,value="")
info_price = tk.StringVar(info_window,value="")


info_title_label = tk.Label(info_window,textvariable=info_title,font=("Open Sans",14),bg="#fff")
info_title_label.pack()

description_label = tk.Label(info_window,text="Description:",font=("Open Sans bold",12),bg="#fff")
description_label.place(x=10,y=100)
description_label_content = tk.Label(info_window,textvariable=info_description,font=("Open Sans",10),bg="#fff")
description_label_content.place(x=130,y=100)

material_label = tk.Label(info_window,text="Material(s):",font=("Open Sans bold",12),bg="#fff")
material_label.place(x=10,y=130)
material_label_content = tk.Label(info_window,textvariable=info_material,font=("Open Sans",10),bg="#fff")
material_label_content.place(x=130,y=130)

price_label = tk.Label(info_window,text="Price:",font=("Open Sans bold",12),bg="#fff")
price_label.place(x=10,y=160)
price_label_content = tk.Label(info_window,textvariable=info_price,font=("Open Sans",10),bg="#fff")
price_label_content.place(x=130,y=160)

shopping_label = tk.Label(info_window,text="Shops:",font=("Open Sans bold",12),bg="#fff")
shopping_label.place(x=140,y=230)

shopping_tmp_img_a = cv2.imread('internet.png',cv2.IMREAD_GRAYSCALE)
shopping_tmp_img_a = cv2.resize(shopping_tmp_img_a,(50,50))
shopping_tmp_img = Image.fromarray(shopping_tmp_img_a)
shopping_img = ImageTk.PhotoImage(shopping_tmp_img)

shopping_icon = tk.Button(info_window,image=shopping_img,bg="#fff",cursor="hand2",relief=tk.RAISED,command=startMap) 
shopping_icon.place(x=230,y=220)

window.mainloop()