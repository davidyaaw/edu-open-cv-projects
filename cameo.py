import cv2.cv2 as cv2
import filters
from managers import WindowManager, CaptureManager


class Cameo(object):
    def __init__(self):

        self._filter1_enabled = None
        self._filter2_enabled = None
        self._filter3_enabled = None
        self._filter4_enabled = None
        self._filter5_enabled = None
        self._filter6_enabled = None
        self._filter7_enabled = None

        self._blurFilter = filters.BlurFilter()
        self._sharpenFilter = filters.SharpenFilter()
        self._findedgesFilter = filters.FindEdgesFilter()
        self._embossFilter = filters.EmbossFilter()
        self._laplasianFilter = filters.Laplasian()
        self._laplasianFilterL = filters.LaplacianFilter()

        self._windowManager = WindowManager('Cameo', self.onKeypress)
        self._captureManager = CaptureManager(cv2.VideoCapture(0), self._windowManager, False)

    def run(self):
        """Run main loop"""
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            if frame is not None:
                # TO DO: Filter the frame
                if self._filter1_enabled:
                    filters.strokeEdges(frame, frame)
                if self._filter2_enabled:
                    self._sharpenFilter.apply(frame, frame)
                if self._filter3_enabled:
                    self._findedgesFilter.apply(frame,frame)
                if self._filter4_enabled:
                    self._blurFilter.apply(frame, frame)
                if self._filter5_enabled:
                    self._embossFilter.apply(frame, frame)
                if self._filter6_enabled:
                    self._laplasianFilter.apply(frame, frame)
                if self._filter7_enabled:
                    self._laplasianFilterL.apply(frame, frame)
                pass

            self._captureManager.exitFrame()
            self._windowManager.processEvents()

    def onKeypress(self, keycode):
        """
        space -> take screenshot
        tab -> start/stop rec a screencast
        esc -> quit
        1 -> stroke Edges filter
        2 -> sharpen filter
        3 -> find edges filter
        4 -> blur filter
        5 -> emboss filter
        6 - > laplasian 3x3
        7 - > laplasian 5x5
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
        elif keycode == ord('1'):
            self._filter1_enabled = not self._filter1_enabled
            print('strokeEdges: ', self._filter1_enabled)
        elif keycode == ord('2'):
            self._filter2_enabled = not self._filter2_enabled
            print('Sharpen Filter: ', self._filter2_enabled)
        elif keycode == ord('3'):
            self._filter3_enabled = not self._filter3_enabled
            print('FindEdge Filter: ', self._filter3_enabled)
        elif keycode == ord('4'):
            self._filter4_enabled = not self._filter4_enabled
            print('Blur Filter: ', self._filter4_enabled)
        elif keycode == ord('5'):
            self._filter5_enabled = not self._filter5_enabled
            print('Emboss Filter: ', self._filter5_enabled)
        elif keycode == ord('6'):
            self._filter6_enabled = not self._filter6_enabled
            print('Laplasian Filter 3x3: ', self._filter6_enabled)
        elif keycode == ord('7'):
            self._filter7_enabled = not self._filter7_enabled
            print('Laplasian Filter 5x5: ', self._filter7_enabled)


if __name__ == '__main__':
    Cameo().run()
