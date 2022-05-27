import pyautogui
import ctypes
import time 

import threading
from tkinter import *
from os import path

#https://www.mirametrics.com/help/mira_pro_script_8/source/getkeystate.htm 

#GLOBAL VARIABLE
VERSION = "1.0"

CURRENT_WORKING_DIRECTORY = path.dirname(__file__)
SAVE_FILE_PATH = CURRENT_WORKING_DIRECTORY + "\\resources\\" + "tomoclicker_save_file.txt"

MENU_TOGGLE_ON = False
ACTIVE_PROCESS_ON = False

BACKGROUND_CLR = "#281B30"
DEFAULT_SCREEN_SIZE = "1280x720"
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720

ROOT = Tk(className= "Tomocliker")
CURRENT_FRAME = None
HEADER_FRAME = None
MENU_FRAME = None
BODY_FRAME = None
MINI_BODY_FRAME = None
FOOTER_FRAME = None
CURRENT_FRAME_NAME = "N/A"

CURRENT_LOADED_X = -1
CURRENT_LOADED_Y = -1
CURRENT_LOADED_NAME = StringVar(ROOT)
CURRENT_LOADED_NAME.set("No Coordinates Loaded")
INDEX = -1
SAVE_LIST = []

LOGO_IMAGE = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "TomoclickerLogo.png")
LOGO_BUTTON_IMAGE = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "tomoclickerlogobuttonoff.png").subsample(4,4)
SAVE_COORDINATE_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "save_button.png").subsample(2,2)
FREE_AIM_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "free_aim_button.png").subsample(2,2)
AIM_LOCK_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "aim_lock_button.png").subsample(2,2)
HOME_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "home_button.png").subsample(4,4)
SAVE_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "save_image.png").subsample(4,4)
LOAD_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "load_image.png").subsample(4,4)
DELETE_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "delete_button.png").subsample(4,4)
AUTOCLICK_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "TomoclickerLogo.png").subsample(4,4)
EXIT_BUTTON = PhotoImage(file=CURRENT_WORKING_DIRECTORY + "\\resources\\" + "exit_button.png").subsample(4,4)

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
        bnum = 0x01

        while 1:
            if ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
                # ^ this returns either 0 or 1 when button is not being held down
                while ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
                    #while button is being held down
                    continue
                while 1:
                    pyautogui.click(clicks=clicks_per_second, x=CURRENT_LOADED_X, y=CURRENT_LOADED_Y)
                    if ctypes.windll.user32.GetKeyState(0x1B) not in [0, 1]:
                        ACTIVE_PROCESS_ON = False
                        return 
    

#NOTE:MUST GIVE FEEDBACK IF POSITION IS NOT VALID
def auto_click_set_position_default():
    global ACTIVE_PROCESS_ON
    ACTIVE_PROCESS_ON = True
    if (INDEX != -1):
        bnum = 0x01

        while 1:
            if ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
                # ^ this returns either 0 or 1 when button is not being held down
                while ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
                    #while button is being held down
                    while 1:
                        pyautogui.click(clicks=30, x=int(CURRENT_LOADED_X), y=int(CURRENT_LOADED_Y))
                        if ctypes.windll.user32.GetKeyState(0x1B) not in [0, 1]:
                            ACTIVE_PROCESS_ON = False
                            return
    

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
 
    #USER PRESSED ESC OR SAVE IS DONE:
    ACTIVE_PROCESS_ON = False

# TODO: Check to make sure that all characters are legal characters i.e: no "\n" or ":" AND GIVE FEEDBACK when save is invalid
def perform_save(coordinates_tuple, save_name, pop_up_window):
    if (1 <= len(save_name) <= 30 and save_name.replace(" ", "").isalnum()):
        if (not is_save_name_in_save_list(save_name)):
            with open(SAVE_FILE_PATH, "a") as myfile:
                    myfile.write(str(coordinates_tuple[0]) + "," + str(coordinates_tuple[1]) + "," + save_name + "\n")
                    SAVE_LIST.append([coordinates_tuple[0], coordinates_tuple[1], save_name])
            pop_up_window.destroy()

def start_save_thread():
    if (not ACTIVE_PROCESS_ON):
        threading.Thread(target=save_new_coordinate, daemon=True).start() 

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
            CURRENT_LOADED_NAME.set(x_y_name[2])
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
            if x_y_name[2].split('\n')[0] == save_name.split('\n')[0]:
                global CURRENT_LOADED_X, CURRENT_LOADED_Y, CURRENT_LOADED_NAME, INDEX
                CURRENT_LOADED_X = x_y_name[0]
                CURRENT_LOADED_Y = x_y_name[1]
                CURRENT_LOADED_NAME.set(x_y_name[2])
                INDEX = temp_index

                return 0
            temp_index += 1
        #CASE: FILE NOT FOUND GIVE FEEDBACK
        print("SAVE NOT FOUND")

def is_save_name_in_save_list(save_name):
    for save in SAVE_LIST:
        if (save[2] == save_name):
            return True
    return False        

def load_save_list():
    save_list = []
    with open(SAVE_FILE_PATH, "r+") as myfile:
        for save in myfile:
            x_y_name = save.split(",")
            save_list.append(x_y_name)
    return save_list
    
def build_save_list(load):
    load_save_list = []

    if (load):
        load_save_list.append("No Coordinates Loaded:                    (-1,-1)")
    else:
        load_save_list.append("No save selected")

    for save in SAVE_LIST:
        load_save_list.append(format_save_name(save))

    return load_save_list

def format_save_name(save):
    formatted_save_name = save[2] + ":"
    coordinate = "(" + str(save[0]) + "," + str(save[1]) + ")"
    spaces_to_add = 40 - len(formatted_save_name) - len(coordinate)

    while (spaces_to_add > 1):
        formatted_save_name += "  "
        spaces_to_add = spaces_to_add - 1

    formatted_save_name += coordinate

    return formatted_save_name

def update_current_loaded_save(*args):
    save_name = CURRENT_LOADED_NAME.get().split(":")[0]

    if (save_name != "No Coordinates Loaded"):
        load_coordinate_by_name(save_name)

    else:
        reset_loaded_coordinates()
        
    FOOTER_FRAME = draw_footer_frame()
    FOOTER_FRAME.place(x=0, y=DEFAULT_HEIGHT-31, anchor='nw')

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

def delete_coordinate_by_name(name_to_be_deleted, root):
    index=0
    for save in SAVE_LIST:
        if (save[2] == name_to_be_deleted):
            delete_coordinate_by_index(index)
            root.destroy()
            break
        index += index
    

def delete_coordinate_by_index(index_to_be_deleted):
    SAVE_LIST.remove(SAVE_LIST[index_to_be_deleted])
    save_list_to_file()

def delete_coordinate(name_to_be_deleted):
    global ACTIVE_PROCESS_ON, CURRENT_FRAME_NAME
    ACTIVE_PROCESS_ON = True

    #clean save_name
    name_to_be_deleted = name_to_be_deleted.split(":")[0]

    #pop up window if valid save:
    delete_popup_root = Tk(className= "Confirm Delete")

    #sets background color
    delete_popup_root.configure(bg=BACKGROUND_CLR)

    #sets window size
    delete_popup_root.geometry("300x50")
    delete_popup_root.minsize(300, 50)
    delete_popup_root.maxsize(300, 50)

    Button(delete_popup_root, text="Delete", width=10, command=lambda: delete_coordinate_by_name(name_to_be_deleted, delete_popup_root)).place(x=40, y=10)
    Button(delete_popup_root, text="cancel", width=10, command=delete_popup_root.destroy).place(x=170, y=10)
         
    delete_popup_root.mainloop()
    
    CURRENT_FRAME_NAME = "UpdateLoadScreen"
    draw_load()

    #USER PRESSED ESC OR SAVE IS DONE:
    ACTIVE_PROCESS_ON = False
    


def start_delete_save_thread(name_to_be_deleted):
    if (not ACTIVE_PROCESS_ON):
        threading.Thread(target=lambda: delete_coordinate(name_to_be_deleted), daemon=True).start() 


def toggle_draw_menu():
    global MENU_TOGGLE_ON
    MENU_TOGGLE_ON = not MENU_TOGGLE_ON


def reset_loaded_coordinates():
    global CURRENT_LOADED_X, CURRENT_LOADED_Y, CURRENT_LOADED_NAME, INDEX
    CURRENT_LOADED_X = -1
    CURRENT_LOADED_Y = -1
    CURRENT_LOADED_NAME.set("No Coordinates Loaded")
    INDEX = -1 

def draw_menu():
    #toggles the draw menu config
    toggle_draw_menu()

    if (MENU_TOGGLE_ON):
        MENU_FRAME.lift()
        MINI_BODY_FRAME.lift()
    
    else:
        MENU_FRAME.lower()
        BODY_FRAME.lift()


def draw_home():
    global  BODY_FRAME, MINI_BODY_FRAME, CURRENT_FRAME_NAME
    if (CURRENT_FRAME_NAME != "home"):
        BODY_FRAME.destroy()
        MINI_BODY_FRAME.destroy()

        CURRENT_FRAME_NAME = "home"
        BODY_FRAME = draw_home_page()
        MINI_BODY_FRAME = draw_home_page_menu()

        BODY_FRAME.place(x=0, y=101, anchor='nw')
        MINI_BODY_FRAME.place(x=405, y=110, anchor='nw')

        MENU_FRAME.lift()

def draw_save():
    global  BODY_FRAME, MINI_BODY_FRAME, CURRENT_FRAME_NAME
    if (CURRENT_FRAME_NAME != "save"):
        BODY_FRAME.destroy()
        MINI_BODY_FRAME.destroy()

        CURRENT_FRAME_NAME = "save"
        BODY_FRAME = draw_save_page()
        MINI_BODY_FRAME = draw_save_page_menu()

        BODY_FRAME.place(x=0, y=101, anchor='nw')
        MINI_BODY_FRAME.place(x=405, y=110, anchor='nw')

        MENU_FRAME.lift()
        

def draw_load():
    global  BODY_FRAME, MINI_BODY_FRAME, CURRENT_FRAME_NAME
    if (CURRENT_FRAME_NAME != "load"):
        BODY_FRAME.destroy()
        MINI_BODY_FRAME.destroy()

        CURRENT_FRAME_NAME = "load"
        BODY_FRAME = draw_load_page()
        MINI_BODY_FRAME = draw_load_page_menu()

        BODY_FRAME.place(x=0, y=101, anchor='nw')
        MINI_BODY_FRAME.place(x=405, y=110, anchor='nw')

        MENU_FRAME.lift()

def draw_autoclick():
    global  BODY_FRAME, MINI_BODY_FRAME, CURRENT_FRAME_NAME
    if (CURRENT_FRAME_NAME != "click"):
        BODY_FRAME.destroy()
        MINI_BODY_FRAME.destroy()

        CURRENT_FRAME_NAME = "click"
        BODY_FRAME = draw_autoclick_page()
        MINI_BODY_FRAME = draw_autoclick_page_menu()

        BODY_FRAME.place(x=0, y=101, anchor='nw')
        MINI_BODY_FRAME.place(x=405, y=110, anchor='nw')

        MENU_FRAME.lift()

def draw_home_page():
    home_frame = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=588)

    #draws body
    Label(home_frame, text="Welcome to Tomoclicker: ", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=20).place(x=10, y=9)
    Label(home_frame, text="THE NUMBER ONE AUTOCLICKER APPLICATION", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=40).place(x=500, y=24)

    Label(home_frame, text="Getting Started:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=20).place(x=60, y=79)
    Label(home_frame, text="Select the logo on the top left to access the naviguation menu", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=129)

    Label(home_frame, text="Tomoclicker currently supports:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=30).place(x=60, y=199)
    Label(home_frame, text="-Free Aim Autoclicking (Free Aim Mode)", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=30).place(x=100, y=249)
    Label(home_frame, text="-Coordinate Based Autoclicking (Aim Lock Mode)", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=40).place(x=100, y=299)
    Label(home_frame, text="-Saving/Loading/Deleting Coordinates", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=29).place(x=100, y=349)

    return home_frame

def draw_save_page():
    save_frame = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=588)

    #draws body
    Label(save_frame, text="SAVE", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=5).place(x=10, y=9)
    Label(save_frame, text="Instructions:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=60, y=79)
    Label(save_frame, text="Press the save button to start saving process, afterwards position the cursor ", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=129)
    Label(save_frame, text="wherever you would like to save. When ready, left click at the target coordinate", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=159)
    Label(save_frame, text="to store it. You will also be prompted to input a save name.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=189)
    Button(save_frame, height=80, width=180, image=SAVE_COORDINATE_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_save_thread).place(x=530, y=299)


    return save_frame

def draw_load_page():
    load_frame = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=588)

    #body resources
    save_to_be_deleted = StringVar(ROOT, value="Select Save to Delete")
    load_save_list = build_save_list(load=True)
    delete_save_list = build_save_list(load=False)
    list_of_saves_to_load = OptionMenu(load_frame, CURRENT_LOADED_NAME, *load_save_list)
    list_of_saves_to_delete = OptionMenu(load_frame, save_to_be_deleted, *delete_save_list)

    #draws body
    Label(load_frame, text="LOAD SAVE", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=10).place(x=10, y=9)
    Label(load_frame, text="Loading Coordinates:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=25).place(x=60, y=79)
    Label(load_frame, text="Select a save from the drop down menu if you have one ", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=45).place(x=100, y=129)
    Label(load_frame, text="or more coordinates saved.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=30).place(x=100, y=159)

    Label(load_frame, text="DELETE SAVE", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=15, y=330)
    Label(load_frame, text="Select the save you wish to delete from the drop down menu", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=45).place(x=85, y=400)
    Label(load_frame, text="and hit the delete button", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=30).place(x=85, y=430)
    Button(load_frame, height=40, width=80, image=DELETE_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=lambda: start_delete_save_thread(str(save_to_be_deleted.get()))).place(x=1140, y=405)

    list_of_saves_to_load.place(x=805, y=143)
    list_of_saves_to_delete.place(x=805, y=410)

    return load_frame

def draw_autoclick_page():
    autoclick_frame = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=588)

    #draws body
    Label(autoclick_frame, text="AUTOCLICK", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=10).place(x=10, y=9)
    Label(autoclick_frame, text="Free Aim Mode:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=60, y=79)
    Label(autoclick_frame, text="Once Active, manually aim the cursor and when in position,", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=129)
    Label(autoclick_frame, text="left click to begin the autoclicker. Press \"esc\" key to stop.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=159)
    Button(autoclick_frame, height=80, width=180, image=FREE_AIM_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_auto_click_free_mode_thread).place(x=900, y=119)

    Label(autoclick_frame, text="Aim Lock Mode:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=60, y=299)
    Label(autoclick_frame, text="Load a saved coordinate, press the button to start autoclicking", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=349)
    Label(autoclick_frame, text="at the saved coordinate. Press \"esc\" key to stop.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=100, y=379)
    Button(autoclick_frame, height=80, width=180, image=AIM_LOCK_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_auto_click_aim_mode_thread).place(x=900, y=339)

    return autoclick_frame

def draw_home_page_menu():
    home_frame_menu_on = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH - 405, height=579)

    #draws body
    Label(home_frame_menu_on, text="Welcome to Tomoclicker: ", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=20).place(x=15, y=0)
    Label(home_frame_menu_on, text="THE NUMBER ONE AUTOCLICKER APPLICATION", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=40).place(x=15, y=45)

    Label(home_frame_menu_on, text="Getting Started:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=20).place(x=45, y=100)
    Label(home_frame_menu_on, text="Select the logo on the top left to access the naviguation menu", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=85, y=140)

    Label(home_frame_menu_on, text="Tomoclicker currently supports:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=30).place(x=45, y=210)
    Label(home_frame_menu_on, text="-Free Aim Autoclicking (Free Aim Mode)", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=30).place(x=85, y=260)
    Label(home_frame_menu_on, text="-Coordinate Based Autoclicking (Aim Lock Mode)", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=40).place(x=85, y=310)
    Label(home_frame_menu_on, text="-Saving/Loading/Deleting Coordinates", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=29).place(x=85, y=360)

    return home_frame_menu_on

def draw_save_page_menu():
    save_frame_menu_on = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH - 405, height=579)

    #draws body
    Label(save_frame_menu_on, text="SAVE", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=5).place(x=15, y=0)
    Label(save_frame_menu_on, text="Instructions:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=45, y=70)
    Label(save_frame_menu_on, text="Press the save button to start saving process, afterwards position", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=85, y=120)
    Label(save_frame_menu_on, text="the cursor wherever you would like to save. ", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=85, y=150)
    Label(save_frame_menu_on, text="When ready, left click at the target coordinate to store it.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=85, y=180)
    Label(save_frame_menu_on, text="You will also be prompted to input a save name.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=85, y=210)
    Button(save_frame_menu_on, height=80, width=180, image=SAVE_COORDINATE_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_save_thread).place(x=335, y=290)

    return save_frame_menu_on

def draw_load_page_menu():
    load_frame_menu_on = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH - 405, height=579)

    #body resources
    save_to_be_deleted = StringVar(ROOT, value="Select Save to Delete")
    load_save_list = build_save_list(load=True)
    delete_save_list = build_save_list(load=False)
    list_of_saves_to_load = OptionMenu(load_frame_menu_on, CURRENT_LOADED_NAME, *load_save_list)
    list_of_saves_to_delete = OptionMenu(load_frame_menu_on, save_to_be_deleted, *delete_save_list)

    #draws body
    Label(load_frame_menu_on, text="LOAD SAVE", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=10).place(x=15, y=0)
    Label(load_frame_menu_on, text="Loading Coordinates:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=25).place(x=45, y=70)
    Label(load_frame_menu_on, text="Select a save from the drop down menu if you have one ", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=85, y=120)
    Label(load_frame_menu_on, text="or more coordinates saved.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=85, y=150)

    Label(load_frame_menu_on, text="DELETE SAVE", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=15, y=330)
    Label(load_frame_menu_on, text="Select the save you wish to delete from the drop down menu", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=85, y=380)
    Label(load_frame_menu_on, text="and hit the delete button", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=85, y=410)
    Button(load_frame_menu_on, height=40, width=80, image=DELETE_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=lambda: start_delete_save_thread(str(save_to_be_deleted.get()))).place(x=690, y=465)

    list_of_saves_to_load.place(x=355, y=250)
    list_of_saves_to_delete.place(x=355, y=470)

    return load_frame_menu_on

def draw_autoclick_page_menu():
    autoclick_frame_menu_on = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH - 405, height=579)

    #draws body
    Label(autoclick_frame_menu_on, text="AUTOCLICK", font=("Helvetica", 25), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=10).place(x=15, y=0)
    Label(autoclick_frame_menu_on, text="Free Aim Mode:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=45, y=70)
    Label(autoclick_frame_menu_on, text="Once Active, manually aim the cursor and when in position,", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=85, y=120)
    Label(autoclick_frame_menu_on, text="left click to begin the autoclicker. Press \"esc\" key to stop.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=85, y=150)
    Button(autoclick_frame_menu_on, height=80, width=180, image=FREE_AIM_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_auto_click_free_mode_thread).place(x=325, y=210)

    Label(autoclick_frame_menu_on, text="Aim Lock Mode:", font=("Helvetica", 20), anchor='nw', fg="white", bg=BACKGROUND_CLR, height=1, width=12).place(x=45, y=330)
    Label(autoclick_frame_menu_on, text="Load a saved coordinate, press the button to start autoclicking", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=85, y=380)
    Label(autoclick_frame_menu_on, text="at the saved coordinate. Press \"esc\" key to stop.", font=("Helvetica", 15), anchor='nw', fg="#FFC983", bg=BACKGROUND_CLR, height=1, width=60).place(x=85, y=410)
    Button(autoclick_frame_menu_on, height=80, width=180, image=AIM_LOCK_BUTTON, bg=BACKGROUND_CLR, activebackground=BACKGROUND_CLR, relief=FLAT, command=start_auto_click_aim_mode_thread).place(x=325, y=470)


    return autoclick_frame_menu_on

def draw_header_frame():
    header_frame = Frame(ROOT, bg=BACKGROUND_CLR, width=DEFAULT_WIDTH, height=100)

    #sets header (text, font, color, background color, position)

    Label(header_frame, text="", font=("GillSans", 25), fg="white", bg="#624285", height=2, width=DEFAULT_WIDTH).place(x=0, y=0)
    Label(header_frame, text="TOMOCLICKER", font=("AvenirNext", 25), fg="white", bg="#624285", height=2, width=20).place(x = 15, y=0)
    Label(header_frame, text="Version: " + VERSION, anchor='w', font=("AvenirNext", 10), fg="white", bg="#624285", height=2, width=10).place(x = 450, y=30)

    #draws the header line
    Label(header_frame, text="", font=("GillSans", 1), bg="#E85295", height=0, width=DEFAULT_WIDTH).place(x=0, y=99)

    #sets logo button in top left
    Button(header_frame, height=80, width=80, image=LOGO_BUTTON_IMAGE, bg="#624285", activebackground="#624290", relief=FLAT, command=draw_menu).place(x=2, y=5)

    return header_frame    

def draw_footer_frame():
    footer_frame = Frame(ROOT, width=DEFAULT_WIDTH, height=31)

    #draws footer
    Label(footer_frame, text="", bg="#E85295", height=1, width=230).place(x=0, y=0)
    Label(footer_frame, text="", bg="#624285", height=10, width=230).place(x=0, y=1)
    Label(footer_frame, text="X: " + str(CURRENT_LOADED_X), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 10, y=1)
    Label(footer_frame, text="Y: " + str(CURRENT_LOADED_Y), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=20).place(x = 300, y=1)
    Label(footer_frame, text="Save Name: " + CURRENT_LOADED_NAME.get(), anchor='nw', font=("AvenirNext", 15), fg="white", bg="#624285", height=1, width=200).place(x = 600, y=1)

    return footer_frame

def draw_menu_frame():
    menu_frame = Frame(ROOT, width=405, height=588)

    #draw menu
    Label(menu_frame, text="", font=("GillSans", 1), bg="#E85295", height=291, width=0).place(x=400, y=0)
    Label(menu_frame, bg="#27738e", text="", font=("GillSans", 1), height=291, width=398).place(x=0, y=0)
    

    #draw menu buttons
    Button(menu_frame, height=80, width=80, image=HOME_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_home).place(x=5, y=9)
    Label(menu_frame, text="HOME", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=32)
    Button(menu_frame, height=80, width=80, image=SAVE_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_save).place(x=5, y=109)
    Label(menu_frame, text="SAVE", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=132)
    Button(menu_frame, height=80, width=80, image=LOAD_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_load).place(x=5, y=209)
    Label(menu_frame, text="LOAD", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=232)
    Button(menu_frame, height=80, width=80, image=AUTOCLICK_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=draw_autoclick).place(x=5, y=309)
    Label(menu_frame, text="AUTOCLICK", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=10).place(x = 130, y=332)
    Button(menu_frame, height=80, width=80, image=EXIT_BUTTON, bg="#27738e", activebackground="#27739f", relief=FLAT, command=ROOT.destroy).place(x=5, y=499)
    Label(menu_frame, text="EXIT", anchor="w", font=("GillSans", 20), fg="white", bg="#27738e", height=1, width=5).place(x = 130, y=522)

    return menu_frame



#START OF SCRIPT

#loads all saves to global variable
SAVE_LIST = load_save_list()

#sets window icon
ROOT.iconphoto(True, LOGO_IMAGE)

#sets background color
ROOT.configure(bg=BACKGROUND_CLR)

#sets window size
ROOT.geometry(DEFAULT_SCREEN_SIZE)
ROOT.minsize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
ROOT.maxsize(DEFAULT_WIDTH, DEFAULT_HEIGHT)

#Draws Header, Menu, Body and Footer frames
HEADER_FRAME = draw_header_frame()
HEADER_FRAME.place(x=0, y=0, anchor='nw')

MENU_FRAME = draw_menu_frame()
MENU_FRAME.place(x=0, y=101, anchor='nw')

MINI_BODY_FRAME = draw_home_page_menu()
MINI_BODY_FRAME.place(x=405, y=110, anchor='nw')

BODY_FRAME = draw_home_page()
BODY_FRAME.place(x=0, y=101, anchor='nw')

FOOTER_FRAME = draw_footer_frame()
FOOTER_FRAME.place(x=0, y=DEFAULT_HEIGHT-31, anchor='nw')


#sets the home as the current frame
CURRENT_FRAME = BODY_FRAME
CURRENT_FRAME_NAME = "home"
CURRENT_LOADED_NAME.trace("w", update_current_loaded_save)

ROOT.mainloop()
