import time
import pyautogui
from tkinter import *

window = Tk()

window.title("SHVR Auto Split")
window.geometry('500x500')

debugText = StringVar()
debugText.set("Point your mouse at\nthe top left portion\nof your desired area,\n and then press Enter.")

debugLabel = Label(window, textvariable=debugText)
debugLabel.config(font=("Courier", 24))
debugLabel.pack()

# https://stackoverflow.com/a/47476389
def enter(event=None):
    print("ENTER :)")
    global window
    window.quit()
window.bind('<Return>', enter)

window.mainloop()

posTL = pyautogui.position()

print("Got position", posTL)

debugText.set("Point your mouse at\nthe bottom right portion\nof your desired area,\n and then press Enter.")
window.mainloop()

debugText.set("White Pixels: ?%\nDark Frames: ?")
window.update()

posBR = pyautogui.position()

print("Got position", posBR)

sx, sy = posTL[0], posTL[1]
ex, ey = posBR[0], posBR[1]
w, h = ex-sx, ey-sy
dx, dy = int(round(w * 0.1)), int(round(h * 0.1))

numPixels = len(range(sx, ex, dx)) * len(range(sy, ey, dy))

pixelThreshold = 12
stateThreshold = 3

stateFrames = 0

running = True
while running:
    pixelCount = 0
    for x in range(sx, ex, dx):
        for y in range(sy, ey, dy):
            if (pyautogui.pixelMatchesColor(x, y, (255,255,255), tolerance=40)):
                pixelCount += 1

    prevStateFrames = stateFrames

    pixelPercent = int(round((100 * (pixelCount / numPixels))))
    if pixelPercent < pixelThreshold:
        stateFrames += 1
    else:
        stateFrames = 0

    if prevStateFrames >= stateThreshold and stateFrames == 0:
        print("-----------------\nNEW LEVEL SEGMENT\n-----------------")

    debugText.set("White Pixels: " + str(pixelPercent) + "%\n" + "Dark Frames: " + str(stateFrames))

    window.update()
    
    print("White Pixels:", str(pixelPercent) + "%",
          " | Dark Frames:", stateFrames)
