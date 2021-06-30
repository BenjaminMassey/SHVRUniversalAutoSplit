import time
import threading
import pyautogui
from tkinter import *
import win32api, win32con
from keylist import *

window = Tk()

window.title("SHVR Auto Split")
window.geometry('500x250')

key = None

try:
	file = open("key.txt", "r")
	content = file.readline()
	if len(content) > 0 and content in VK_CODE:
		key = VK_CODE[content]
	else:
		key = VK_CODE['end']
	file.close()
except:
	key = VK_CODE['end']

def setkey(self, *args):
	global key, keyselect, VK_CODE
	key = VK_CODE[keyselect.get()]
	file = open("key.txt", 'w')
	file.write(keyselect.get())
	file.close()

keyselect = StringVar()
keys = list(VK_CODE.keys())

file = open("key.txt")
keyselect.set(file.readline())
file.close()

splitKeyLabel = Label(window, text="Split Key:").pack()

selector = OptionMenu(window, keyselect, *keys).pack()
keyselect.trace('w', setkey)

try:
	setkey()
except:
	pass

def split():
	global key
	win32api.keybd_event(key,0,0,0)
	time.sleep(.05)
	win32api.keybd_event(key,0,win32con.KEYEVENTF_KEYUP,0)

#testButton = Button(window, text="Split", command=split).pack()

debugText = StringVar()
debugText.set("\nPoint your mouse at\nthe top left portion\nof your desired area,\n and then press Enter.")

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

debugText.set("\nPoint your mouse at\nthe bottom right portion\nof your desired area,\n and then press Enter.")
window.mainloop()

debugText.set("\nSetting up...")
#debugText.set("\nWhite Pixels: ?%\nDark Frames: ?")
window.update()

posBR = pyautogui.position()

print("Got position", posBR)

section = 0

def splitLoop():
	global section, posTL, posBR
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
		
		transition = False;
		
		if section == 4:
			if stateFrames > 2:
				transition = True
		elif section > 0 and section < 4:
			if prevStateFrames >= stateThreshold and stateFrames == 0:
				transition = True
		elif section == 0:
			# NEED LOGIC HERE
			transition = True
		else:
			print("Should not be here >:(")
		
		if transition:
			print("-----------------\nSPLIT\n-----------------")
			debugText.set("\n-----------------\nSPLIT\n-----------------")
			split()
			section += 1
		else:
			debugText.set("\nIn Section " + str(section) + "\n\nRunning...")
		
		print("White Pixels:", str(pixelPercent) + "%",
			  " | Dark Frames:", stateFrames)

splitter = threading.Thread(target=splitLoop)
splitter.start()

window.mainloop()

