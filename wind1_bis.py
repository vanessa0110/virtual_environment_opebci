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
from scipy.signal import detrend
from scipy.stats import zscore




#avoid to write it always
link ='C:\\Users\\User\\Documents\\Stage_4A_Vanessa\\Interface\\Images'
logo = link + '\\openBCI.ico'



###################################################################################################################
#-------------------------------------------------WINDOW 1---------------------------------------------------------
# the function of the first window we open. When we click on the button it create a new window with this information into
def window_1():
    other = Toplevel()
    other.title("Raw data") #we change the title of the new window 
    other.geometry("1400x1600")
    other.iconbitmap(logo)

    # create a main frame
    main_frame =  Frame(other)
    main_frame.pack(fill=BOTH, expand=1)

    # create a canvas
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # add a scrollbar to the canvas : a vertical and horizontal one 
    my_scrollbarv = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbarv.pack(side=RIGHT, fill=Y)
    my_scrollbarh = ttk.Scrollbar(main_frame, orient=HORIZONTAL, command=my_canvas.xview)
    my_scrollbarh.pack(side=TOP,fill=X)

    # configure the canvas
    my_canvas.configure(yscrollcommand = my_scrollbarv.set)
    my_canvas.configure(xscrollcommand = my_scrollbarh.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")) )

    # create an other frame inside the canvas
    second_frame = Frame(my_canvas)

    # add the new frame to a window in the canvas 
    my_canvas.create_window((0,0), window= second_frame, anchor="nw")
    second_frame.config(width=1600, height=1200)



    #------------------ Image of nomenclature --------------------------------------------------
    global my_img1
    image = Image.open(link + "\\head__1_-removebg-preview.png")
    image = image.resize((150, 200))
    my_img1 = ImageTk.PhotoImage(image)
    my_label = Label(second_frame, image=my_img1)
    my_label.place(x=400,y=0)

    #------------------ Graphic ---------------------------------------------------------------
    # load the data 
    road = 'C:\\Users\\User\\Documents\\Stage_4A_Vanessa\\doc_matlab'
    raw_data = pd.read_csv(road +'/2021911-19-2-data.csv', delimiter=',')
    # Separate data according to the tasks 
    raw_data['Time'] = raw_data['Time']/ 1000000 #put the time in seconds
    event_data = pd.read_csv(road+'\\2021911-19-2-events.csv', delimiter=',')

    def plot(value) : 
        #### plot
        fig, ax = plt.subplots()
        sns.set(rc={'figure.figsize':(16,6)})
        value_normalized = value.copy()
        value_normalized.iloc[:,:] = zscore(value.iloc[:,:], axis=0)
        value_detrended = value_normalized.copy()
        value_detrended.iloc[:,:] = detrend(value.iloc[:,:], axis=0)
        sns.lineplot(data=value_detrended, x='Time', y='FC3', ax=ax, label='FC3')
        sns.lineplot(data=value_detrended, x='Time', y='FCZ', ax=ax, label='FCZ')
        sns.lineplot(data=value_detrended, x='Time', y='FC4', ax=ax, label='FC4')
        sns.lineplot(data=value_detrended, x='Time', y='C3', ax=ax, label='C3')
        sns.lineplot(data=value_detrended, x='Time', y='Cz', ax=ax, label='CZ')
        sns.lineplot(data=value_detrended, x='Time', y='C4', ax=ax, label='C4')
        sns.lineplot(data=value_detrended, x='Time', y='CP3', ax=ax, label='CP3')
        sns.lineplot(data=value_detrended, x='Time', y='CPz', ax=ax, label='CPZ')
        sns.lineplot(data=value_detrended, x='Time', y='CP4', ax=ax, label='CP4')
        #scipy.signal.detrend(value, axis=- 1, type='linear', bp=0, overwrite_data=False)
        lines = ax.lines
        for line in lines :
            line.set_alpha(0.5)
        ax.set_ylabel('')
        ax.set_xlabel('Time (in seconds)')
        ax.legend()
        ax.figure.canvas.draw()
        # Add the canvas to the frame   
        canvas = FigureCanvasTkAgg(fig, master=second_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=200)
        
    # --------------------------------------------------------------------------------------


    #ajust the x limit
    # ------------------------------------- add vertical lines ----------------------------------------------------
    # Add vertical lines with legend for each task present in the event.csv
    text_list = []
    def vertical_lines(ax, x_min, x_max):
        event_data['0'] = event_data['0']/ 1000000 
        for i in range(event_data.shape[0]):
            y_val = 1.02
            x_value = event_data.iloc[i, 0]
            #if we change the xaxis, we just display the vertical lines of this window
            if x_value >= x_min and x_value <= x_max:
                if event_data.iloc[i,1]=="IMGTASK_LA" :
                    plt.axvline(x=x_value, color='darkcyan', linewidth=1)
                    text = ax.text(x_value,y_val, 'IMGTASK_LA', fontsize=7, color='darkcyan',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                    text_list.append(text)
                elif event_data.iloc[i,1]=="IMGTASK_RA" :
                    plt.axvline(x=x_value, color='mediumturquoise', linewidth=1)
                    text = ax.text(x_value,y_val, 'IMGTASK_RA', fontsize=7, color='mediumturquoise',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                    text_list.append(text)
                elif event_data.iloc[i,1]=="IMGTASK_AT" :
                    plt.axvline(x=x_value, color='cyan', linewidth=1)
                    text = ax.text(x_value,y_val, 'IMGTASK_AT', fontsize=7, color='cyan',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                    text_list.append(text)
                elif event_data.iloc[i,1]=="IMGTASK_START" :
                    plt.axvline(x=x_value, color='red', linewidth=1)
                    text = ax.text(x_value,y_val, 'IMGTASK_START', fontsize=7, color='red',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                    text_list.append(text)
                elif event_data.iloc[i,1]=="OE" :
                    plt.axvline(x=x_value, color='darkviolet', linewidth=1)
                    text = ax.text(x_value,y_val, 'OE', fontsize=7, color='darkviolet',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                    text_list.append(text)
                elif event_data.iloc[i,1]=="CE" :
                    plt.axvline(x=x_value, color='violet', linewidth=1)
                    text = ax.text(x_value,y_val, 'CE', fontsize=7, color='violet',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                    text_list.append(text)
                elif event_data.iloc[i,1]=="PAUSE":
                    plt.axvline(x=x_value,color='crimson',linewidth=1)
                    text = ax.text(x_value,y_val, 'PAUSE', fontsize=7, color='crimson',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                    text_list.append(text)
                elif event_data.iloc[i,1]=="START":
                    plt.axvline(x=x_value,color='darkred',linewidth=1) 
                    text = ax.text(x_value,y_val, 'START', fontsize=7, color='darkred',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                    text_list.append(text)
                elif event_data.iloc[i,1]=="END":
                    plt.axvline(x=x_value,color='brown',linewidth=1)
                    text = ax.text(x_value,y_val, 'END', fontsize=7, color='brown',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                    text_list.append(text)
                
    #-------------------------------------------------------------------------------------------------------------------


    #--------------------------------------- change the xlim if we click on the next bouton ------------
    #arrow = my_canvas.create_polygon(50,200,150,150,150,250, fill="black")
    #my_canvas.tag_bind(arrow,"<Button-1>", )
    next = Button(second_frame, text='>',bg="#249CD0")
    next.place(x=1000,y=82)
         
    #----------------------------------------------------------------------------------------------------

    #---------------------------- we create a button to close the window when we finish in an exact place ------------------------
    bold_font = tkFont.Font(weight="bold")
    exit = Button(second_frame, text="Close the window", command=other.destroy,font=bold_font,bg="#249CD0")
    exit.place(x=800,y=75)

    return plot,vertical_lines




