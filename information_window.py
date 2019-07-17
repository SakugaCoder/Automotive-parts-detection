import tkinter as tk
from PIL import ImageTk,Image
import cv2
import os



def startMap():
    print("Starting map")
    os.system("parts_location_tomtom.html")


def main(piece):
    #Window setup
    info_window = tk.Tk()
    info_window.resizable(0,0)
    info_window.geometry("500x400")
    info_window.title("Piece information window")
    info_window.config(bg="#fff")
    #String variables
    title = tk.StringVar(info_window,value="Piston")
    description = tk.StringVar(info_window,value="The piston is the one of the motor's main parts")
    material =  tk.StringVar(info_window,value="Copper, aluminium")
    price = tk.StringVar(info_window,value="120 MXN - 1350 MXN")

    title_label = tk.Label(info_window,textvariable=title,font=("Open Sans",16),bg="#fff")
    title_label.pack()

    description_label = tk.Label(info_window,text="Description:",font=("Open Sans bold",14),bg="#fff")
    description_label.place(x=10,y=100)
    description_label_content = tk.Label(info_window,textvariable=description,font=("Open Sans",12),bg="#fff")
    description_label_content.place(x=130,y=100)

    material_label = tk.Label(info_window,text="Material(s):",font=("Open Sans bold",14),bg="#fff")
    material_label.place(x=10,y=130)
    material_label_content = tk.Label(info_window,textvariable=material,font=("Open Sans",12),bg="#fff")
    material_label_content.place(x=130,y=130)

    price_label = tk.Label(info_window,text="Price:",font=("Open Sans bold",14),bg="#fff")
    price_label.place(x=10,y=160)
    price_label_content = tk.Label(info_window,textvariable=price,font=("Open Sans",12),bg="#fff")
    price_label_content.place(x=130,y=160)

    shopping_label = tk.Label(info_window,text="Shops:",font=("Open Sans bold",14),bg="#fff")
    shopping_label.place(x=140,y=230)

    shopping_tmp_img_a = cv2.imread('internet.png',cv2.IMREAD_GRAYSCALE)
    shopping_tmp_img_a = cv2.resize(shopping_tmp_img_a,(50,50))
    shopping_tmp_img = Image.fromarray(shopping_tmp_img_a)
    shopping_img = ImageTk.PhotoImage(shopping_tmp_img)

    shopping_icon = tk.Button(info_window,image=shopping_img,bg="#fff",cursor="hand2",relief=tk.RAISED,command=startMap) 
    shopping_icon.place(x=230,y=220)
    info_window.update()
