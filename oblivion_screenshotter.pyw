# Made by Biksel

import keyboard
import threading
import configparser
import sys
from pyautogui import screenshot
from tkinter import *
from PIL import ImageTk, Image  
from os.path import isfile
from os import system
from time import sleep

running = True

left = 135
top = 100
shot_width = 775
shot_height = 825

screen_width = 1000
screen_height = 800

img = screenshot(region = (left, top, shot_width, shot_height))

is_frame_hidden = False

hotkey = "print scrn"

def read_config():
    global left, top, shot_width, shot_height, hotkey
    if not isfile("config.txt"):
        write_config()
    parser = configparser.RawConfigParser()
    config_path = "config.txt"
    parser.read(config_path)
    left = parser.getint("user", "topleft_x")
    top = parser.getint("user", "topleft_y")
    shot_width = parser.getint("user", "botright_x") - left
    shot_height = parser.getint("user", "botright_y") - top
    hotkey = parser.get("user", "hotkey")
    return

def write_config():
    global left, top, shot_width, shot_height, hotkey
    parser = configparser.RawConfigParser()
    config_path = "config.txt"
    parser.read(config_path)
    parser.set("user", "topleft_x", left)
    parser.set("user", "topleft_y", top)
    parser.set("user", "botright_x", left + shot_width)
    parser.set("user", "botright_y", top + shot_height)
    parser.set("user", "hotkey", hotkey)
    with open(config_path, 'w') as configfile:
        parser.write(configfile)
    return

def takeScreenshot():
    global img, resized_image, new_image, running
    while running:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == hotkey:
            img = screenshot(region = (left, top, shot_width, shot_height))
            resized_image = img.resize((canvas.winfo_width(), canvas.winfo_height()), Image.LANCZOS)
            new_image = ImageTk.PhotoImage(resized_image)
            canvas.itemconfigure(img_id, image=new_image)
    return
            

def setKey():
    global hotkey
    btnSetKey.configure(text="<Press a key>")
    hotkey = keyboard.read_event().name
    lblKey.configure(text="Current hotkey: {}".format(hotkey))
    btnSetKey.configure(text="Set new hotkey")
    write_config()
    return

def switchFrame():
    global is_frame_hidden
    if is_frame_hidden:
        btnHideFrame.configure(text="Show Frame")
        is_frame_hidden = False
        root.geometry("+{}+{}".format(root.winfo_x() - 5, root.winfo_y())) 
    elif not is_frame_hidden:
        btnHideFrame.configure(text="Hide Frame")
        is_frame_hidden = True
        root.geometry("+{}+{}".format(root.winfo_x() + 5, root.winfo_y())) 
    root.overrideredirect(is_frame_hidden)
    return

def saveCorners():
    global left, top, shot_width, shot_height
    coordsTop = entryTopCorner.get().split(",")
    coordsBot = entryBotCorner.get().split(",")
    try:
        left = int(coordsTop[0])
        top = int(coordsTop[1])
        shot_width = int(coordsBot[0]) - int(coordsTop[0])
        shot_height = int(coordsBot[1]) - int(coordsTop[1])
    except:
        return
    write_config()
    return

def resizer(e):
    global img, resized_image, new_image
    resized_image = img.resize((e.width, e.height), Image.LANCZOS)
    new_image = ImageTk.PhotoImage(resized_image)
    canvas.itemconfigure(img_id, image=new_image)
    return

def handleClosing():
    global running
    running = False
    system('taskkill /f /im oblivion_screenshotter.exe') # Probably not the best solution but works for now
    root.destroy()
    sys.exit(0)

read_config()
threading.Thread(target=takeScreenshot).start()

# Tkinter initialization
root = Tk()
root.configure(bg="#10141a")
root.title("Oblivion Override Screenshot Tool")
root.overrideredirect(is_frame_hidden)

topFrame = Frame(root, pady=10, bg="#10141a")
topFrame.pack(side=TOP)
btnHideFrame = Button(topFrame, text="Hide Frame", command=lambda: threading.Thread(target=switchFrame).start())
btnHideFrame.pack(side=LEFT)
lblInstructions = Label(topFrame, text="Format: x,y", padx=20, pady=2, bg="#10141a", fg="white", font='Arial 10 bold')
lblInstructions.pack(side=LEFT)

# Corners
lblTopCorner = Label(topFrame, text="Top-left corner: ", bg="#10141a", fg="white",font='Arial 10 bold')
entryTopCorner = Entry(topFrame)
lblTopCorner.pack(side=LEFT)
entryTopCorner.pack(side=LEFT)
entryTopCorner.insert(0, "{},{}".format(left, top))

lblBotCorner = Label(topFrame, text="Bottom-right corner: ", padx=2, pady=2, bg="#10141a", fg="white", font='Arial 10 bold')
entryBotCorner = Entry(topFrame)
lblBotCorner.pack(side=LEFT)
entryBotCorner.pack(side=LEFT)
entryBotCorner.insert(0, "{},{}".format(left + shot_width, top + shot_height))

btnSaveCorners = Button(topFrame, text = "Save positions", command=lambda: threading.Thread(target=saveCorners).start(), padx=2, pady=2)
btnSaveCorners.pack(side=LEFT)

# Hotkey
lblKey = Label(topFrame, text="Current hotkey: {}".format(hotkey), padx=2, pady=2, bg="#10141a", fg="white", font='Arial 10 bold')
btnSetKey = Button(topFrame, text = "Set new hotkey", command=lambda: threading.Thread(target=setKey).start(), padx=20, pady=2)
lblKey.pack(side=LEFT)
btnSetKey.pack(side=LEFT)

# Image Frame
botFrame = Frame(root)
botFrame.pack()

canvas = Canvas(root, width=shot_width, height=shot_height)
canvas.pack(fill=BOTH, expand=True, side=RIGHT)
img_id = canvas.create_image(0, 0, image=ImageTk.PhotoImage(img), anchor='nw')
canvas.bind('<Configure>', resizer)

root.protocol("WM_DELETE_WINDOW", handleClosing)
root.mainloop()