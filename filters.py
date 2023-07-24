import cv2.cv2 as cv2
import numpy as np
import utils


def strokeEdges(src, dst, blurKsize=7, edgeKsize=5):
    # 7 and 5 produces more pleasant effect
    if blurKsize >= 3:
        blurredSrc = cv2.medianBlur(src, blurKsize)
        graySrc = cv2.cvtColor(blurredSrc, cv2.COLOR_BGR2GRAY)
    else:
        graySrc = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    cv2.Laplacian(graySrc, cv2.CV_8U, graySrc, ksize=edgeKsize)
    normalizedInverseAlpha = (1.0 / 255) * (255 - graySrc)
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = channel * normalizedInverseAlpha
    cv2.merge(channels, dst)


class VConvolutionalFilter(object):
    def __init__(self, kernel):
        self._kernel = kernel

    def apply(self, src, dst):
        cv2.filter2D(src, -1, self._kernel, dst)  # -1 means the same in/out depth


class SharpenFilter(VConvolutionalFilter):
    """Sharpen filter with 1 px radius"""

    def __init__(self):
        kernel = np.array([
            [-1, -1, -1],
            [-1, 9, -1],
            [-1, -1, -1]
        ])
        VConvolutionalFilter.__init__(self, kernel)


class FindEdgesFilter(VConvolutionalFilter):
    def __init__(self):
        kernel = np.array([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ])
        VConvolutionalFilter.__init__(self, kernel)


class BlurFilter(VConvolutionalFilter):
    """Sum to 1 . 2px radius"""

    def __init__(self):
        kernel = np.array([
            [0.04, 0.04, 0.04, 0.04, 0.04],
            [0.04, 0.04, 0.04, 0.04, 0.04],
            [0.04, 0.04, 0.04, 0.04, 0.04],
            [0.04, 0.04, 0.04, 0.04, 0.04],
            [0.04, 0.04, 0.04, 0.04, 0.04]
        ])
        VConvolutionalFilter.__init__(self, kernel)


class EmbossFilter(VConvolutionalFilter):
    def __init__(self):
        kernel = np.array([
            [-2, -1, 0],
            [-1, 1, 1],
            [0, 1, 2]
        ])
        VConvolutionalFilter.__init__(self, kernel)


class Laplasian(VConvolutionalFilter):
    def __init__(self):
        kernel = np.array([
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0]
        ])
        VConvolutionalFilter.__init__(self, kernel)


class LaplacianFilter(VConvolutionalFilter):
    """Laplacian filter 5 x 5 """

    def __init__(self):
        kernel = np.array([
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, 24, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1]
        ])
        VConvolutionalFilter.__init__(self, kernel)
