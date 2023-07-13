# import if libraries
from tkinter import *
from PIL import ImageTk, Image
import csv
import pandas as pd
import io
from tkinter import ttk
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox
import importlib
import window_1
import splite_task
import bandpass


#avoid to write it always, CHANGE IT
link ='C:\\Users\\User\\Documents\\Stage_4A_Vanessa\\Interface\\Images'


def windoww0(file_path,file_path_2):
    
    # Separate data according to the tasks 
    raw_data = pd.read_csv(file_path, delimiter=',')
    raw_data['Time'] = raw_data['Time']/ 1000000 #put the time in seconds
    event_data = pd.read_csv(file_path_2, delimiter=',')
    event_data['0'] = event_data['0']/ 1000000 # first column is the time so we need to put it in seconds
    event_data.iloc[1,0]=raw_data.iloc[0,0] # because the task "start" is not is the time 0 so we adjust them 
    

    importlib.reload(splite_task) #last version of splite_task
    splite_task.splite_10_seconds_by_10_seconds(raw_data, event_data)
    importlib.reload(window_1) #last version of wind1_bis

    #creation of a window
    root=Toplevel()
    
    ############################################### LOADING WINDOW ##########################################
     # Create a window for loading 
    loading_window = Toplevel(root)
    loading_window.title("Wait...")
    # size and position for the loading window
    screen_width = loading_window.winfo_screenwidth()
    screen_height = loading_window.winfo_screenheight()
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
    # Masquez la fenêtre principale initialement
    root.withdraw()

    # Définissez une fonction pour masquer la fenêtre de chargement et afficher la fenêtre principale
    def show_main_window():
        loading_window.withdraw()  # Masque la fenêtre de chargement
        root.deiconify()  # Affiche la fenêtre principale

    # # after is for display the main window after 3 seconds (it is in microseconds here)
    root.after(3000, show_main_window)  
    #########################################################################################################
    
    #we give a title for the window, a size by default and a background color also
    window_width = 400
    window_height = 150
    x= (root.winfo_screenwidth()-window_width)//2
    y = (root.winfo_screenheight()-window_height)//2
    root.title("Vizualize data")
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.configure(bg="#CAD0DA")

    #we add an other logo (here that of the openBCI)
    logo = link + '\\openBCI.ico'
    image = root.iconbitmap(logo)

    ############################################################# RAW DATA #####################################
    # ----------------------------------------- Create liste with all 10 secondes for each variable ------------
    liste_oe1 = [eval(f"splite_task.oe1_{i}_df") for i in range(13)]
    liste_ce = [eval(f"splite_task.ce_{i}_df") for i in range(13)]
    liste_it1 = [eval(f"splite_task.it1_{i}_df") for i in range(32)]
    liste_p2 = [eval(f"splite_task.p2_{i}_df") for i in range(13)]
    liste_it2 = [eval(f"splite_task.it2_{i}_df") for i in range(32)]
    liste_p3 = [eval(f"splite_task.p3_{i}_df") for i in range(2)]
    liste_oe2 = [eval(f"splite_task.oe2_{i}_df") for i in range(13)]
    # ----------------------------------------------------------------------------------------------------------

    list = [splite_task.start, liste_oe1, liste_ce, splite_task.pause_1, liste_it1, liste_p2, liste_it2, liste_p3, liste_oe2]

    
    ###################################################### BANDPASS DATA #######################################
    importlib.reload(bandpass)
    bandpass_data = bandpass.bandpass_function(raw_data)
    #bandpass_data['Time'] = bandpass_data['Time']/ 1000000 #put the time in seconds
    splite_task.splite_10_seconds_by_10_seconds(bandpass_data, event_data)
    liste_oe1 = [eval(f"splite_task.oe1_{i}_df") for i in range(13)]
    liste_ce = [eval(f"splite_task.ce_{i}_df") for i in range(13)]
    liste_it1 = [eval(f"splite_task.it1_{i}_df") for i in range(32)]
    liste_p2 = [eval(f"splite_task.p2_{i}_df") for i in range(13)]
    liste_it2 = [eval(f"splite_task.it2_{i}_df") for i in range(32)]
    liste_p3 = [eval(f"splite_task.p3_{i}_df") for i in range(2)]
    liste_oe2 = [eval(f"splite_task.oe2_{i}_df") for i in range(13)]
    # ----------------------------------------------------------------------------------------------------------

    list_bandpass = [splite_task.start, liste_oe1, liste_ce, splite_task.pause_1, liste_it1, liste_p2, liste_it2, liste_p3, liste_oe2]



    ###############################################################################################################
    # ------------------------- We create a menu where people can select the task they want to see ------------
    # Create a general function to plot data and vertical lines, it's better
    def call_plot(value, value_bandpass, option):
        window_1.window_1(next_10_seconds,back_10_seconds, event_data, option, value, value_bandpass)
    ###############################################################################################################


    ###############################################################################################################
    # Function to plot data more efficient because all the data are in a list
    def callback_general(j, index, option):
        i = index
        value = list[j][i]
        value2 = list_bandpass[j][i]
        call_plot(value, value2, option)
    ###############################################################################################################
    
    
    global current_index
    current_index = 0
    
    
    ###############################################################################################################
    # Call this function if we select a task   
    def option_callback(option):
        global current_index
        current_index = 0
        dic = {"Open_eyes_1" : 1, "Close_eyes" : 2, "IMG_TASK_1" : 4, "Break_2" : 5, "IMG_TASK_2" : 6, "Break_3" : 7, "Open_eyes_2" : 8}
        for i in dic:
            if option == i :
                callback_general(dic[i], current_index, option)
        if option == "Start":
            value = list[0]
            value2 = list_bandpass[0]
            call_plot(value, value2, option)
        elif option == "Break_1":
            value = list[3]
            value2 = list_bandpass[3]
            call_plot(value, value2, option)
    ###############################################################################################################     
         
         
    ###############################################################################################################
    # We write a text
    custom_font = tkFont.Font(size=16)
    mylabel = Label(root,text = "Please select the task you want to see : ", font = custom_font, bg="#CAD0DA")
    mylabel.pack(side="top", pady=20)
    ###############################################################################################################
       
       
    ###############################################################################################################
    # We create the menu
    bold_font = tkFont.Font(weight="bold")
    clicked = StringVar()
    clicked.set("Task")
    options= ["Start","Open_eyes_1", "Close_eyes", "Break_1", "IMG_TASK_1","Break_2","IMG_TASK_2","Break_3","Open_eyes_2"]
    drop = OptionMenu(root, clicked, *options, command=lambda option: option_callback(option))
    drop.configure(font=bold_font,bg="#249CD0")
    drop.pack(anchor="center",side="top")
    ###############################################################################################################



    ###############################################################################################################
    def update_plot_s_et_b1(direction):
        global current_index
        # change the current index when we click on a button and display a message if the current_index isn't in the list
        if direction == "next":
            current_index += 1
        elif direction == "back":
            current_index = current_index-3
        if  current_index !=0:
            # say message if we are already at the begining or at the end of the list
            if direction == "next":
                messagebox.showinfo("End of list", "You have reached the end of the list.", parent=window_1.root)
            elif direction == "back":
                messagebox.showinfo("Start of list", "You have reached the start of the list.", parent=window_1.root)
    ###############################################################################################################
        
        
    ###############################################################################################################
    # general funtion to update the graphic 
    def update_plot(i, direction, event_data):        
        global current_index
        if direction == "next":
            current_index += 1
        elif direction == "back":
            current_index -= 1
        # for the raw data 
        #----------------------------------------------------------------------------------------------------------------
        if 0 <= current_index < len(list[i]):
            value = list[i][current_index]
            time = value.index
            colors = ["#EF9A60", "#A1E7A6", "#A1E7DD", "#A1BCE7", "#A4A1E7", "#CCA1E7", "#E7A1D4", "#E7A1AD", "#B98079"] 
            for i, ax in enumerate(window_1.axs):
                ax.cla()
                ax.plot(time, value[value.columns[i]], label=value.columns[i], alpha=0.5, color=colors[i])
                window_1.vertical_lines(ax, time.min(), time.max(), event_data)
                ax.set_ylabel('')
                if i != 8:
                    ax.set_xticks([])
                else:
                    ax.set_xlabel('Time (in seconds)')
                # new limits for y_axis
                ymin = value[value.columns[i]].min()
                ymax = value[value.columns[i]].max()
                ax.set_ylim(ymin, ymax)
                ax.set_xlim(time.min(), time.max())
            ax.figure.canvas.draw()
        #----------------------------------------------------------------------------------------------------------------
        
        # for bandpass data
        #----------------------------------------------------------------------------------------------------------------
        if 0 <= current_index < len(list_bandpass[i]):
            value2 = list_bandpass[i][current_index]
            time = value2.index
            colors = ["#EF9A60", "#A1E7A6", "#A1E7DD", "#A1BCE7", "#A4A1E7", "#CCA1E7", "#E7A1D4", "#E7A1AD", "#B98079"] 
            for i, ax in enumerate(window_1.axes):
                ax.cla()
                ax.plot(time, value2[value2.columns[i]], label=value2.columns[i], alpha=0.5, color=colors[i])
                window_1.vertical_lines(ax, time.min(), time.max(), event_data)
                ax.set_ylabel('')
                if i != 8:
                    ax.set_xticks([])
                else:
                    ax.set_xlabel('Time (in seconds)')
                # new limits for y_axis
                ymin = value2[value2.columns[i]].min()
                ymax = value2[value2.columns[i]].max()
                ax.set_ylim(ymin, ymax)
                ax.set_xlim(time.min(), time.max())
            ax.figure.canvas.draw()
        #----------------------------------------------------------------------------------------------------------------
        else:
            # say message if we are already at the begining or at the end of the list
            if direction == "next":
                messagebox.showinfo("End of list", "You have reached the end of the list.", parent=window_1.root)
            elif direction == "back":
                messagebox.showinfo("Start of list", "You have reached the start of the list.", parent=window_1.root)
    ###############################################################################################################


    ###############################################################################################################
    # display the next seconds           
    def next_10_seconds():
        # create a dictionnary to call the function update_plot only in a for loop
        dic = {"Open_eyes_1" : 1, "Close_eyes" : 2, "IMG_TASK_1" : 4, "Break_2" : 5, "IMG_TASK_2" : 6, "Break_3" : 7, "Open_eyes_2" : 8}
        option = clicked.get()
        if option == "Start":
            update_plot_s_et_b1("next")
        elif option == "Break_1":
            update_plot_s_et_b1("next")
        
        for i in dic:
            if option == i :
                update_plot(dic[i], "next", event_data)
    ###############################################################################################################
    
    ###############################################################################################################
    # display the back 10 seconds and adjust the x limits
    def back_10_seconds():
        # create a dictionnary to call the function update_plot only in a for loop
        dic = {"Open_eyes_1" : 1, "Close_eyes" : 2, "IMG_TASK_1" : 4, "Break_2" : 5, "IMG_TASK_2" : 6, "Break_3" : 7, "Open_eyes_2" : 8}
        option = clicked.get()
        if option == "Start":
            update_plot_s_et_b1("back")
        elif option == "Break_1":
            update_plot_s_et_b1("back")
        
        for i in dic:
            if option == i :
                update_plot(dic[i], "back", event_data)
    ###############################################################################################################
    
    # -------------------------------------------------------------------------------------------------------------------------------------------
    root.mainloop()