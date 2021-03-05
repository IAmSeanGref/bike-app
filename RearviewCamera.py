from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import cv2
import datetime
import threading
import time
import tkinter as tki
import os

class RearviewCamera:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.stopEvent = threading.Event()
        self.oldFrameTime = time.time()
        self.thread = threading.Thread(target=self.videoLoop, args=[self.stopEvent], daemon=True)
        self.thread.start()
        
    def videoLoop(self, stopEvent):
        self.startCapture()
        self.setupCanvas()
        try:
            while not stopEvent.is_set():
                (ret, frame) = self.getFrame()
                if ret:
                    self.drawFrame(frame)
                    
                time.sleep(1.0/self.vid.get(cv2.CAP_PROP_FPS))
                self.oldFrameTime = self.newFrameTime

            print("[INFO] Releasing resources...")
            if self.vid.isOpened():
                self.vid.release()
            print("[INFO] Done.")

        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def startCapture(self):
        self.vid = cv2.VideoCapture(0)
        # Hack, setting to an absurd size gives maximum resolution!
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
        self.capWidth = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.capHeight = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.capAspectRatio = float(self.capWidth) / float(self.capHeight)

    def setupCanvas(self):
        self.imageWidget = self.canvas.create_image(0, 0, anchor = tki.NW)
        b = tki.Button(self.canvas, text='Implode!')
        self.canvas.create_window(10, 10, anchor=tki.NW, window=b)

    def getFrame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 1))
            else:
                return (ret, None)
        else:
            return (None, None)

    def drawFrame(self, frame):
        (imgX, imgY, targetWidth, targetHeight) = self.getTargetDimensions()
        resizedFrame = cv2.resize(frame, (targetWidth, targetHeight), interpolation = cv2.INTER_AREA)

        self.newFrameTime = time.time()
        fps = "FPS: " + str(int(1/(self.newFrameTime - self.oldFrameTime)))
        cv2.putText(resizedFrame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 3, cv2.LINE_AA)

        self.frame = ImageTk.PhotoImage(image = Image.fromarray(resizedFrame))
        self.canvas.coords(self.imageWidget, imgX, imgY)
        self.canvas.itemconfig(self.imageWidget, image = self.frame)
        self.canvas.gcSafeFrame = self.frame # Stupid tkinter needs to hold a reference or has flickering.

    def getTargetDimensions(self):
        # Update dimensions in case window changed.
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        self.aspectRatio = float(self.width) / float(self.height)
        targetWidth = self.width
        targetHeight = self.height
        if (self.capAspectRatio > self.aspectRatio):
            targetHeight = int(self.width / self.capAspectRatio)
        else:
            targetWidth = int(self.height * self.capAspectRatio)
        
        imgX = (self.width - targetWidth) / 2 
        imgY = (self.height - targetHeight) / 2
        return (imgX, imgY, targetWidth, targetHeight)

    def onClose(self):
        print("[INFO] Closing...")
        self.stopEvent.set()
        print("[INFO] Closed.")
