import time
import pyautogui

print("Point your mouse at the top left portion of your desired area, \
       and then press Enter.")

input()

posTL = pyautogui.position()

print("Got position", posTL)

print("Point your mouse at the bottom right portion of your desired area, \
       and then press Enter.")

input()

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

while True:
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
    
    print("White Pixels:", str(pixelPercent) + "%",
          " | Dark Frames:", stateFrames)
