import mouse
import time
import keyboard

import tkinter as tk


actions = 0


def clickEvent():
    global actions
    actions += 1


def keyEvent(e):
    global actions

    global startTime
    global runTime

    if e.event_type == 'down':
        actions += 1

        if e.name == 'end':
            actions = 0
            startTime = time.time()
            currentTime = time.time()
            runTime = currentTime - startTime

mouse.on_click(clickEvent)
mouse.on_right_click(clickEvent)
keyboard.hook(keyEvent, suppress=False, on_remove=print(''))



startTime = time.time()
runTime = 0




root = tk.Tk()
screenHeight = root.winfo_screenheight()
screenWidth = root.winfo_screenwidth()


width = int(screenWidth / 10)
height = int(screenHeight / 20)
startX = int(screenWidth - width)
startY = 0



root.overrideredirect(True)
root.attributes('-alpha',1)
root.geometry("{}x{}+{}+{}".format(width, height, startX, startY))

root.lift()
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "black")

label = tk.Label(
    text="0",
    foreground="red",
    background="black",
    font=("Arial", 20)
)



label.pack(ipadx=width, ipady=height)

def changeAPM():
    currentTime = time.time()
    runTime = currentTime - startTime
    mins = runTime / 60
    if mins > 0:
        apm = int(actions / mins)
        label.config(text=str(apm))

    root.after(1, changeAPM)


root.after(1, changeAPM)

def stay_on_top():
   root.lift()
   root.after(2000, stay_on_top)

stay_on_top()
root.mainloop()
