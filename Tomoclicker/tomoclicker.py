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
LOGO_FILE_PATH = CURRENT_WORKING_DIRECTORY + "\\resources\\" + "TomoclickerLogo.png"
LOGO_BUTTON_OFF_IMAGE = CURRENT_WORKING_DIRECTORY + "\\resources\\" + "tomoclickerlogobuttonoff.png"
LOGO_BUTTON_ON_IMAGE = CURRENT_WORKING_DIRECTORY + "\\resources\\" + "tomoclickerlogobuttonon.png"
SAVE_BUTTON_IMAGE = CURRENT_WORKING_DIRECTORY + "\\resources\\" + "save_image.png"
LOAD_BUTTON_IMAGE = CURRENT_WORKING_DIRECTORY + "\\resources\\" + "load_image.png"
HOME_BUTTON_IMAGE = CURRENT_WORKING_DIRECTORY + "\\resources\\" + "home_button.png"
EXIT_BUTTON_IMAGE = CURRENT_WORKING_DIRECTORY + "\\resources\\" + "exit_button.png"
FREE_AIM_BUTTON_IMAGE = CURRENT_WORKING_DIRECTORY + "\\resources\\" + "free_aim_button.png"
AIM_LOCK_BUTTON_IMAGE = CURRENT_WORKING_DIRECTORY + "\\resources\\" + "aim_lock_button.png"

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

ROOT = None
HOME_FRAME = None
SAVE_FRAME = None
LOAD_FRAME = None
AUTOCLICK_FRAME = None
HOME_FRAME_MENU_ON = None
SAVE_FRAME_MENU_ON = None
LOAD_FRAME_MENU_ON = None
AUTOCLICK_FRAME_MENU_ON = None

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
                ACTIVE_PROCESS_ON = False
                break

#NOTE:MUST GIVE FEEDBACK IF POSITION IS NOT VALID
def auto_click_set_position_default():
    global ACTIVE_PROCESS_ON
    ACTIVE_PROCESS_ON = True
    if (INDEX != -1):
        time.sleep(2)
        while 1:
            pyautogui.click(clicks=30, x=CURRENT_LOADED_X, y=CURRENT_LOADED_Y)
            if ctypes.windll.user32.GetKeyState(0x1B) not in [0, 1]:
                ACTIVE_PROCESS_ON = False
                break

def start_auto_click_aim_mode_thread():
    if (not ACTIVE_PROCESS_ON):
        threading.Thread(target=auto_click_set_position_default, daemon=True).start()  

#SAVE COORDINATE BASED ON WHERE YOU CLICK ON THE SCREEN
def save_new_coordinate():
    coordinates_tuple = get_mouse_placement_on_click()
    if coordinates_tuple[0] != -1 and coordinates_tuple[1] != -1:
        save_name = input('Please enter the name for this save file:\n')
        with open(SAVE_FILE_PATH, "a") as myfile:
            myfile.write(str(coordinates_tuple[0]) + "," + str(coordinates_tuple[1]) + "," + save_name + "\n")
            SAVE_LIST.append([coordinates_tuple[0], coordinates_tuple[1], save_name])
    #USER PRESSED ESC:
    print("Coordination Save Cancelled\n")

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



#START OF SCRIPT

#loads all saves to global variable
SAVE_LIST = load_save_list()

#creates window and sets window name
ROOT = Tk(className= "Tomocliker")

HOME_FRAME = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
SAVE_FRAME = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
LOAD_FRAME = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
AUTOCLICK_FRAME = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
HOME_FRAME_MENU_ON = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
SAVE_FRAME_MENU_ON = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
LOAD_FRAME_MENU_ON = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
AUTOCLICK_FRAME_MENU_ON = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)

#draw menu
Label(HOME_FRAME_MENU_ON, text="", font=("GillSans", 1), bg="#E85295", height=291, width=0).place(x=400, y=101)
Label(HOME_FRAME_MENU_ON, bg="#27738e", text="", font=("GillSans", 1), height=291, width=398).place(x=0, y=101)

Label(SAVE_FRAME_MENU_ON, text="", font=("GillSans", 1), bg="#E85295", height=291, width=0).place(x=400, y=101)
Label(SAVE_FRAME_MENU_ON, bg="#27738e", text="", font=("GillSans", 1), height=291, width=398).place(x=0, y=101)

Label(LOAD_FRAME_MENU_ON, text="", font=("GillSans", 1), bg="#E85295", height=291, width=0).place(x=400, y=101)
Label(LOAD_FRAME_MENU_ON, bg="#27738e", text="", font=("GillSans", 1), height=291, width=398).place(x=0, y=101)

Label(AUTOCLICK_FRAME_MENU_ON, text="", font=("GillSans", 1), bg="#E85295", height=291, width=0).place(x=400, y=101)
Label(AUTOCLICK_FRAME_MENU_ON, bg="#27738e", text="", font=("GillSans", 1), height=291, width=398).place(x=0, y=101)

#draw menu buttons
home_button_image = PhotoImage(file=HOME_BUTTON_IMAGE).subsample(4,4)
save_button_image = PhotoImage(file=SAVE_BUTTON_IMAGE).subsample(4,4)
load_button_image = PhotoImage(file=LOAD_BUTTON_IMAGE).subsample(4,4)
click_button_image = PhotoImage(file=LOGO_FILE_PATH).subsample(4,4)
exit_button_image = PhotoImage(file=EXIT_BUTTON_IMAGE).subsample(4,4)

Button(HOME_FRAME_MENU_ON, height=80, width=80, image=home_button_image, bg="#27739f", activebackground="#27739f", relief=SUNKEN, command=draw_home).place(x=5, y=110)
Label(HOME_FRAME_MENU_ON, text="HOME", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=113)
Button(HOME_FRAME_MENU_ON, height=80, width=80, image=save_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_save).place(x=5, y=210)
Label(HOME_FRAME_MENU_ON, text="SAVE", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=213)
Button(HOME_FRAME_MENU_ON, height=80, width=80, image=load_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_load).place(x=5, y=310)
Label(HOME_FRAME_MENU_ON, text="LOAD", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=313)
Button(HOME_FRAME_MENU_ON, height=80, width=80, image=click_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_autoclick).place(x=5, y=410)
Label(HOME_FRAME_MENU_ON, text="AUTOCLICK", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=10).place(x = 130, y=413)
Button(HOME_FRAME_MENU_ON, height=80, width=80, image=exit_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=ROOT.destroy).place(x=5, y=600)
Label(HOME_FRAME_MENU_ON, text="EXIT", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=603)

Button(SAVE_FRAME_MENU_ON, height=80, width=80, image=home_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_home).place(x=5, y=110)
Label(SAVE_FRAME_MENU_ON, text="HOME", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=113)
Button(SAVE_FRAME_MENU_ON, height=80, width=80, image=save_button_image, bg="#27739f", activebackground="#27739f", relief=SUNKEN, command=draw_save).place(x=5, y=210)
Label(SAVE_FRAME_MENU_ON, text="SAVE", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=213)
Button(SAVE_FRAME_MENU_ON, height=80, width=80, image=load_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_load).place(x=5, y=310)
Label(SAVE_FRAME_MENU_ON, text="LOAD", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=313)
Button(SAVE_FRAME_MENU_ON, height=80, width=80, image=click_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_autoclick).place(x=5, y=410)
Label(SAVE_FRAME_MENU_ON, text="AUTOCLICK", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=10).place(x = 130, y=413)
Button(SAVE_FRAME_MENU_ON, height=80, width=80, image=exit_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=ROOT.destroy).place(x=5, y=600)
Label(SAVE_FRAME_MENU_ON, text="EXIT", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=603)

Button(LOAD_FRAME_MENU_ON, height=80, width=80, image=home_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_home).place(x=5, y=110)
Label(LOAD_FRAME_MENU_ON, text="HOME", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=113)
Button(LOAD_FRAME_MENU_ON, height=80, width=80, image=save_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_save).place(x=5, y=210)
Label(LOAD_FRAME_MENU_ON, text="SAVE", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=213)
Button(LOAD_FRAME_MENU_ON, height=80, width=80, image=load_button_image, bg="#27739f", activebackground="#27739f", relief=SUNKEN, command=draw_load).place(x=5, y=310)
Label(LOAD_FRAME_MENU_ON, text="LOAD", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=313)
Button(LOAD_FRAME_MENU_ON, height=80, width=80, image=click_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_autoclick).place(x=5, y=410)
Label(LOAD_FRAME_MENU_ON, text="AUTOCLICK", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=10).place(x = 130, y=413)
Button(LOAD_FRAME_MENU_ON, height=80, width=80, image=exit_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=ROOT.destroy).place(x=5, y=600)
Label(LOAD_FRAME_MENU_ON, text="EXIT", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=603)

Button(AUTOCLICK_FRAME_MENU_ON, height=80, width=80, image=home_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_home).place(x=5, y=110)
Label(AUTOCLICK_FRAME_MENU_ON, text="HOME", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=113)
Button(AUTOCLICK_FRAME_MENU_ON, height=80, width=80, image=save_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_save).place(x=5, y=210)
Label(AUTOCLICK_FRAME_MENU_ON, text="SAVE", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=213)
Button(AUTOCLICK_FRAME_MENU_ON, height=80, width=80, image=load_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_load).place(x=5, y=310)
Label(AUTOCLICK_FRAME_MENU_ON, text="LOAD", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=313)
Button(AUTOCLICK_FRAME_MENU_ON, height=80, width=80, image=click_button_image, bg="#27739f", activebackground="#27739f", relief=SUNKEN, command=draw_autoclick).place(x=5, y=410)
Label(AUTOCLICK_FRAME_MENU_ON, text="AUTOCLICK", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=10).place(x = 130, y=413)
Button(AUTOCLICK_FRAME_MENU_ON, height=80, width=80, image=exit_button_image, bg="#27738e", activebackground="#27739f", relief=FLAT, command=ROOT.destroy).place(x=5, y=600)
Label(AUTOCLICK_FRAME_MENU_ON, text="EXIT", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=603)


#sets window icon
logo = PhotoImage(file=LOGO_FILE_PATH)
ROOT.iconphoto(True, logo)

#sets background color
ROOT.configure(bg=BACKGROUND_CLR)

#sets window size
ROOT.geometry(DEFAULT_SCREEN_SIZE)
ROOT.minsize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
ROOT.maxsize(DEFAULT_WIDTH, DEFAULT_HEIGHT)

#sets header (text, font, color, background color, position)
Label(HOME_FRAME, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
Label(HOME_FRAME, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
Label(HOME_FRAME, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
Label(HOME_FRAME, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)
Label(HOME_FRAME_MENU_ON, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
Label(HOME_FRAME_MENU_ON, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
Label(HOME_FRAME_MENU_ON, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
Label(HOME_FRAME_MENU_ON, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)

Label(SAVE_FRAME, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
Label(SAVE_FRAME, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
Label(SAVE_FRAME, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
Label(SAVE_FRAME, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)
Label(SAVE_FRAME_MENU_ON, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
Label(SAVE_FRAME_MENU_ON, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
Label(SAVE_FRAME_MENU_ON, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
Label(SAVE_FRAME_MENU_ON, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)

Label(LOAD_FRAME, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
Label(LOAD_FRAME, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
Label(LOAD_FRAME, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
Label(LOAD_FRAME, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)
Label(LOAD_FRAME_MENU_ON, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
Label(LOAD_FRAME_MENU_ON, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
Label(LOAD_FRAME_MENU_ON, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
Label(LOAD_FRAME_MENU_ON, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)

Label(AUTOCLICK_FRAME, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
Label(AUTOCLICK_FRAME, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
Label(AUTOCLICK_FRAME, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
Label(AUTOCLICK_FRAME, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)
Label(AUTOCLICK_FRAME_MENU_ON, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=10).grid(row=0, column= 1)
Label(AUTOCLICK_FRAME_MENU_ON, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=51).place(x=0, y=0)
Label(AUTOCLICK_FRAME_MENU_ON, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
Label(AUTOCLICK_FRAME_MENU_ON, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)

#sets logo button in top left
logo_button_off_image = PhotoImage(file=LOGO_BUTTON_OFF_IMAGE).subsample(4,4)

#Button(ROOT, height=80, width=100, image=logo_button_off_image, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)

Button(HOME_FRAME, height=80, width=80, image=logo_button_off_image, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)
Button(HOME_FRAME_MENU_ON, height=80, width=80, image=logo_button_off_image, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)

Button(SAVE_FRAME, height=80, width=80, image=logo_button_off_image, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)
Button(SAVE_FRAME_MENU_ON, height=80, width=80, image=logo_button_off_image, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)

Button(LOAD_FRAME, height=80, width=80, image=logo_button_off_image, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)
Button(LOAD_FRAME_MENU_ON, height=80, width=80, image=logo_button_off_image, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)

Button(AUTOCLICK_FRAME, height=80, width=80, image=logo_button_off_image, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)
Button(AUTOCLICK_FRAME_MENU_ON, height=80, width=80, image=logo_button_off_image, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_body).place(x=2, y=5)

#draws the header line
header_canvas = Canvas(HOME_FRAME, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=1, highlightthickness=0)
header_canvas.create_line(0, 0, DEFAULT_WIDTH, 0, fill="#E85295")
header_canvas.grid(row=1)

header_canvas = Canvas(HOME_FRAME_MENU_ON, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=1, highlightthickness=0)
header_canvas.create_line(0, 0, DEFAULT_WIDTH, 0, fill="#E85295")
header_canvas.grid(row=1)

header_canvas = Canvas(SAVE_FRAME, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=1, highlightthickness=0)
header_canvas.create_line(0, 0, DEFAULT_WIDTH, 0, fill="#E85295")
header_canvas.grid(row=1)
header_canvas = Canvas(SAVE_FRAME_MENU_ON, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=1, highlightthickness=0)
header_canvas.create_line(0, 0, DEFAULT_WIDTH, 0, fill="#E85295")
header_canvas.grid(row=1)

header_canvas = Canvas(LOAD_FRAME, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=1, highlightthickness=0)
header_canvas.create_line(0, 0, DEFAULT_WIDTH, 0, fill="#E85295")
header_canvas.grid(row=1)
header_canvas = Canvas(LOAD_FRAME_MENU_ON, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=1, highlightthickness=0)
header_canvas.create_line(0, 0, DEFAULT_WIDTH, 0, fill="#E85295")
header_canvas.grid(row=1)

header_canvas = Canvas(AUTOCLICK_FRAME, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=1, highlightthickness=0)
header_canvas.create_line(0, 0, DEFAULT_WIDTH, 0, fill="#E85295")
header_canvas.grid(row=1)
header_canvas = Canvas(AUTOCLICK_FRAME_MENU_ON, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=1, highlightthickness=0)
header_canvas.create_line(0, 0, DEFAULT_WIDTH, 0, fill="#E85295")
header_canvas.grid(row=1)

#draws body
#HOME
Label(HOME_FRAME, text="Welcome to Tomoclicker: ", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=20).place(x=10, y=110)
Label(HOME_FRAME, text="THE NUMBER ONE AUTOCLICKER APPLICATION", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=40).place(x=500, y=125)

Label(HOME_FRAME, text="Getting Started:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=20).place(x=60, y=180)
Label(HOME_FRAME, text="Select the logo on the top left to access the naviguation menu", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=230)

Label(HOME_FRAME, text="Tomoclicker currently supports:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=30).place(x=60, y=300)
Label(HOME_FRAME, text="-Free Aim Autoclicking (Free Aim Mode)", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=30).place(x=100, y=350)
Label(HOME_FRAME, text="-Coordinate Based Autoclicking (Aim Lock Mode)", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=40).place(x=100, y=400)
Label(HOME_FRAME, text="-Saving/Loading/Deleting Coordinates", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=29).place(x=100, y=450)

Label(HOME_FRAME_MENU_ON, text="Welcome to Tomoclicker: ", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=20).place(x=420, y=110)
Label(HOME_FRAME_MENU_ON, text="THE NUMBER ONE AUTOCLICKER APPLICATION", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=40).place(x=420, y=155)

Label(HOME_FRAME_MENU_ON, text="Getting Started:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=20).place(x=450, y=210)
Label(HOME_FRAME_MENU_ON, text="Select the logo on the top left to access the naviguation menu", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=250)

Label(HOME_FRAME_MENU_ON, text="Tomoclicker currently supports:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=30).place(x=450, y=320)
Label(HOME_FRAME_MENU_ON, text="-Free Aim Autoclicking (Free Aim Mode)", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=30).place(x=490, y=370)
Label(HOME_FRAME_MENU_ON, text="-Coordinate Based Autoclicking (Aim Lock Mode)", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=40).place(x=490, y=420)
Label(HOME_FRAME_MENU_ON, text="-Saving/Loading/Deleting Coordinates", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=29).place(x=490, y=470)

#AUTOCLICK
free_aim_button_image = PhotoImage(file=FREE_AIM_BUTTON_IMAGE).subsample(2,2)
aim_lock_button_image = PhotoImage(file=AIM_LOCK_BUTTON_IMAGE).subsample(2,2)
Label(AUTOCLICK_FRAME, text="AUTOCLICK", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=10).place(x=10, y=110)
Label(AUTOCLICK_FRAME, text="Free Aim Mode:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=60, y=180)
Label(AUTOCLICK_FRAME, text="Once Active, manually aim the cursor and when in position,", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=230)
Label(AUTOCLICK_FRAME, text="left click to begin the autoclicker. Press \"esc\" key to stop.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=260)
Button(AUTOCLICK_FRAME, height=80, width=180, image=free_aim_button_image, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_auto_click_free_mode_thread).place(x=900, y=220)

Label(AUTOCLICK_FRAME, text="Aim Lock Mode:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=60, y=400)
Label(AUTOCLICK_FRAME, text="Load a saved coordinate, press the button to start autoclicking", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=450)
Label(AUTOCLICK_FRAME, text="at the saved coordinate. Press \"esc\" key to stop.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=480)
Button(AUTOCLICK_FRAME, height=80, width=180, image=aim_lock_button_image, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_auto_click_aim_mode_thread).place(x=900, y=440)

Label(AUTOCLICK_FRAME_MENU_ON, text="AUTOCLICK", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=10).place(x=420, y=110)
Label(AUTOCLICK_FRAME_MENU_ON, text="Free Aim Mode:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=450, y=180)
Label(AUTOCLICK_FRAME_MENU_ON, text="Once Active, manually aim the cursor and when in position,", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=230)
Label(AUTOCLICK_FRAME_MENU_ON, text="left click to begin the autoclicker. Press \"esc\" key to stop.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=260)
Button(AUTOCLICK_FRAME_MENU_ON, height=80, width=180, image=free_aim_button_image, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_auto_click_free_mode_thread).place(x=730, y=320)

Label(AUTOCLICK_FRAME_MENU_ON, text="Aim Lock Mode:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=450, y=440)
Label(AUTOCLICK_FRAME_MENU_ON, text="Load a saved coordinate, press the button to start autoclicking", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=490)
Label(AUTOCLICK_FRAME_MENU_ON, text="at the saved coordinate. Press \"esc\" key to stop.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=490, y=520)
Button(AUTOCLICK_FRAME_MENU_ON, height=80, width=180, image=aim_lock_button_image, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_auto_click_aim_mode_thread).place(x=730, y=580)

#SAVE



#draws footer
Label(HOME_FRAME, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
Label(HOME_FRAME, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
Label(HOME_FRAME, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
Label(HOME_FRAME, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
Label(HOME_FRAME, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)
Label(HOME_FRAME_MENU_ON, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
Label(HOME_FRAME_MENU_ON, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
Label(HOME_FRAME_MENU_ON, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
Label(HOME_FRAME_MENU_ON, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
Label(HOME_FRAME_MENU_ON, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)

Label(SAVE_FRAME, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
Label(SAVE_FRAME, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
Label(SAVE_FRAME, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
Label(SAVE_FRAME, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
Label(SAVE_FRAME, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)
Label(SAVE_FRAME_MENU_ON, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
Label(SAVE_FRAME_MENU_ON, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
Label(SAVE_FRAME_MENU_ON, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
Label(SAVE_FRAME_MENU_ON, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
Label(SAVE_FRAME_MENU_ON, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)

Label(LOAD_FRAME, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
Label(LOAD_FRAME, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
Label(LOAD_FRAME, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
Label(LOAD_FRAME, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
Label(LOAD_FRAME, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)
Label(LOAD_FRAME_MENU_ON, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
Label(LOAD_FRAME_MENU_ON, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
Label(LOAD_FRAME_MENU_ON, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
Label(LOAD_FRAME_MENU_ON, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
Label(LOAD_FRAME_MENU_ON, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)

Label(AUTOCLICK_FRAME, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
Label(AUTOCLICK_FRAME, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
Label(AUTOCLICK_FRAME, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
Label(AUTOCLICK_FRAME, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
Label(AUTOCLICK_FRAME, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)
Label(AUTOCLICK_FRAME_MENU_ON, text="", bg="#E85295", height=1, width=230).place(x=0, y=DEFAULT_HEIGHT - 31)
Label(AUTOCLICK_FRAME_MENU_ON, text="", bg="#624285", height=10, width=230).place(x=0, y=DEFAULT_HEIGHT - 30)
Label(AUTOCLICK_FRAME_MENU_ON, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=DEFAULT_HEIGHT - 30)
Label(AUTOCLICK_FRAME_MENU_ON, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=DEFAULT_HEIGHT - 30)
Label(AUTOCLICK_FRAME_MENU_ON, text="Save Name: " + CURRENT_LOADED_NAME, anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=DEFAULT_HEIGHT - 30)



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
