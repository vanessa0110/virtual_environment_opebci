# import libraries
from tkinter import *
from PIL import ImageTk, Image
import csv
import io
import tkinter.font as tkFont
import importlib
import window0
from tkinter import filedialog
importlib.reload(window0)

main = Tk()
main.title("Interface for clinician")

# open the window in the middle of my screen 
window_width = 1200
window_height = 740
x= (main.winfo_screenwidth()-window_width)//2
y = (main.winfo_screenheight()-(window_height+40))//2
main.geometry(f"{window_width}x{window_height}+{x}+{y}")
main.configure(bg="#CAD0DA")

#avoid to write it always
link ='C:\\Users\\User\\Documents\\Stage_4A_Vanessa\\Interface\\Images'
logo = link + '\\openBCI.ico'


#we add a other logo (here that of the openBCI)
image = main.iconbitmap(logo)

# We open the image for the home page with our specific size and we load it
image = Image.open(link + "\\banniere.png")
image = image.resize((1200, 600))
my_img = ImageTk.PhotoImage(image)
my_label = Label(main, image=my_img)
my_label.pack()

# ---------------------------------- for the data file -----------------------------------
file_path_data = ""
file_path_event = ""
bold_font = tkFont.Font(weight="bold")
def open_file():
    global file_path_data
    file_path_data = filedialog.askopenfilename()
    if file_path_data:
        label = Label(main, text="Data file path : \n"+file_path_data)
        label.place(x=315,y=628)
    else:
        label = Label(main, text="Error: No data file selected.", fg="red")
        label.place(x=315, y=628)
    
button = Button(main, text="Select data file to open", command=open_file,font=bold_font)
button.place(x=52,y=625)
# ----------------------------------------------------------------------------------------

# ---------------------------------- for the event file ----------------------------------
def open_file_e():
    global file_path_event
    file_path_event = filedialog.askopenfilename()
    if file_path_event :
        label = Label(main, text="Event file path : \n"+file_path_event)
        label.place(x=315,y=693)
    else:
        label = Label(main, text="Error: No data file selected.", fg="red")
        label.place(x=315, y=693)
        
button_event = Button(main,text="Select event file to open", command=open_file_e, font=bold_font)
button_event.place(x=50,y=690)
# ----------------------------------------------------------------------------------------

# we create a button which call window0 when we click and an error message appear if a file is not selected
def visualize_data():
    if file_path_data and file_path_event:
        window0.windoww0(file_path_data, file_path_event)
    else:
        error_label = Label(main, text="Error: Data file or event file is missing.", fg="red")
        error_label.place(x=870, y=695)

b2 = Button(main, text="Visualize data", command=visualize_data, font=bold_font)
b2.place(x=900, y=663)

main.mainloop()