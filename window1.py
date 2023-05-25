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
    my_label.place(x=650,y=0)

    #------------------ Graphic ---------------------------------------------------------------
    # load the data 
    road = 'C:\\Users\\User\\Documents\\Stage_4A_Vanessa\\doc_matlab'
    raw_data = pd.read_csv(road +'/2021911-19-2-data.csv', delimiter=',',index_col=0)
    event_data = pd.read_csv(road+'\\2021911-19-2-events.csv', delimiter=',')
    
    # create a figure and plot them with the library seaborn
    fig, ax = plt.subplots()
    sns.set(rc={'figure.figsize':(16,6)})
    sns.lineplot(data=raw_data)

    

    #ajust the x limit
    # Define a dictionary to store x-axis limits
    x_limits = {'minimum': 400, 'maximum': 410}
    plt.xlim(x_limits['minimum'] * 1000000, x_limits['maximum'] * 1000000)
    
    # ------------------------------------- add vertical lines ----------------------------------------------------
    # Add vertical lines with legend for each task present in the event.csv
    text_list = []
    
    def vertical_lines():
        for i in range(event_data.shape[0]):
            # retrieve max values of x
            x_min, x_max = ax.get_xlim()
            x_value = event_data.iloc[i, 0]
            #if we change the xaxis, we just display the vertical lines of this window
            if x_value >= x_min and x_value <= x_max:
                if event_data.iloc[i,1]=="IMGTASK_LA" :
                    plt.axvline(x=x_value, color='darkcyan', linewidth=1)
                    text = ax.text(x_value,110000, 'IMGTASK_LA', fontsize=7, color='darkcyan', rotation='vertical')
                    text_list.append(text)
                elif event_data.iloc[i,1]=="IMGTASK_RA" :
                    plt.axvline(x=x_value, color='mediumturquoise', linewidth=1)
                    text = ax.text(x_value,110000, 'IMGTASK_RA', fontsize=7, color='mediumturquoise', rotation='vertical')
                    text_list.append(text)
                elif event_data.iloc[i,1]=="IMGTASK_AT" :
                    plt.axvline(x=x_value, color='cyan', linewidth=1)
                    text = ax.text(x_value,110000, 'IMGTASK_AT', fontsize=7, color='cyan', rotation='vertical')
                    text_list.append(text)
                elif event_data.iloc[i,1]=="IMGTASK_START" :
                    plt.axvline(x=x_value, color='red', linewidth=1)
                    text = ax.text(x_value,110000, 'IMGTASK_START', fontsize=7, color='red', rotation='vertical')
                    text_list.append(text)
                elif event_data.iloc[i,1]=="OE" :
                    plt.axvline(x=x_value, color='darkviolet', linewidth=1)
                    text = ax.text(x_value,110000, 'OE', fontsize=7, color='darkviolet', rotation='vertical')
                    text_list.append(text)
                elif event_data.iloc[i,1]=="CE" :
                    plt.axvline(x=x_value, color='violet', linewidth=1)
                    text = ax.text(x_value,110000, 'CE', fontsize=7, color='violet', rotation='vertical')
                    text_list.append(text)
                elif event_data.iloc[i,1]=="PAUSE":
                    plt.axvline(x=x_value,color='crimson',linewidth=1)
                    text = ax.text(x_value,110000, 'PAUSE', fontsize=7, color='crimson', rotation='vertical')
                    text_list.append(text)
                elif event_data.iloc[i,1]=="START":
                    plt.axvline(x=x_value,color='darkred',linewidth=1) 
                    text = ax.text(x_value,110000, 'START', fontsize=7, color='darkred', rotation='vertical')
                    text_list.append(text)
                elif event_data.iloc[i,1]=="END":
                    plt.axvline(x=x_value,color='brown',linewidth=1)
                    text = ax.text(x_value,110000, 'END', fontsize=7, color='brown', rotation='vertical')
                    text_list.append(text)
                
    #-------------------------------------------------------------------------------------------------------------------

    #--------------------------------------- change the xlim if we click on the next bouton ------------
    def update_plot(x_minimum, x_maximum):
        plt.xlim(x_minimum * 1000000, x_maximum * 1000000)
        # Convert the tick values from milliseconds to seconds
        xticks_seconds = [tick / 1000000 for tick in ax.get_xticks()]
        # Set the new tick labels on the x-axis
        ax.set_xticklabels(xticks_seconds)
        vertical_lines()
        plt.draw()
    
    
    def nexxt():
        # Remove the previous text
        for text in text_list:
            text.remove()
        text_list.clear()
        # Update the x-axi
        x_limits['minimum'] += 10
        x_limits['maximum'] += 10
        update_plot(x_limits['minimum'], x_limits['maximum'])

    next = Button(second_frame, text='>', command=nexxt,bg="#249CD0")
    next.place(x=815,y=840)
    #----------------------------------------------------------------------------------------------------
    
    
    #--------------------------------------- change the xlim if we click on the back bouton ------------
    def bacck():
        # Remove the previous text
        for text in text_list:
            text.remove()
        text_list.clear()
        x_limits['minimum'] -= 10
        x_limits['maximum'] -= 10
        update_plot(x_limits['minimum'], x_limits['maximum'])
        
    back = Button(second_frame, text='<', command=bacck,bg="#249CD0")
    back.place(x=600,y=840)
    #----------------------------------------------------------------------------------------------------
    


    # Get the current x-axis tick labels
    xticks = ax.get_xticks()
    # Convert the tick values from milliseconds to seconds
    xticks_seconds = [tick / 1000000 for tick in xticks]
    # Set the new tick labels on the x-axis
    ax.set_xticklabels(xticks_seconds)
   
    vertical_lines()

    
    # Add the canvas to the frame
    canvas = FigureCanvasTkAgg(fig, master=second_frame)
    canvas.draw()
    canvas.get_tk_widget().place(x=0, y=200)

    

    #---------------------------- we create a button to close the window when we finish in an exact place ------------------------
    bold_font = tkFont.Font(weight="bold")
    exit = Button(second_frame, text="Close the window", command=other.destroy,font=bold_font,bg="#249CD0")
    exit.place(x=625,y=830)
    
    #---------------------------- we create a button to come bakc at the home page ---------------------- ------------------------
    #home_page = Button(second_frame, text="Come back to the menu", command=lambda : show_frame(root),font=bold_font)
    #home_page.place(x=650,y=875)
    
    

    other.mainloop()


