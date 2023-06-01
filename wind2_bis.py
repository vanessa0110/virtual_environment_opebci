# import if libraries
from tkinter import *
from PIL import ImageTk, Image
import csv
import pandas as pd
import io
from tkinter import ttk
import tkinter.font as tkFont


#avoid to write it always
link ='C:\\Users\\User\\Documents\\Stage_4A_Vanessa\\Interface\\Images'
logo = link + '\\openBCI.ico'
###################################################################################################################
#-------------------------------------------------WINDOW 2---------------------------------------------------------
# the function of the second window we open. When we click on the button it create an other window with this information into
def window_2():
    other = Toplevel()
    other.title("After ASR")
    other.geometry("1200x1200")
    other.iconbitmap(logo)
    label = Label(other, text= "nouvelle fenetre",bg="black",fg="White")
    label.pack()
    
    #we can close the window with this button
    Button(other, text="Close the window", command=other.destroy).pack()
