# import libraries
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
import wind2_bis,wind1_bis
import splite_task



def windoww0(file_path,file_path_2):
    importlib.reload(splite_task) #last version of splite_task
    splite_task.splite_data_create_variables(file_path, file_path_2)
    importlib.reload(wind2_bis) #last version of wind2_bis
    importlib.reload(wind1_bis) #last version of wind1_bis

    #creation of a window
    root=Toplevel()

    #we give a title for the window, a size by default and a background color also
    window_width = 400
    window_height = 150
    x= (root.winfo_screenwidth()-window_width)//2
    y = (root.winfo_screenheight()-window_height)//2
    root.title("Vizualize data")
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.configure(bg="#CAD0DA")

    #avoid to write it always
    link ='C:\\Users\\User\\Documents\\Stage_4A_Vanessa\\Interface\\Images'
    logo = link + '\\openBCI.ico'


    #we add a other logo (here that of the openBCI)
    image = root.iconbitmap(logo)

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


    # ------------------------- We create a menu where people can select the task they want to see ----------------------------------------------
    # Create a general function to plot data and vertical lines, it's better
    def call_plot(value,option):
        wind1_bis.window_1(next_10_seconds,back_10_seconds, file_path, file_path_2, option, value)

    # Function to plot data more efficient because all the data are in a list
    def callback_general(j, index, option):
        i = index
        value = list[j][i]
        call_plot(value,option)

    global current_index
    current_index = 0
    
    # Call this function if we select a task   
    def option_callback(option):
        global current_index
        if option == "Start":
            value = list[0]
            call_plot(value, option)
            current_index = 0
        elif option == "Open_eyes_1":
            current_index = 0
            callback_general(1,current_index, option)
        elif option == "Close_eyes":
            current_index = 0
            callback_general(2,current_index, option)
        elif option == "Break_1":
            current_index = 0
            value = list[3]
            call_plot(value, option)
        elif option == "IMG_TASK_1":
            current_index = 0
            callback_general(4,current_index, option)
        elif option == "Break_2":
            current_index = 0
            callback_general(5,current_index, option)
        elif option == "IMG_TASK_2":
            current_index = 0
            callback_general(6,current_index, option)
        elif option == "Break_3":
            current_index = 0
            callback_general(7,current_index, option)
        elif option == "Open_eyes_2":
            current_index = 0
            callback_general(8,current_index, option)
         
         
    # We write a text
    custom_font = tkFont.Font(size=16)
    mylabel = Label(root,text = "Please select the task you want to see : ", font = custom_font, bg="#CAD0DA")
    mylabel.pack(side="top", pady=20)
       
    # We create the menu
    bold_font = tkFont.Font(weight="bold")
    clicked = StringVar()
    clicked.set("Task")
    options= ["Start","Open_eyes_1", "Close_eyes", "Break_1", "IMG_TASK_1","Break_2","IMG_TASK_2","Break_3","Open_eyes_2"]
    drop = OptionMenu(root, clicked, *options, command=lambda option: option_callback(option))
    drop.configure(font=bold_font,bg="#249CD0")#bg="#CAD0DA")
    drop.pack(anchor="center",side="top")


    def update_plot_s_et_b1(direction):
        global current_index
        if direction == "next":
            current_index += 1
        elif direction == "back":
            current_index = current_index-3
        if  current_index !=0:
            # say message if we are already at the begining or at the end of the list
            if direction == "next":
                messagebox.showinfo("End of list", "You have reached the end of the list.", parent=wind1_bis.root)
            elif direction == "back":
                messagebox.showinfo("Start of list", "You have reached the start of the list.", parent=wind1_bis.root)

        
    # --------------------------------------------- we update the graphic if we click on the next or back boutton -------------------------------
    event_data = pd.read_csv(file_path_2, delimiter=',')
    event_data['0'] = event_data['0']/ 1000000 # first column is the time so we need to put it in seconds
    
    # general funtion to update the graphic 
    def update_plot(i, direction, option, event_data):        
        global current_index
        if direction == "next":
            current_index += 1
        elif direction == "back":
            current_index -= 1
        if 0 <= current_index < len(list[i]):
            value = list[i][current_index]
            time = value.index
            colors = ["#EF9A60", "#A1E7A6", "#A1E7DD", "#A1BCE7", "#A4A1E7", "#CCA1E7", "#E7A1D4", "#E7A1AD", "#B98079"] 
            for i, ax in enumerate(wind1_bis.axs):
                ax.cla()
                ax.plot(time, value[value.columns[i]], label=value.columns[i], alpha=0.5, color=colors[i])
                wind1_bis.vertical_lines(ax, time.min(), time.max(), event_data)
                ax.set_ylabel('')
                if i != 8:
                    ax.set_xticks([])
                else:
                    ax.set_xlabel('Time (in seconds)')
                # Calculer les nouvelles limites de l'axe des y
                ymin = value[value.columns[i]].min()
                ymax = value[value.columns[i]].max()
                ax.set_ylim(ymin, ymax)
                ax.set_xlim(time.min(), time.max())
            ax.figure.canvas.draw()
        else:
            # say message if we are already at the begining or at the end of the list
            if direction == "next":
                messagebox.showinfo("End of list", "You have reached the end of the list.", parent=wind1_bis.root)
            elif direction == "back":
                messagebox.showinfo("Start of list", "You have reached the start of the list.", parent=wind1_bis.root)
      

    # display the next seconds           
    def next_10_seconds():
        option = clicked.get()
        if option == "Start":
            update_plot_s_et_b1("next")
        elif option == "Open_eyes_1":
            update_plot(1, "next",option, event_data)
        elif option == "Close_eyes":
            update_plot(2, "next",option, event_data)
        elif option == "Break_1":
            update_plot_s_et_b1("next")
        elif option == "IMG_TASK_1":
            update_plot(4, "next",option, event_data)
        elif option == "Break_2":
            update_plot(5, "next",option, event_data)
        elif option == "IMG_TASK_2":
            update_plot(6, "next",option, event_data)
        elif option == "Break_3":
            update_plot(7, "next",option, event_data)
        elif option == "Open_eyes_2":
            update_plot(8, "next",option, event_data)

    # display the back 10 seconds and adjust the x limits
    def back_10_seconds():
        option = clicked.get()
        if option == "Start":
            update_plot_s_et_b1("back")
        elif option == "Open_eyes_1":
            update_plot(1, "back",option, event_data)
        elif option == "Close_eyes":
            update_plot(2, "back",option, event_data)
        elif option == "Break_1":
            update_plot_s_et_b1("back")
        elif option == "IMG_TASK_1":
            update_plot(4, "back",option, event_data)
        elif option == "Break_2":
            update_plot(5, "back",option, event_data)
        elif option == "IMG_TASK_2":
            update_plot(6, "back",option, event_data)
        elif option == "Break_3":
            update_plot(7, "back",option, event_data)
        elif option == "Open_eyes_2":
            update_plot(8, "back",option, event_data)
    # -------------------------------------------------------------------------------------------------------------------------------------------



    root.mainloop()