import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def test1():
    path = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\10.12 view above notebook\space #1 ocupied.jpeg"

    im = cv2.imread(path)
    imCopy = im.copy()
    scaleDownIm = cv2.resize(imCopy,None,fx=0.5,fy=0.5,interpolation= cv2.INTER_LINEAR)
    cropROI = scaleDownIm[120:260,390:650]
    plt.imshow(im)
    plt.show()
    plt.imshow(cropROI)
    plt.show()

test1()
