# import if libraries
from tkinter import *
from PIL import ImageTk, Image
import csv
import pandas as pd
import io
from tkhtmlview import HTMLLabel
import numpy as np
import seaborn as sns
from tkinter import ttk
import tkinter.font as tkFont

import importlib
import wind2_bis,wind1_bis


importlib.reload(wind2_bis) #last version of wind2_bis
importlib.reload(wind1_bis) #last version of wind1_bis

#creation of a window
root=Tk()

#we give a title for the window, a size by default and a background color also
root.title("Interface for clinician")
root.geometry("1200x700")
root.configure(bg="#CAD0DA")

#avoid to write it always
link ='C:\\Users\\User\\Documents\\Stage_4A_Vanessa\\Interface\\Images'
logo = link + '\\openBCI.ico'


#we add a other logo (here that of the openBCI)
image = root.iconbitmap(logo)

# We open the image for the home page with our specific size and we load it
image = Image.open(link + "\\banniere.png")
image = image.resize((1200, 600))
my_img = ImageTk.PhotoImage(image)
my_label = Label(root, image=my_img)
my_label.pack()


#next step : we create the button which call window1 when we click 
bold_font = tkFont.Font(weight="bold")
b1 = Button(root, text="Click to see the raw data ", command= lambda : wind1_bis.window_1(),font=bold_font)
b1.place(x=200, y=650)

#we create a second button which call window2 when we click 
b2 = Button(root, text="Click to see the data after the ASR ", command= lambda : wind2_bis.window_2(),font=bold_font)
# we also place the button where we want
b2.place(x=710, y=650)


root.mainloop()