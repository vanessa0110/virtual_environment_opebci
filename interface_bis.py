# import if libraries
from tkinter import *
from PIL import ImageTk, Image
import csv
import pandas as pd
import io
from tkhtmlview import HTMLLabel
from tkinter import ttk
import tkinter.font as tkFont
import numpy as np
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import importlib
import wind2_bis,wind1_bis
import splite_task

importlib.reload(splite_task) #last version of splite_task
splite_task.splite_data_create_variables()
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


# ----------------------------------------- Create liste with all 10 secondes for each variable ------------
liste_oe1 = []
for i in range(13):
    liste_oe1.append(eval(f"splite_task.oe1_{i}_df"))
    
liste_ce = []
for i in range(13):
    liste_ce.append(eval(f"splite_task.ce_{i}_df"))
    
liste_it1 = []
for i in range(32):
    liste_it1.append(eval(f"splite_task.it1_{i}_df"))
    
liste_p2 = []
for i in range(13):
    liste_p2.append(eval(f"splite_task.p2_{i}_df"))
    
liste_it2 = []
for i in range(32):
    liste_it2.append(eval(f"splite_task.it2_{i}_df"))
    
liste_p3 = []
for i in range(2):
    liste_p3.append(eval(f"splite_task.p3_{i}_df"))
    
liste_oe2 = []
for i in range(13):
    liste_oe2.append(eval(f"splite_task.oe2_{i}_df"))
    # ----------------------------------------------------------------------------------------------------------

list = [splite_task.start, liste_oe1, liste_ce, splite_task.pause_1, liste_it1, liste_p2, liste_it2, liste_p3, liste_oe2]

# ------------------------- We create a menu where people can select the task they want to see ----------------------------------------------
# Create a general function to plot data and vertical lines, it's better
def call_plot(value, mini, maxi):
    win1 = wind1_bis.window_1()
    plot_function = win1[0]
    vertical_lines_function = win1[1]
    plot_function(value)
    ax = plt.gca()
    vertical_lines_function(ax, mini, maxi)
        
    
# Function which calculate min and  max
def min_max(value):
    mini = value.index.min()
    maxi = value.index.max()
    return mini, maxi


# Function to plot data more efficient because all the data are in a list
def callback_general(j):
    i = 0
    value = (list[j])[i]
    mini,maxi = min_max(value)
    call_plot(value, mini, maxi)
    #i = i+1#value_of_i(list[j],i, next_value)
    #update_plot(j)

# update graph when we click on the button
def update_plot(j):
    #i = value_of_i(list[j])
    value = (list[j])[i]
    mini,maxi = min_max(value)
    call_plot(value, mini, maxi)
     
    
# Function for the value of i 
next_value = 1
def value_of_i(liste,i,next_value):
    i = i + 1
    if ((i < len(liste)) and (next_value == 1)):
        return i
    
    

# Call this function if we select a task   
def option_callback(option):
    if option == "Start":
        value = splite_task.start
        mini = 0
        maxi = value.index.max()
        call_plot(value, mini, maxi)
    elif option == "Open_eyes_1":
        callback_general(1)
    elif option == "Close_eyes":
        callback_general(2)
    elif option == "Break_1":
        value = list[3]
        mini,maxi = min_max(value)
        call_plot(value, mini, maxi)
    elif option == "IMG_TASK_1":
        callback_general(4)
    elif option == "Break_2":
        callback_general(5)
    elif option == "IMG_TASK_2":
        callback_general(6)
    elif option == "Break_3":
        callback_general(7)
    elif option == "Open_eyes_2":
        callback_general(8)
        
# We create the menu
bold_font = tkFont.Font(weight="bold")
clicked = StringVar()
clicked.set("Click to see the raw data")
options= ["Start","Open_eyes_1", "Close_eyes", "Break_1", "IMG_TASK_1","Break_2","IMG_TASK_2","Break_3","Open_eyes_2"]
drop = OptionMenu(root, clicked, *options, command=lambda option: option_callback(option))
drop.configure(font=bold_font)
drop.place(x=200,y=650)
# -------------------------------------------------------------------------------------------------------------------------------------------


# we create a second button which call window2 when we click 
b2 = Button(root, text="Click to see the data after the ASR ", command= lambda : wind2_bis.window_2(),font=bold_font)
# we also place the button where we want
b2.place(x=710, y=650)


root.mainloop()