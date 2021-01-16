import time
import pyautogui

sx, sy = 2343, 126
w, h = 952, 714
ex, ey = sx+w, sy+h
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
