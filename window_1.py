# import libraries
from tkinter import *
from PIL import ImageTk, Image
import csv
import pandas as pd
import io
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


root = None
axs = None 
# ------------------------------------------------ resize graph--------------------------------
def resize_graph(event):
    # Obtain the new dimension 
    new_width = event.width
    new_height = event.height
    # Redimensionner le widget canvas pour correspondre à la nouvelle taille de la fenêtre
    ax = plt.gca()
    fig = ax.get_figure()
    fig.set_size_inches(new_width/100, new_height/100) 
# ---------------------------------------------------------------------------------------------


# --------------------------------------------- UPDATE THE GRAPHIC AND VERTICAL LINES ---------
def update_graph(axs,time,value, option, event_data):
    # for the color of each channel
    colors = ["#EF9A60", "#A1E7A6", "#A1E7DD", "#A1BCE7", "#A4A1E7", "#CCA1E7", "#E7A1D4", "#E7A1AD", "#B98079"]  
    for i, column in enumerate(value.columns):
        ax = axs[i]
        ax.plot(time, value[column], label=column, alpha=0.5, color=colors[i]) 
        vertical_lines(ax, time.min(), time.max(), event_data)
        ax.set_ylabel('')
        ax.legend()
        if i != 8:
            ax.set_xticks([])
        else : 
            ax.set_xlabel('Time (in seconds)')
        ax.figure.canvas.draw()    

# ---------------------------------------------------------------------------------------------


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ----------------------------- MAIN FUNCTION -------------------------------------------------
def window_1(next_callback,back_callback,file_path, file_path_2,option,value):
    global root
    # Créer la fenêtre principale
    root = Toplevel()
    
    # Creation of a dictionnary with all options for titles for the title of the window and the titel of the graphics
    option_title_name = {"Start": "Start","Open_eyes_1": "Open Eyes 1", "Close_eyes": "Close Eyes","Break_1": "GBreak 1",
        "IMG_TASK_1": "IMG Task 1","Break_2": "Break 2", "IMG_TASK_2": "IMG Task 2","Break_3": "Break 3","Open_eyes_2": "Open Eyes 2"}
    root.title(option_title_name[option])
    
    # Creation of a dictionnary with all options for titles for the title of the graphics
    option_titles = {"Start": "Graphic with the 9 channels during the step Start",
        "Open_eyes_1": "Graphic with the 9 channels during the step Open Eyes 1",
        "Close_eyes": "Graphic with the 9 channels during the step Close Eyes",
        "Break_1": "Graphic with the 9 channels during the step Break 1",
        "IMG_TASK_1": "Graphic with the 9 channels during the step IMG Task 1",
        "Break_2": "Graphic with the 9 channels during the step Break 2",
        "IMG_TASK_2": "Graphic with the 9 channels during the step IMG Task 2",
        "Break_3": "Graphic with the 9 channels during the step Break 3",
        "Open_eyes_2": "Graphic with the 9 channels during the step Open Eyes 2"}
    
    # the first value fir the screen is the dimension of the screen (computer) minus 40 and 100 to see all the window
    window_width = root.winfo_screenwidth()-40
    window_height = root.winfo_screenheight()-100
    x=10
    y=10
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # change the color of the background
    root.config(bg="#CAD0DA")
    # Attach an event handler to the window to detect size changes
    root.bind("<Configure>", resize_graph)

    # Separate data according to the tasks 
    raw_data = pd.read_csv(file_path, delimiter=',')
    raw_data['Time'] = raw_data['Time']/ 1000000 #put the time in seconds
    event_data = pd.read_csv(file_path_2, delimiter=',')
    event_data['0'] = event_data['0']/ 1000000 # first column is the time so we need to put it in seconds
    event_data.iloc[1,0]=raw_data.iloc[0,0] # because the task "start" is not is the time 0 so we adjust them 
    
    global axs
    time = value.index
    num_columns = len(value.columns)
    fig, axs = plt.subplots(nrows=num_columns, ncols=1 , figsize=(16, 1*num_columns))
    fig.set_facecolor('#CAD0DA') 
    fig.suptitle(option_titles[option], y=0.95)
    update_graph(axs,time, value, option, event_data)

    # create a frame with my 3 buttons and the picture inside 
    frame = Frame(root)
    frame.config(bg="#CAD0DA")
    frame.pack(side=TOP, padx=10, pady=10)
        
    # Créer un Frame pour contenir le graphique
    graph_frame = Frame(root)
    graph_frame.pack()

    # Create a tkinter widget to display the graphic
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    fig.canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
    
    

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    link ="C:\\Users\\User\\Documents\\Stage_4A_Vanessa\\Interface\\Images"
    image = Image.open(link + "\\head.png")
    image = image.resize((200, 155))
    global my_img1
    my_img1 = ImageTk.PhotoImage(image)
    root.my_img1 = my_img1 
    my_label = Label(frame, image=my_img1, bg="#CAD0DA")
    my_label.pack(side="left", padx=10)

    #--------------------------------------- change the xlim if we click on the back bouton ------------
    back_button = Button(frame, text="Back 10 seconds",command=back_callback, bg="#249CD0")
    back_button.pack(side="left", padx=10)
    #----------------------------------------------------------------------------------------------------

    #-------------------------we create a button to close the window when we finish in an exact place ---
    bold_font = tkFont.Font(weight="bold")
    exit =Button(frame, text="Close the window", command=root.destroy, font = bold_font,bg="#249CD0")
    exit.pack(side="left")

    #--------------------------------------- change the xlim if we click on the next bouton ------------
    next_button =Button(frame, text="Next 10 seconds", command=next_callback, bg="#249CD0")
    next_button.pack(side="left",padx=10)
    #----------------------------------------------------------------------------------------------------
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    root.mainloop()


    


#ajust the x limit
# ------------------------------------- add vertical lines ----------------------------------------------------
# Add vertical lines with legend for each task present in the event.csv
def vertical_lines(ax, x_min, x_max,event_data):
    # Separate data according to the tasks 
    text_list = []
    for i in range(event_data.shape[0]):
        y_val = 1.02
        x_value = event_data.iloc[i, 0]
        #if we change the xaxis, we just display the vertical lines of this window
        if x_value >= x_min and x_value <= x_max:
            if event_data.iloc[i,1]=="IMGTASK_LA" :
                ax.axvline(x=x_value, color='dodgerblue', linewidth=1)
                text = ax.text(x_value,y_val, 'IMGTASK_LA', fontsize=7, color='dodgerblue',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                text_list.append(text)
            elif event_data.iloc[i,1]=="IMGTASK_RA" :
                ax.axvline(x=x_value, color='teal', linewidth=1)
                text = ax.text(x_value,y_val, 'IMGTASK_RA', fontsize=7, color='teal',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                text_list.append(text)
            elif event_data.iloc[i,1]=="IMGTASK_AT" :
                ax.axvline(x=x_value, color='royalblue', linewidth=1)
                text = ax.text(x_value,y_val, 'IMGTASK_AT', fontsize=7, color='royalblue',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                text_list.append(text)
            elif event_data.iloc[i,1]=="IMGTASK_START" :
                ax.axvline(x=x_value, color='red', linewidth=1)
                text = ax.text(x_value,y_val, 'IMGTASK_START', fontsize=7, color='red',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                text_list.append(text)
            elif event_data.iloc[i,1]=="OE" :
                ax.axvline(x=x_value, color='darkviolet', linewidth=1)
                text = ax.text(x_value,y_val, 'OE', fontsize=7, color='darkviolet',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                text_list.append(text)
            elif event_data.iloc[i,1]=="CE" :
                ax.axvline(x=x_value, color='violet', linewidth=1)
                text = ax.text(x_value,y_val, 'CE', fontsize=7, color='violet',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                text_list.append(text)
            elif event_data.iloc[i,1]=="PAUSE":
                ax.axvline(x=x_value,color='crimson',linewidth=1)
                text = ax.text(x_value,y_val, 'PAUSE', fontsize=7, color='crimson',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                text_list.append(text)
            elif event_data.iloc[i,1]=="START":
                ax.axvline(x=x_value,color='darkred',linewidth=1) 
                text = ax.text(x_value,y_val, 'START', fontsize=7, color='darkred',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                text_list.append(text)
            elif event_data.iloc[i,1]=="END":
                ax.axvline(x=x_value,color='brown',linewidth=1)
                text = ax.text(x_value,y_val, 'END', fontsize=7, color='brown',ha='center',va='bottom', transform=ax.get_xaxis_transform())
                text_list.append(text)
#-------------------------------------------------------------------------------------------------------------------




