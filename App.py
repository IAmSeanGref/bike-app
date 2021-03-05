from RearviewCamera import RearviewCamera
import tkinter as tki
import threading
import time

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        print("[INFO] Received close signal.")
        self.rearviewCamera.onClose()
        print("[INFO] Quitting...")
        self.root.quit()
        print("[INFO] Quit.")

    def run(self):
        self.root = tki.Tk()
        self.root.wm_title("Rear View Camera")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        if self.root.winfo_screenwidth() < 800:
            self.root.attributes('-fullscreen', True)
        else:
            self.root.geometry('720x480+0+0')
        self.buildInterface(self.root)
        self.root.mainloop() # This is a blocking call.

    def buildInterface(self, window):
        canvas = tki.Canvas(self.root, bg='black', highlightthickness=0)
        canvas.pack(fill=tki.BOTH, expand=True)
        self.rearviewCamera = RearviewCamera(window, canvas)
