import pyautogui
import ctypes
import time 

import threading
from tkinter import *
from PIL import *
from os import path

#https://www.mirametrics.com/help/mira_pro_script_8/source/getkeystate.htm 

#GLOBAL VARIABLE
VERSION = "1.0"

CURRENT_WORKING_DIRECTORY = path.dirname(__file__)
SAVE_FILE_PATH = CURRENT_WORKING_DIRECTORY + "\\resources\\" + "tomoclicker_save_file.txt"

MENU_TOGGLE_ON = False
ACTIVE_PROCESS_ON = False

CURRENT_LOADED_X = -1
CURRENT_LOADED_Y = -1
CURRENT_LOADED_NAME = "No Coordinates Loaded"
INDEX = -1
SAVE_LIST = []

BACKGROUND_CLR = "#281B30"
DEFAULT_SCREEN_SIZE = "1280x720"
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720

ROOT = Tk(className= "Tomocliker")
HOME_FRAME = None
SAVE_FRAME = None
LOAD_FRAME = None
AUTOCLICK_FRAME = None
HOME_FRAME_MENU_ON = None
SAVE_FRAME_MENU_ON = None
LOAD_FRAME_MENU_ON = None
AUTOCLICK_FRAME_MENU_ON = None

LOGO_BUTTON_IMAGE = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "tomoclickerlogobuttonoff.png").subsample(4,4)
SAVE_COORDINATE_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "save_button.png").subsample(2,2)
FREE_AIM_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "free_aim_button.png").subsample(2,2)
AIM_LOCK_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "aim_lock_button.png").subsample(2,2)
HOME_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "home_button.png").subsample(4,4)
SAVE_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "save_image.png").subsample(4,4)
LOAD_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "load_image.png").subsample(4,4)
AUTOCLICK_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "TomoclickerLogo.png").subsample(4,4)
EXIT_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "exit_button.png").subsample(4,4)

FRAME_DICTIONARY = {
  HOME_FRAME: HOME_FRAME_MENU_ON,
  SAVE_FRAME: SAVE_FRAME_MENU_ON,
  LOAD_FRAME: LOAD_FRAME_MENU_ON,
  AUTOCLICK_FRAME: AUTOCLICK_FRAME_MENU_ON 
}

CURRENT_FRAME = HOME_FRAME

#FUNCTIONS
def accurate_click(x, y):
    pyautogui.move(x, y)

#NOTE bnum = 0x01 (means left click)
#NOTE bnum = 0x02 (means right click)
def detect_click(bnum):
    '''Waits for a mouse click. Returns True on click'''
    bnum = 0x01

    while 1:
        if ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
            # ^ this returns either 0 or 1 when button is not being held down
            while ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
                time.sleep(0.001)
            print("CLICK")
            return True
        time.sleep(0.001)

def continuous_print_coordinants_of_mouse():
    print('Press Ctrl-C to quit.')
    try:
        while 1:
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')

def get_mouse_placement_on_click():
    bnum = 0x01

    while 1:
        if ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
            # ^ this returns either 0 or 1 when button is not being held down
            while ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
                #while button is being held down
                time.sleep(0.001)
            return pyautogui.position()
        if ctypes.windll.user32.GetKeyState(0x1B) not in [0, 1]:
            return (-1, -1)
        time.sleep(0.001)

def auto_click_free_position(clicks_per_second):
    bnum = 0x01

    while 1:
        if ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
            # ^ this returns either 0 or 1 when button is not being held down
            while ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
                #while button is being held down
                while 1:
                    pyautogui.click(clicks=clicks_per_second)
                    if ctypes.windll.user32.GetKeyState(0x1B) not in [0, 1]:
                        return      

def auto_click_free_position_default():
    global ACTIVE_PROCESS_ON
    ACTIVE_PROCESS_ON = True
    
    bnum = 0x01

    while 1:
        if ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
            # ^ this returns either 0 or 1 when button is not being held down
            while ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
                #while button is being held down
                while 1:
                    pyautogui.click(clicks=30)
                    if ctypes.windll.user32.GetKeyState(0x1B) not in [0, 1]:
                        ACTIVE_PROCESS_ON = False
                        return
            
def start_auto_click_free_mode_thread():
    if (not ACTIVE_PROCESS_ON):
        threading.Thread(target=auto_click_free_position_default, daemon=True).start()  
    

#NOTE:MUST GIVE FEEDBACK IF POSITION IS NOT VALID
def auto_click_set_position(clicks_per_second):
    global ACTIVE_PROCESS_ON
    ACTIVE_PROCESS_ON = True
    if (INDEX != -1):
        time.sleep(2)
        while 1:
            pyautogui.click(clicks=clicks_per_second, x=CURRENT_LOADED_X, y=CURRENT_LOADED_Y)
            if ctypes.windll.user32.GetKeyState(0x1B) not in [0, 1]:
                break
    ACTIVE_PROCESS_ON = False

#NOTE:MUST GIVE FEEDBACK IF POSITION IS NOT VALID
def auto_click_set_position_default():
    global ACTIVE_PROCESS_ON
    ACTIVE_PROCESS_ON = True
    if (INDEX != -1):
        time.sleep(2)
        while 1:
            pyautogui.click(clicks=30, x=CURRENT_LOADED_X, y=CURRENT_LOADED_Y)
            if ctypes.windll.user32.GetKeyState(0x1B) not in [0, 1]:
                break
    ACTIVE_PROCESS_ON = False

def start_auto_click_aim_mode_thread():
    if (not ACTIVE_PROCESS_ON):
        threading.Thread(target=auto_click_set_position_default, daemon=True).start()  

#SAVE COORDINATE BASED ON WHERE YOU CLICK ON THE SCREEN
def save_new_coordinate():
    global ACTIVE_PROCESS_ON
    ACTIVE_PROCESS_ON = True
    coordinates_tuple = get_mouse_placement_on_click()
    if coordinates_tuple[0] != -1 and coordinates_tuple[1] != -1:
        #pop up window if valid save:
        save_popup_root = Tk(className= "Input save name")

        #sets background color
        save_popup_root.configure(bg=BACKGROUND_CLR)

        #sets window size
        save_popup_root.geometry("640x50")
        save_popup_root.minsize(640, 50)
        save_popup_root.maxsize(640, 50)

        save_text_entry_box = Entry(save_popup_root, bd=5, width=50)
        save_text_entry_box.place(x=5,y=10) 
        Button(save_popup_root, text="save", width=10, command=lambda: perform_save(coordinates_tuple, save_text_entry_box.get(), save_popup_root)).place(x=437, y=10)
        Button(save_popup_root, text="cancel", width=10, command=save_popup_root.destroy).place(x=537, y=10)
         
        save_popup_root.mainloop()

        
    #USER PRESSED ESC:
    ACTIVE_PROCESS_ON = False

def perform_save(coordinates_tuple, save_name, pop_up_window):
    with open(SAVE_FILE_PATH, "a") as myfile:
            myfile.write(str(coordinates_tuple[0]) + "," + str(coordinates_tuple[1]) + "," + save_name + "\n")
            SAVE_LIST.append([coordinates_tuple[0], coordinates_tuple[1], save_name])
    pop_up_window.destroy()

def start_save_thread():
    if (not ACTIVE_PROCESS_ON):
        threading.Thread(target=save_new_coordinate, daemon=True).start()  #ADD TARGET

def load_coordinate_by_index_file(index):
    temp_index = 0
    with open(SAVE_FILE_PATH, "r") as myfile:
        try:
            while (temp_index <= index):
                save = myfile.readline()
                temp_index += 1
            x_y_name = save.split(",")
            global CURRENT_LOADED_X, CURRENT_LOADED_Y, CURRENT_LOADED_NAME, INDEX
            CURRENT_LOADED_X = x_y_name[0]
            CURRENT_LOADED_Y = x_y_name[1]
            CURRENT_LOADED_NAME = x_y_name[2]
            INDEX = temp_index

        except:
            print("invalid index")
            #INDEX NOT VALID
            print("SAVE NOT FOUND")

def load_coordinate_by_index_list(index):
    try:
        return SAVE_LIST[index]
    except:
        print("INVALID INDEX")

def load_coordinate_by_name(save_name):
    temp_index = 0
    with open(SAVE_FILE_PATH, "r") as myfile:
        for save in myfile:
            x_y_name = save.split(",")
            if x_y_name[2] == save_name:
                global CURRENT_LOADED_X, CURRENT_LOADED_Y, CURRENT_LOADED_NAME, INDEX
                CURRENT_LOADED_X = x_y_name[0]
                CURRENT_LOADED_Y = x_y_name[1]
                CURRENT_LOADED_NAME = x_y_name[2]
                INDEX = temp_index

                break
            temp_index += 1
        #CASE: FILE NOT FOUND GIVE FEEDBACK
        print("SAVE NOT FOUND")

def load_save_list():
    save_list = []
    with open(SAVE_FILE_PATH, "r+") as myfile:
        for save in myfile:
            x_y_name = save.split(",")
            save_list.append(x_y_name)
    return save_list
    

def update_saved_coordinate(index, new_x, new_y, new_name):
    new_save = [new_x, new_y, new_name + "\n"]
    try:
        SAVE_LIST[index] = new_save
        save_list_to_file()
    except:
        print("INVALID INDEX")

def save_list_to_file():
    with open(SAVE_FILE_PATH, "w") as myfile:
        for save in SAVE_LIST:
            myfile.write(str(save[0]) + "," + str(save[1]) + "," + save[2])


def delete_coordinate(index_to_be_deleted):
    SAVE_LIST.remove(SAVE_LIST[index_to_be_deleted])
    save_list_to_file()


def toggle_draw_menu():
    global MENU_TOGGLE_ON
    MENU_TOGGLE_ON = not MENU_TOGGLE_ON


def reset_loaded_coordinates():
    global CURRENT_LOADED_X, CURRENT_LOADED_Y, CURRENT_LOADED_NAME, INDEX
    CURRENT_LOADED_X = -1
    CURRENT_LOADED_Y = -1
    CURRENT_LOADED_NAME = "No Coordinates Loaded"
    INDEX = -1 

def draw_body():
    global CURRENT_FRAME, FRAME_DICTIONARY
    #toggles the draw menu config
    toggle_draw_menu()

    CURRENT_FRAME.pack_forget()

    if (MENU_TOGGLE_ON):
        CURRENT_FRAME = FRAME_DICTIONARY[CURRENT_FRAME]
    
    else:
        CURRENT_FRAME = list(FRAME_DICTIONARY.keys())[list(FRAME_DICTIONARY.values()).index(CURRENT_FRAME)]

    CURRENT_FRAME.pack(anchor='nw', fill=BOTH, expand=True, side=LEFT)

def draw_home():
    global HOME_FRAME_MENU_ON, CURRENT_FRAME
    if (CURRENT_FRAME != HOME_FRAME_MENU_ON):
        CURRENT_FRAME.pack_forget()
        CURRENT_FRAME = HOME_FRAME_MENU_ON
        CURRENT_FRAME.pack(anchor='nw', fill=BOTH, expand=True, side=LEFT)


def draw_save():
    global SAVE_FRAME_MENU_ON, CURRENT_FRAME
    if (CURRENT_FRAME != SAVE_FRAME_MENU_ON):
        CURRENT_FRAME.pack_forget()
        CURRENT_FRAME = SAVE_FRAME_MENU_ON
        CURRENT_FRAME.pack(anchor='nw', fill=BOTH, expand=True, side=LEFT)

def draw_load():
    global LOAD_FRAME_MENU_ON, CURRENT_FRAME
    if (CURRENT_FRAME != LOAD_FRAME_MENU_ON):
        CURRENT_FRAME.pack_forget()
        CURRENT_FRAME = LOAD_FRAME_MENU_ON
        CURRENT_FRAME.pack(anchor='nw', fill=BOTH, expand=True, side=LEFT)

def draw_autoclick():
    global AUTOCLICK_FRAME_MENU_ON, CURRENT_FRAME
    if (CURRENT_FRAME != AUTOCLICK_FRAME_MENU_ON):
        CURRENT_FRAME.pack_forget()
        CURRENT_FRAME = AUTOCLICK_FRAME_MENU_ON
        CURRENT_FRAME.pack(anchor='nw', fill=BOTH, expand=True, side=LEFT)

def draw_home_page():
    global ROOT, VERSION, BACKGROUND_CLR, DEFAULT_WIDTH, DEFAULT_HEIGHT, CURRENT_LOADED_X, CURRENT_LOADED_Y, CURRENT_LOADED_NAME, LOGO_BUTTON_IMAGE

    home_frame = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)

    #sets header (text, font, color, background color, position)
    #draws the header line
    Label(home_frame, text="", font=("GillSans", 1), bg="#E85295", height=0, width=DEFAULT_WIDTH).place(x=0, y=93)
    Label(home_frame, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
    Label(home_frame, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
    Label(home_frame, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
    Label(home_frame, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)

    #sets logo button in top left
    Button(home_frame, height=80, width=80, image=LOGO_BUTTON_IMAGE, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)

    #draws body
    Label(home_frame, text="Welcome to Tomoclicker: ", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=20).place(x=10, y=110)
    Label(home_frame, text="THE NUMBER ONE AUTOCLICKER APPLICATION", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=40).place(x=500, y=125)

    Label(home_frame, text="Getting Started:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=20).place(x=60, y=180)
    Label(home_frame, text="Select the logo on the top left to access the naviguation menu", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=230)

    Label(home_frame, text="Tomoclicker currently supports:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=30).place(x=60, y=300)
    Label(home_frame, text="-Free Aim Autoclicking (Free Aim Mode)", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=30).place(x=100, y=350)
    Label(home_frame, text="-Coordinate Based Autoclicking (Aim Lock Mode)", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=40).place(x=100, y=400)
    Label(home_frame, text="-Saving/Loading/Deleting Coordinates", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=29).place(x=100, y=450)

    #draws footer
    Label(home_frame, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
    Label(home_frame, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
    Label(home_frame, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
    Label(home_frame, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
    Label(home_frame, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)

    return home_frame

def draw_save_page():
    global ROOT, VERSION, BACKGROUND_CLR, DEFAULT_WIDTH, DEFAULT_HEIGHT, CURRENT_LOADED_X, CURRENT_LOADED_Y, CURRENT_LOADED_NAME, LOGO_BUTTON_IMAGE

    save_frame = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)

    #sets header (text, font, color, background color, position)
    #draws the header line
    Label(save_frame, text="", font=("GillSans", 1), bg="#E85295", height=0, width=DEFAULT_WIDTH).place(x=0, y=93)
    Label(save_frame, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
    Label(save_frame, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
    Label(save_frame, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
    Label(save_frame, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)

    #sets logo button in top left
    Button(save_frame, height=80, width=80, image=LOGO_BUTTON_IMAGE, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)

    #SAVE
    Label(save_frame, text="SAVE", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=5).place(x=10, y=110)
    Label(save_frame, text="Instructions:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=60, y=180)
    Label(save_frame, text="Press the save button to start saving process, afterwards position the cursor ", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=230)
    Label(save_frame, text="wherever you would like to save. When ready, left click at the target coordinate", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=260)
    Label(save_frame, text="to store it. You will also be prompted to input a save name.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=290)
    Button(save_frame, height=80, width=180, image=SAVE_COORDINATE_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_save_thread).place(x=530, y=400)

    #draws footer
    Label(save_frame, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
    Label(save_frame, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
    Label(save_frame, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
    Label(save_frame, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
    Label(save_frame, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)

    return save_frame

def draw_load_page():
    global ROOT, VERSION, BACKGROUND_CLR, DEFAULT_WIDTH, DEFAULT_HEIGHT, CURRENT_LOADED_X, CURRENT_LOADED_Y, CURRENT_LOADED_NAME, LOGO_BUTTON_IMAGE

    load_frame = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)

    #sets header (text, font, color, background color, position)
    #draws the header line
    Label(load_frame, text="", font=("GillSans", 1), bg="#E85295", height=0, width=DEFAULT_WIDTH).place(x=0, y=93)
    Label(load_frame, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
    Label(load_frame, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
    Label(load_frame, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
    Label(load_frame, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)

    #sets logo button in top left
    Button(load_frame, height=80, width=80, image=LOGO_BUTTON_IMAGE, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)

    #draws body TODO

    #draws footer
    Label(load_frame, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
    Label(load_frame, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
    Label(load_frame, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
    Label(load_frame, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
    Label(load_frame, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)

    return load_frame

def draw_autoclick_page():
    global ROOT, VERSION, BACKGROUND_CLR, DEFAULT_WIDTH, DEFAULT_HEIGHT, CURRENT_LOADED_X, CURRENT_LOADED_Y, CURRENT_LOADED_NAME, LOGO_BUTTON_IMAGE

    autoclick_frame = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)

    #sets header (text, font, color, background color, position)
    #draws the header line
    Label(autoclick_frame, text="", font=("GillSans", 1), bg="#E85295", height=0, width=DEFAULT_WIDTH).place(x=0, y=93)
    Label(autoclick_frame, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
    Label(autoclick_frame, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
    Label(autoclick_frame, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
    Label(autoclick_frame, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)

    #sets logo button in top left
    Button(autoclick_frame, height=80, width=80, image=LOGO_BUTTON_IMAGE, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)

    #draws body
    Label(autoclick_frame, text="AUTOCLICK", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=10).place(x=10, y=110)
    Label(autoclick_frame, text="Free Aim Mode:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=60, y=180)
    Label(autoclick_frame, text="Once Active, manually aim the cursor and when in position,", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=230)
    Label(autoclick_frame, text="left click to begin the autoclicker. Press \"esc\" key to stop.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=260)
    Button(autoclick_frame, height=80, width=180, image=FREE_AIM_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_auto_click_free_mode_thread).place(x=900, y=220)

    Label(autoclick_frame, text="Aim Lock Mode:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=60, y=400)
    Label(autoclick_frame, text="Load a saved coordinate, press the button to start autoclicking", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=450)
    Label(autoclick_frame, text="at the saved coordinate. Press \"esc\" key to stop.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=480)
    Button(autoclick_frame, height=80, width=180, image=AIM_LOCK_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_auto_click_aim_mode_thread).place(x=900, y=440)

    #draws footer
    Label(autoclick_frame, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
    Label(autoclick_frame, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
    Label(autoclick_frame, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
    Label(autoclick_frame, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
    Label(autoclick_frame, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)

    return autoclick_frame

def draw_home_page_menu():
    global ROOT, VERSION, BACKGROUND_CLR, DEFAULT_WIDTH, DEFAULT_HEIGHT, CURRENT_LOADED_X, CURRENT_LOADED_Y, CURRENT_LOADED_NAME, LOGO_BUTTON_IMAGE

    home_frame_menu_on = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)

    #draw menu
    Label(home_frame_menu_on, text="", font=("GillSans", 1), bg="#E85295", height=291, width=0).place(x=400, y=101)
    Label(home_frame_menu_on, bg="#27738e", text="", font=("GillSans", 1), height=291, width=398).place(x=0, y=101)

    #draw menu buttons
    Button(home_frame_menu_on, height=80, width=80, image=HOME_BUTTON, bg="#27739f", activebackground="#27739f", relief=SUNKEN, command=draw_home).place(x=5, y=110)
    Label(home_frame_menu_on, text="HOME", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=133)
    Button(home_frame_menu_on, height=80, width=80, image=SAVE_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_save).place(x=5, y=210)
    Label(home_frame_menu_on, text="SAVE", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=233)
    Button(home_frame_menu_on, height=80, width=80, image=LOAD_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_load).place(x=5, y=310)
    Label(home_frame_menu_on, text="LOAD", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=333)
    Button(home_frame_menu_on, height=80, width=80, image=AUTOCLICK_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_autoclick).place(x=5, y=410)
    Label(home_frame_menu_on, text="AUTOCLICK", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=10).place(x = 130, y=433)
    Button(home_frame_menu_on, height=80, width=80, image=EXIT_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=ROOT.destroy).place(x=5, y=600)
    Label(home_frame_menu_on, text="EXIT", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=623)

    #sets header (text, font, color, background color, position)
    #draws the header line
    Label(home_frame_menu_on, text="", font=("GillSans", 1), bg="#E85295", height=0, width=DEFAULT_WIDTH).place(x=0, y=93)
    Label(home_frame_menu_on, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
    Label(home_frame_menu_on, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
    Label(home_frame_menu_on, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
    Label(home_frame_menu_on, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)

    #sets logo button in top left
    Button(home_frame_menu_on, height=80, width=80, image=LOGO_BUTTON_IMAGE, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)

    #draws body
    Label(home_frame_menu_on, text="Welcome to Tomoclicker: ", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=20).place(x=420, y=110)
    Label(home_frame_menu_on, text="THE NUMBER ONE AUTOCLICKER APPLICATION", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=40).place(x=420, y=155)

    Label(home_frame_menu_on, text="Getting Started:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=20).place(x=450, y=210)
    Label(home_frame_menu_on, text="Select the logo on the top left to access the naviguation menu", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=250)

    Label(home_frame_menu_on, text="Tomoclicker currently supports:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=30).place(x=450, y=320)
    Label(home_frame_menu_on, text="-Free Aim Autoclicking (Free Aim Mode)", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=30).place(x=490, y=370)
    Label(home_frame_menu_on, text="-Coordinate Based Autoclicking (Aim Lock Mode)", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=40).place(x=490, y=420)
    Label(home_frame_menu_on, text="-Saving/Loading/Deleting Coordinates", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=29).place(x=490, y=470)

    #draws footer
    Label(home_frame_menu_on, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
    Label(home_frame_menu_on, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
    Label(home_frame_menu_on, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
    Label(home_frame_menu_on, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
    Label(home_frame_menu_on, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)

    return home_frame_menu_on

def draw_save_page_menu():
    global ROOT, VERSION, BACKGROUND_CLR, DEFAULT_WIDTH, DEFAULT_HEIGHT, CURRENT_LOADED_X, CURRENT_LOADED_Y, CURRENT_LOADED_NAME, LOGO_BUTTON_IMAGE

    save_frame_menu_on = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)

    #draw menu
    Label(save_frame_menu_on, text="", font=("GillSans", 1), bg="#E85295", height=291, width=0).place(x=400, y=101)
    Label(save_frame_menu_on, bg="#27738e", text="", font=("GillSans", 1), height=291, width=398).place(x=0, y=101)

    #draw menu buttons
    Button(save_frame_menu_on, height=80, width=80, image=HOME_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_home).place(x=5, y=110)
    Label(save_frame_menu_on, text="HOME", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=133)
    Button(save_frame_menu_on, height=80, width=80, image=SAVE_BUTTON, bg="#27739f", activebackground="#27739f", relief=SUNKEN, command=draw_save).place(x=5, y=210)
    Label(save_frame_menu_on, text="SAVE", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=233)
    Button(save_frame_menu_on, height=80, width=80, image=LOAD_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_load).place(x=5, y=310)
    Label(save_frame_menu_on, text="LOAD", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=333)
    Button(save_frame_menu_on, height=80, width=80, image=AUTOCLICK_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_autoclick).place(x=5, y=410)
    Label(save_frame_menu_on, text="AUTOCLICK", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=10).place(x = 130, y=433)
    Button(save_frame_menu_on, height=80, width=80, image=EXIT_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=ROOT.destroy).place(x=5, y=600)
    Label(save_frame_menu_on, text="EXIT", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=623)

    #sets header (text, font, color, background color, position)
    #draws the header line
    Label(save_frame_menu_on, text="", font=("GillSans", 1), bg="#E85295", height=0, width=DEFAULT_WIDTH).place(x=0, y=93)
    Label(save_frame_menu_on, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
    Label(save_frame_menu_on, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
    Label(save_frame_menu_on, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
    Label(save_frame_menu_on, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)

    #sets logo button in top left
    Button(save_frame_menu_on, height=80, width=80, image=LOGO_BUTTON_IMAGE, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)

    #draws body
    Label(save_frame_menu_on, text="SAVE", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=5).place(x=420, y=110)
    Label(save_frame_menu_on, text="Instructions:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=450, y=180)
    Label(save_frame_menu_on, text="Press the save button to start saving process, afterwards position", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=230)
    Label(save_frame_menu_on, text="the cursor wherever you would like to save. ", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=260)
    Label(save_frame_menu_on, text="When ready, left click at the target coordinate to store it.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=290)
    Label(save_frame_menu_on, text="You will also be prompted to input a save name.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=320)
    Button(save_frame_menu_on, height=80, width=180, image=SAVE_COORDINATE_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_save_thread).place(x=740, y=400)

    #draws footer
    Label(save_frame_menu_on, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
    Label(save_frame_menu_on, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
    Label(save_frame_menu_on, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
    Label(save_frame_menu_on, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
    Label(save_frame_menu_on, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)

    return save_frame_menu_on

def draw_load_page_menu():
    global ROOT, VERSION, BACKGROUND_CLR, DEFAULT_WIDTH, DEFAULT_HEIGHT, CURRENT_LOADED_X, CURRENT_LOADED_Y, CURRENT_LOADED_NAME, LOGO_BUTTON_IMAGE

    load_frame_menu_on = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)

    #draw menu
    Label(load_frame_menu_on, text="", font=("GillSans", 1), bg="#E85295", height=291, width=0).place(x=400, y=101)
    Label(load_frame_menu_on, bg="#27738e", text="", font=("GillSans", 1), height=291, width=398).place(x=0, y=101)

    #draw menu buttons
    Button(load_frame_menu_on, height=80, width=80, image=HOME_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_home).place(x=5, y=110)
    Label(load_frame_menu_on, text="HOME", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=133)
    Button(load_frame_menu_on, height=80, width=80, image=SAVE_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_save).place(x=5, y=210)
    Label(load_frame_menu_on, text="SAVE", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=233)
    Button(load_frame_menu_on, height=80, width=80, image=LOAD_BUTTON, bg="#27739f", activebackground="#27739f", relief=SUNKEN, command=draw_load).place(x=5, y=310)
    Label(load_frame_menu_on, text="LOAD", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=333)
    Button(load_frame_menu_on, height=80, width=80, image=AUTOCLICK_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_autoclick).place(x=5, y=410)
    Label(load_frame_menu_on, text="AUTOCLICK", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=10).place(x = 130, y=433)
    Button(load_frame_menu_on, height=80, width=80, image=EXIT_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=ROOT.destroy).place(x=5, y=600)
    Label(load_frame_menu_on, text="EXIT", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=623)

    #sets header (text, font, color, background color, position)
    #draws the header line
    Label(load_frame_menu_on, text="", font=("GillSans", 1), bg="#E85295", height=0, width=DEFAULT_WIDTH).place(x=0, y=93)
    Label(load_frame_menu_on, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
    Label(load_frame_menu_on, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
    Label(load_frame_menu_on, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
    Label(load_frame_menu_on, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)

    #sets logo button in top left
    Button(load_frame_menu_on, height=80, width=80, image=LOGO_BUTTON_IMAGE, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)

    #draws body TODO

    #draws footer
    Label(load_frame_menu_on, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
    Label(load_frame_menu_on, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
    Label(load_frame_menu_on, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
    Label(load_frame_menu_on, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
    Label(load_frame_menu_on, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)

    return load_frame_menu_on

def draw_autoclick_page_menu():
    global ROOT, VERSION, BACKGROUND_CLR, DEFAULT_WIDTH, DEFAULT_HEIGHT, CURRENT_LOADED_X, CURRENT_LOADED_Y, CURRENT_LOADED_NAME, LOGO_BUTTON_IMAGE

    autoclick_frame_menu_on = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)

    #draw menu
    Label(autoclick_frame_menu_on, text="", font=("GillSans", 1), bg="#E85295", height=291, width=0).place(x=400, y=101)
    Label(autoclick_frame_menu_on, bg="#27738e", text="", font=("GillSans", 1), height=291, width=398).place(x=0, y=101)

    #draw menu buttons
    Button(autoclick_frame_menu_on, height=80, width=80, image=HOME_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_home).place(x=5, y=110)
    Label(autoclick_frame_menu_on, text="HOME", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=133)
    Button(autoclick_frame_menu_on, height=80, width=80, image=SAVE_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_save).place(x=5, y=210)
    Label(autoclick_frame_menu_on, text="SAVE", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=233)
    Button(autoclick_frame_menu_on, height=80, width=80, image=LOAD_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_load).place(x=5, y=310)
    Label(autoclick_frame_menu_on, text="LOAD", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=333)
    Button(autoclick_frame_menu_on, height=80, width=80, image=AUTOCLICK_BUTTON, bg="#27739f", activebackground="#27739f", relief=SUNKEN, command=draw_autoclick).place(x=5, y=410)
    Label(autoclick_frame_menu_on, text="AUTOCLICK", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=10).place(x = 130, y=433)
    Button(autoclick_frame_menu_on, height=80, width=80, image=EXIT_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=ROOT.destroy).place(x=5, y=600)
    Label(autoclick_frame_menu_on, text="EXIT", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=623)

    #sets header (text, font, color, background color, position)
    #draws the header line
    Label(autoclick_frame_menu_on, text="", font=("GillSans", 1), bg="#E85295", height=0, width=DEFAULT_WIDTH).place(x=0, y=93)
    Label(autoclick_frame_menu_on, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
    Label(autoclick_frame_menu_on, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
    Label(autoclick_frame_menu_on, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
    Label(autoclick_frame_menu_on, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)

    #sets logo button in top left
    Button(autoclick_frame_menu_on, height=80, width=80, image=LOGO_BUTTON_IMAGE, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)

    #draws body
    Label(autoclick_frame_menu_on, text="AUTOCLICK", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=10).place(x=420, y=110)
    Label(autoclick_frame_menu_on, text="Free Aim Mode:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=450, y=180)
    Label(autoclick_frame_menu_on, text="Once Active, manually aim the cursor and when in position,", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=230)
    Label(autoclick_frame_menu_on, text="left click to begin the autoclicker. Press \"esc\" key to stop.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=260)
    Button(autoclick_frame_menu_on, height=80, width=180, image=FREE_AIM_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_auto_click_free_mode_thread).place(x=730, y=320)

    Label(autoclick_frame_menu_on, text="Aim Lock Mode:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=450, y=440)
    Label(autoclick_frame_menu_on, text="Load a saved coordinate, press the button to start autoclicking", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=490)
    Label(autoclick_frame_menu_on, text="at the saved coordinate. Press \"esc\" key to stop.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=520)
    Button(autoclick_frame_menu_on, height=80, width=180, image=AIM_LOCK_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_auto_click_aim_mode_thread).place(x=730, y=580)

    #draws footer
    Label(autoclick_frame_menu_on, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
    Label(autoclick_frame_menu_on, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
    Label(autoclick_frame_menu_on, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
    Label(autoclick_frame_menu_on, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
    Label(autoclick_frame_menu_on, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)

    return autoclick_frame_menu_on




#START OF SCRIPT

#loads all saves to global variable
SAVE_LIST = load_save_list()

#sets window icon
ROOT.iconphoto(True, LOGO_BUTTON_IMAGE)

#sets background color
ROOT.configure(bg=BACKGROUND_CLR)

#sets window size
ROOT.geometry(DEFAULT_SCREEN_SIZE)
ROOT.minsize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
ROOT.maxsize(DEFAULT_WIDTH, DEFAULT_HEIGHT)


AUTOCLICK_FRAME_MENU_ON = draw_autoclick_page_menu()
LOAD_FRAME_MENU_ON = draw_load_page_menu()
SAVE_FRAME_MENU_ON = draw_save_page_menu()
HOME_FRAME_MENU_ON = draw_home_page_menu()
AUTOCLICK_FRAME = draw_autoclick_page()
LOAD_FRAME = draw_load_page()
SAVE_FRAME = draw_save_page()
HOME_FRAME = draw_home_page()
HOME_FRAME.pack(anchor='nw', fill=BOTH, expand=True, side=LEFT)

#sets the home as the current frame
CURRENT_FRAME = HOME_FRAME

#sets the frame dictionary
FRAME_DICTIONARY = {
  HOME_FRAME: HOME_FRAME_MENU_ON,
  SAVE_FRAME: SAVE_FRAME_MENU_ON,
  LOAD_FRAME: LOAD_FRAME_MENU_ON,
  AUTOCLICK_FRAME: AUTOCLICK_FRAME_MENU_ON 
}

ROOT.mainloop()
