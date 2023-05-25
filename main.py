import tkinter as tk
from tkinter.colorchooser import askcolor
import pickle
import mouse
import time
import keyboard





root = tk.Tk()
root.title('APM Overlay')

mainFont = 'Arial'

fontStyle = 'Arial'

screenHeight = root.winfo_screenheight()
screenWidth = root.winfo_screenwidth()









stdMargin = 10


def loadOptions():

    try:
        with open('options.pkl', 'rb') as file:

            optionsDict = pickle.load(file)

        file.close()

        return optionsDict
    except:
        return {

            'width' : int(screenWidth / 10),
            'height' : int(screenHeight / 15),
            'startX' : int(screenWidth - (screenWidth / 10)),
            'startY' : 0,
            'fontSize' : 20,
            'standardAPM' : 100,
            'targetAPM' : 150,
            'lowAPMColor' : '#D81212',
            'midAPMColor' : '#F56902',
            'highAPMColor' : '#24c324',
            'resetKey' : 'end',

        }







optionsDict = loadOptions()


widthVar = tk.IntVar(root, optionsDict['width'])
heightVar = tk.IntVar(root, optionsDict['height'])
startXVar = tk.IntVar(root, optionsDict['startX'])
startYVar = tk.IntVar(root, optionsDict['startY'])
fontSizeVar = tk.IntVar(root, optionsDict['fontSize'])

standardAPMVar = tk.IntVar(root, optionsDict['standardAPM'])
targetAPMVar = tk.IntVar(root, optionsDict['targetAPM'])

lowAPMColorVar = tk.StringVar(root, optionsDict['lowAPMColor'])
midAPMColorVar = tk.StringVar(root, optionsDict['midAPMColor'])
highAPMColorVar = tk.StringVar(root, optionsDict['highAPMColor'])

resetKeyVar = tk.StringVar(root, optionsDict['resetKey'])





locationLabel = tk.Label(root, text = 'Window Display', font=(mainFont,12, 'bold'))


widthLabel = tk.Label(root, text = 'Width', font=(mainFont,10))
heightLabel = tk.Label(root, text = 'Height', font=(mainFont,10))
startXLabel = tk.Label(root, text = 'Start X', font=(mainFont,10))
startYLabel = tk.Label(root, text = 'Start Y', font=(mainFont,10))
fontSizeLabel = tk.Label(root, text = 'Font Size', font=(mainFont,10))

widthInput = tk.Entry(root, textvariable = widthVar, font=(mainFont,10,'normal'))
heightInput = tk.Entry(root, textvariable = heightVar, font=(mainFont,10,'normal'))
startXInput = tk.Entry(root, textvariable = startXVar, font=(mainFont,10,'normal'))
startYInput = tk.Entry(root, textvariable = startYVar, font=(mainFont,10,'normal'))
fontSizeInput = tk.Entry(root, textvariable = fontSizeVar, font=(mainFont,10,'normal'))





###########################################################




apmDisplayLabel = tk.Label(root, text = 'APM Targets', font=(mainFont,12, 'bold'))



standardAPMLabel = tk.Label(root, text = 'Average APM', font=(mainFont,10))
targetAPMLabel = tk.Label(root, text = 'Target APM', font=(mainFont,10))

standardAPMInput = tk.Entry(root, textvariable = standardAPMVar, font=(mainFont,10,'normal'))
targetAPMInput = tk.Entry(root, textvariable = targetAPMVar, font=(mainFont,10,'normal'))



def changeLowColor():
    colors = askcolor()
    lowAPMColorVar.set(colors[1])
    lowColorBtn.configure(bg=colors[1])


def changeMidColor():
    colors = askcolor()
    midAPMColorVar.set(colors[1])
    midColorBtn.configure(bg=colors[1])


def changeHighColor():
    colors = askcolor()
    highAPMColorVar.set(colors[1])
    highColorBtn.configure(bg=colors[1])


APMTargetColorsLabel = tk.Label(root, text = 'APM Target Colors', font=(mainFont,12, 'bold'))

lowColorLabel = tk.Label(root, text = 'Low', font=(mainFont,10))
midColorLabel = tk.Label(root, text = 'Mid', font=(mainFont,10))
highColorLabel = tk.Label(root, text = 'High', font=(mainFont,10))


lowColorBtn = tk.Button(root, text='        ',bg=optionsDict['lowAPMColor'])
lowColorBtn.configure(command = changeLowColor)

midColorBtn = tk.Button(root, text='        ',bg=optionsDict['midAPMColor'])
midColorBtn.configure(command = changeMidColor)

highColorBtn = tk.Button(root, text='        ',bg=optionsDict['highAPMColor'])
highColorBtn.configure(command = changeHighColor)



resetKeyChange = False




resetKeyLabel = tk.Label(root, text = 'Reset Key', font=(mainFont,12, 'bold'))
resetKeyPromptLabel = tk.Label(root, text = 'Press Any Key', font=(mainFont,10, 'bold'))




def changeResetKey():

    global resetKeyChange
    global resetKeyPromptLabel

    resetKeyChange = True
    resetKeyPromptLabel.grid(row=11, column = 2, padx=stdMargin, pady=stdMargin)


resetKeyBtn = tk.Button(root, text=optionsDict['resetKey'], command=changeResetKey)





def makeOptionsDict():


    optionsDict = {
    'width' : widthVar.get(),
    'height' : heightVar.get(),
    'startX' : startXVar.get(),
    'startY' : startYVar.get(),
    'fontSize' : fontSizeVar.get(),
    'standardAPM' : standardAPMVar.get(),
    'targetAPM' : targetAPMVar.get(),
    'lowAPMColor' : lowAPMColorVar.get(),
    'midAPMColor' : midAPMColorVar.get(),
    'highAPMColor' : highAPMColorVar.get(),
    'resetKey' : resetKeyVar.get()
    }
    return optionsDict





###################################################






def createOverlay():

    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-alpha',1)
    overlay.geometry("{}x{}+{}+{}".format(optionsDict['width'], optionsDict['height'], optionsDict['startX'], optionsDict['startY']))

    overlay.lift()
    overlay.wm_attributes("-topmost", True)
    overlay.wm_attributes("-disabled", True)
    overlay.wm_attributes("-transparentcolor", "black")

    label = tk.Label(overlay,
        text="0",
        foreground='green',
        background="black",
        font=('Arial', optionsDict['fontSize'])
    )

    label.pack(ipadx=optionsDict['width'], ipady=optionsDict['height'])


    return overlay, label


actions = 0


def clickEvent():
    global actions
    actions += 1


def keyEvent(e):
    global actions

    global startTime
    global runTime
    global resetKeyChange

    global resetKeyPromptLabel

    if e.event_type == 'down':
        actions += 1
        if resetKeyChange:
            resetKeyVar.set(e.name)
            resetKeyBtn.configure(text = resetKeyVar.get())
            resetKeyPromptLabel.grid_forget()
            resetKeyChange = False

        if e.name == optionsDict['resetKey']:
            actions = 0
            startTime = time.time()
            currentTime = time.time()
            runTime = currentTime - startTime

mouse.on_click(clickEvent)
mouse.on_right_click(clickEvent)
keyboard.hook(keyEvent, suppress=False, on_remove=print(''))



startTime = time.time()
runTime = 0






overlay, label = createOverlay()


def applyChanges():
    global optionsDict
    optionsDict = makeOptionsDict()
    with open('options.pkl', 'wb') as file:
        pickle.dump(optionsDict, file)

    file.close()

    overlay.geometry("{}x{}+{}+{}".format(optionsDict['width'], optionsDict['height'], optionsDict['startX'], optionsDict['startY']))

    label.configure(font=('Arial', optionsDict['fontSize']))




saveBtn = tk.Button(root, text='Apply Changes', command=applyChanges)


def stay_on_top():
   overlay.lift()
   overlay.after(2000, stay_on_top)




def changeAPM():
    currentTime = time.time()
    runTime = currentTime - startTime
    mins = runTime / 60
    if mins > 0:
        apm = int(actions / mins)

        color = optionsDict['lowAPMColor']

        if apm >= optionsDict['standardAPM']:
            color = optionsDict['midAPMColor']


        if apm >= optionsDict['targetAPM']:
            color = optionsDict['highAPMColor']


        label.config(text=str(apm), fg=color)

    overlay.after(1, changeAPM)


overlay.after(1, changeAPM)





settingsLabel = tk.Label(root, text = 'Settings', font=(mainFont,20, 'bold'))


settingsLabel.grid(row=0,column=2,pady=40)

locationLabel.grid(row=1,column=2,padx=stdMargin, pady=stdMargin)

startXLabel.grid(row=2, column=0, padx=stdMargin, pady=stdMargin)
startYLabel.grid(row=2, column=1, padx=stdMargin, pady=stdMargin)
widthLabel.grid(row=2, column=2, padx=stdMargin, pady=stdMargin)
heightLabel.grid(row=2, column=3, padx=stdMargin, pady=stdMargin)
fontSizeLabel.grid(row=2, column=4, padx=stdMargin, pady=stdMargin)


startXInput.grid(row=3, column=0, padx=stdMargin, pady=stdMargin)
startYInput.grid(row=3, column=1, padx=stdMargin, pady=stdMargin)
widthInput.grid(row=3, column=2, padx=stdMargin, pady=stdMargin)
heightInput.grid(row=3, column=3, padx=stdMargin, pady=stdMargin)
fontSizeInput.grid(row=3, column=4, padx=stdMargin, pady=stdMargin)
apmDisplayLabel.grid(row=4, column=2, padx=stdMargin, pady=stdMargin)
standardAPMLabel.grid(row=5, column=1, padx=stdMargin, pady=stdMargin)
targetAPMLabel.grid(row=5, column=3, padx=stdMargin, pady=stdMargin)
standardAPMInput.grid(row=6, column=1, padx=stdMargin, pady=stdMargin)
targetAPMInput.grid(row=6, column=3, padx=stdMargin, pady=stdMargin)
APMTargetColorsLabel.grid(row=7, column = 2, padx=stdMargin, pady=stdMargin)

lowColorLabel.grid(row=8, column = 0, padx=stdMargin, pady=stdMargin)
midColorLabel.grid(row=8, column = 2, padx=stdMargin, pady=stdMargin)
highColorLabel.grid(row=8, column = 4, padx=stdMargin, pady=stdMargin)

lowColorBtn.grid(row=9, column = 0, padx=stdMargin, pady=stdMargin)
midColorBtn.grid(row=9, column = 2, padx=stdMargin, pady=stdMargin)
highColorBtn.grid(row=9, column = 4, padx=stdMargin, pady=stdMargin)

resetKeyLabel.grid(row=10, column = 2, padx=stdMargin, pady=stdMargin)
resetKeyBtn.grid(row=12, column = 2, padx=stdMargin, pady=stdMargin)



saveBtn.grid(row=13, column=2, padx=stdMargin, pady=30)



photo = tk.PhotoImage(file = "icon.png")
root.iconphoto(False, photo)


root.mainloop()
