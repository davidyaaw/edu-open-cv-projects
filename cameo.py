import cv2.cv2 as cv2
import time
from managers import WindowManager, CaptureManager


class Cameo(object):
    def __init__(self):
        self._windowManager = WindowManager('Cameo', self.onKeypress)
        self._captureManager = CaptureManager(cv2.VideoCapture(1), self._windowManager, True)

    def run(self):
        """Run main loop"""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            if frame is not None:
                # TO DO: Filter the frame
                pass
            self._captureManager.exitFrame()
            self._windowManager.processEvents()

    def onKeypress(self, keycode):
        """
        space -> take screenshot
        tab -> start/stop rec a screencast
        esc -> quit
        """
        if keycode == 32:  # space
            self._captureManager.writeImage('screen_shot.png')
        elif keycode == 9:  # tab
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo('screen_movie.avi')
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27:  # esc
            self._windowManager.destroyWindow()


if __name__ == '__main__':
    Cameo().run()
