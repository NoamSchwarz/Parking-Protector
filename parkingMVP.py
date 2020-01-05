import cv2
import matplotlib.pyplot as plt
import os

baseImagePath  = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\10.12 view above notebook\view_above_notebbok_in_order\image_1.jpeg"
img= cv2.imread(baseImagePath, 1)
baseImage = cv2.resize(img,None,fx=0.5,fy=0.5,interpolation= cv2.INTER_LINEAR)
# Make a dummy image, will be useful to clear the drawing
dummy = baseImage.copy()

def parkingMVP():
    thresh = 100
    maxVal = 255

    cv2.namedWindow("Window")
    # highgui function called when mouse events occur
    cv2.setMouseCallback("Window", cropRectangle)
    k = 0
    # loop until escape character is pressed
    while k != 27:
        cv2.putText(baseImage, 'Choose top left corner and drag to crop',
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2);
        cv2.putText(baseImage, 'press ESC to exit',
                    (10, 55), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2);
        cv2.imshow("Window", baseImage)
        k = cv2.waitKey(20) & 0xFF


    # crop base image mark it firstImageCrop
    firstImageCrop = baseImage[cropTopRow:cropBottomRow, cropLeftColomn:cropRightColomn]
    firstImageCrop = firstImageCrop[...,::-1]
    imageCounter = 2

    while imageCounter < 5:
        # crop image_2 - mark it secondImageCrop
        secondImagePath = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\10.12 view above notebook\view_above_notebbok_in_order\image_%d.jpeg" %imageCounter
        secondImage = cv2.imread(secondImagePath)
        secondImageResized = cv2.resize(secondImage,None,fx=0.5,fy=0.5,interpolation= cv2.INTER_LINEAR)
        secondImageResized = secondImageResized[...,::-1]
        secondImageCrop = secondImageResized[cropTopRow:cropBottomRow, cropLeftColomn:cropRightColomn]

        # compare first_image to second_image , find if there is conotour
        difference = cv2.subtract(firstImageCrop, secondImageCrop)
        differencGreyscale = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        # threshold image. for notebook images
        retreval, differenceThreshold = cv2.threshold(differencGreyscale, thresh, maxVal, cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(differenceThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        differenceThresholdCopy = differenceThreshold.copy()
        differenceThresholdBGR = cv2.cvtColor(differenceThresholdCopy, cv2.COLOR_GRAY2BGR)
        differenceWithContours = cv2.drawContours(differenceThresholdBGR, contours, -1, (0, 255, 0), 1);

        # find biggest contour and boundBox it
        biggestContour = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(biggestContour)
        # draw the book contour (in green)
        cv2.rectangle(differenceWithContours, (x, y), (x + w, y + h), (0, 0, 255), 2)

        plt.imshow(differenceWithContours)
        plt.show()

        imageCounter += 1
        # if yes, print something , stop procces?
        # if no, image_2 becomes first_image, load, crop and mark image_3 to second_image and repeat

    

topLeft = None
bottomRight = None
cropTopRow = None
cropBottomRow = None
cropLeftColomn = None
cropRightColomn = None
cropedImage = None

def cropRectangle(action, x,y,flags, userdata):
    global topLeft,bottomRight,cropTopRow,cropBottomRow,cropLeftColomn,cropRightColomn

    if action==cv2.EVENT_LBUTTONDOWN:
        topLeft = (x,y)
        cropTopRow,cropLeftColomn = y,x

        cv2.rectangle(baseImage,topLeft,topLeft,(100,0,0),thickness=5, lineType=cv2.LINE_8)
    elif action==cv2.EVENT_LBUTTONUP:
        bottomRight = (x,y)
        cropBottomRow,cropRightColomn = y,x
        cv2.rectangle(baseImage, topLeft, bottomRight, (100, 0, 0), thickness=5, lineType=cv2.LINE_8)
        #cv2.imshow("window", baseImage)

        #cropedImage = dummy[cropTopRow:cropBottomRow, cropLeftColomn:cropRightColomn]
        # cv2.imshow("croped", cropedImage)
        # cv2.waitKey(1000)


       # cv2.imwrite("croped.png", cropedImage)

parkingMVP()