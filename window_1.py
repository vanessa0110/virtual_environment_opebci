# import libraries
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import csv
import pandas as pd
import io
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox


# you have to change this link
link ='C:\\Users\\User\\Documents\\Stage_4A_Vanessa\\Interface\\Images'

root = None
axs = None 
###############################################################################################################
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
###############################################################################################################



###############################################################################################################
# --------------------------------------------- UPDATE THE GRAPHIC AND VERTICAL LINES ---------
def update_graph(axs,time,value, event_data):
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
###############################################################################################################



###############################################################################################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ----------------------------- MAIN FUNCTION -------------------------------------------------
def window_1(next_callback, back_callback, event_data, option, value, value_bandpass):
    global root
    # Créer la fenêtre principale
    root = Toplevel()
    
    # Create a window for loading 
    loading_window = Toplevel(root)
    loading_window.title("Wait...")
    # size and position for the loading window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    loading_window_width = 150
    loading_window_height = 150
    x = (screen_width - loading_window_width) // 2
    y = (screen_height - loading_window_height) // 2
    loading_window.geometry(f"{loading_window_width}x{loading_window_height}+{x}+{y}")
    # add a picture for the loading message
    image1 = Image.open(link + "\\loading.png")
    image1 = image1.resize((150, 130))
    my_img = ImageTk.PhotoImage(image1)
    my_label = Label(loading_window, image=my_img)
    my_label.pack()
    loading_label = Label(loading_window, text="Loading...")
    loading_label.pack()

    # MHide the main window in a first time 
    root.withdraw()

    # function to hide the loading window when we have the main window
    def show_main_window():
        loading_window.withdraw()  # Hide loading window
        root.deiconify()  # Show main window
    # after is for display the main window after 5 seconds (it is in microseconds here)
    root.after(5000, show_main_window) 

    
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
    
    
    #we add an other logo (here that of the openBCI)
    logo = link + '\\openBCI.ico'
    image = root.iconbitmap(logo)
    
    # create a frame with my 3 buttons and the picture inside 
    frame = Frame(root)
    frame.config(bg="#CAD0DA")
    frame.pack()#side=TOP, padx=10, pady=10)
    my_notebook = ttk.Notebook(root) # defined a frame where we will create 2 tabs which are "raw data" and "bandpass data"
    my_notebook.pack()
    my_frame1 = Frame(my_notebook)
    my_frame2 = Frame(my_notebook)
    my_frame1.config(bg="#CAD0DA")
    my_frame2.config(bg="#CAD0DA")
    my_frame1.pack()
    my_frame2.pack()
    
    # create a style for the tabs like the width, height and size to write
    style = ttk.Style()
    style.configure("TNotebook.Tab", padding=(20, 6), font=('TkDefaultFont', 13))

    my_notebook.add(my_frame1, text="Raw data")
    my_notebook.add(my_frame2, text="Bandpass")
    
    # Creation of a dictionnary with all options for titles for the title of the window and the titel of the graphics
    option_title_name = {"Start": "Start","Open_eyes_1": "Open Eyes 1", "Close_eyes": "Close Eyes","Break_1": "Break 1",
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
    
    # for the graph of the raw data
    #################################################################################
    global axs
    time = value.index
    num_columns = len(value.columns)
    fig, axs = plt.subplots(nrows=num_columns, ncols=1 , figsize=(16, 1*num_columns))
    fig.set_facecolor('#CAD0DA') 
    fig.suptitle(option_titles[option], y=0.95)
    update_graph(axs,time, value, event_data)
        
    # Create a frame for the graphic of the raw data
    graph_frame = Frame(my_frame1)
    graph_frame.pack()

    # Create a tkinter widget to display the graphic
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    fig.canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
    #################################################################################
    
    # for the graph of the bandpass data
    #################################################################################
    global axes
    time = value_bandpass.index
    num_columns = len(value_bandpass.columns)
    figure, axes = plt.subplots(nrows=num_columns, ncols=1 , figsize=(16, 1*num_columns))
    figure.set_facecolor('#CAD0DA') 
    figure.suptitle(option_titles[option], y=0.95)
    update_graph(axes,time, value_bandpass, event_data)
        
    # Create a frame for the graphic of the raw data
    bandpass_frame = Frame(my_frame2)
    bandpass_frame.pack()

    # Create a tkinter widget to display the graphic
    canvas = FigureCanvasTkAgg(figure, master=bandpass_frame)
    fig.canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
    #################################################################################
    
    ############################## ADD BUTTONS AND PICTURE IN FRAME ##########################################
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    link ="C:\\Users\\User\\Documents\\Stage_4A_Vanessa\\Interface\\Images"
    image = Image.open(link + "\\head.png")
    image = image.resize((200, 155))
    global my_img1
    my_img1 = ImageTk.PhotoImage(image)
    root.my_img1 = my_img1 
    my_label = Label(frame, image=my_img1, bg="#CAD0DA")
    my_label.grid(row=0, column=0, rowspan=2, padx=10)#pack(side="left", padx=10)

    #--------------------------------------- change the xlim if we click on the back bouton ------------
    back_button = Button(frame, text="Back 10 seconds",command=back_callback, bg="#249CD0")
    back_button.grid(row=0, column=1, padx=10)
    #----------------------------------------------------------------------------------------------------

    #-------------------------we create a button to close the window when we finish in an exact place ---
    bold_font = tkFont.Font(weight="bold")
    exit =Button(frame, text="Close the window", command=root.destroy, font = bold_font,bg="#249CD0")
    exit.grid(row=0, column=2)

    #--------------------------------------- change the xlim if we click on the next bouton ------------
    next_button =Button(frame, text="Next 10 seconds", command=next_callback, bg="#249CD0")
    next_button.grid(row=0,column=3,padx=10)
    #----------------------------------------------------------------------------------------------------
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ##########################################################################################################
    
    ###############################################################################################################
    
    
    root.mainloop()


    

################################################################################################################################################
#ajust the x limit
# ------------------------------------- add vertical lines ----------------------------------------------------
# Add vertical lines with legend for each task present in the event.csv
def vertical_lines(ax, x_min, x_max,event_data):
    # Separate data according to the tasks 
    text_list = []
    for i in range(event_data.shape[0]):
        y_val = 1.02
        x_value = event_data.iloc[i, 0]
        #if we change the xaxis, we just display the vertical lines of this window and the text also
        vertical = {"IMGTASK_LA" : "dodgerblue", "IMGTASK_RA" : "teal", "IMGTASK_AT" : "royalblue", "IMGTASK_START" : "red",
                    "OE" : "darkviolet", "CE" : "violet", "PAUSE" : "crimson", "START" : "darkred", "END": "brown"}
        if x_max >= x_value >= x_min :
            for j in vertical :
                if event_data.iloc[i,1]== j :
                    ax.axvline(x = x_value, color= vertical[j], linewidth=1)
                    text = ax.text(x_value, y_val, j, fontsize=7, color = vertical[j], ha='center', va='bottom', transform=ax.get_xaxis_transform())
                    text_list.append(text)
            
#-------------------------------------------------------------------------------------------------------------------
################################################################################################################################################



