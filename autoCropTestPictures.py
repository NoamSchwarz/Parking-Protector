import cv2
import matplotlib.pyplot as plt
import os

firstImagePath = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\notebook_sequential_images\image_2.jpg"
secondImagePath = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\notebook_sequential_images\image_3.jpg"

img1 = cv2.imread(firstImagePath, 1)
firstImage = cv2.resize(img1, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_LINEAR)

img2 = cv2.imread(secondImagePath, 1)
secondImage= cv2.resize(img2, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_LINEAR)
secondImage = secondImage[..., ::-1]

def parkingMVP():

    thresh = 65
    maxVal = 255

    cv2.namedWindow("Window")
    # highgui function called when mouse events occur
    cv2.setMouseCallback("Window", cropRectangle)
    k = 0
    # loop until escape character is pressed
    while k != 27:
        cv2.putText(firstImage, 'Choose top left corner and drag to crop',
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2);
        cv2.putText(firstImage, 'press ESC to exit',
                    (10, 55), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2);
        cv2.imshow("Window", firstImage)
        k = cv2.waitKey(20) & 0xFF

    # crop base image mark it firstImageCrop

    firstImageCrop = firstImage[cropTopRow:cropBottomRow, cropLeftColomn:cropRightColomn]
    firstImageCrop = firstImageCrop[..., ::-1]
    plt.imshow(firstImageCrop)
    plt.show()
    
    secondImageCrop = secondImage[cropTopRow:cropBottomRow, cropLeftColomn:cropRightColomn]
    plt.imshow(secondImageCrop)
    plt.show()

    # compare first_image to second_image , find contours
    difference = cv2.subtract(firstImageCrop, secondImageCrop)
    differencGreyscale = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    retreval, differenceThreshold = cv2.threshold(differencGreyscale, thresh, maxVal, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(differenceThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    differenceThresholdCopy = differenceThreshold.copy()
    differenceThresholdBGR = cv2.cvtColor(differenceThresholdCopy, cv2.COLOR_GRAY2BGR)
    differenceWithContours = cv2.drawContours(differenceThresholdBGR, contours, -1, (0, 255, 0), 1);

    # find biggest contour and boundBox it
    try:
        biggestContour = max(contours, key=cv2.contourArea)
    # incase compared photos are exactly/mostly the same and no contours are found
    except ValueError:
        print("no contours detected in image_2")
    else:
        biggestContourArea = cv2.contourArea(biggestContour)
        image_h, image_w = secondImageCrop.shape[:2]
        if biggestContourArea > (image_h * image_w) * 0.3:
            print("parking taken in image_2" )
        else:
            print("small thing in image_2" )

        x, y, w, h = cv2.boundingRect(biggestContour)
        cv2.rectangle(differenceWithContours, (x, y), (x + w, y + h), (0, 0, 255), 2)

        plt.imshow(differenceWithContours)
        plt.show()


topLeft = None
bottomRight = None
cropTopRow = None
cropBottomRow = None
cropLeftColomn = None
cropRightColomn = None
cropedImage = None


def cropRectangle(action, x, y, flags, userdata):
    global topLeft, bottomRight, cropTopRow, cropBottomRow, cropLeftColomn, cropRightColomn

    if action == cv2.EVENT_LBUTTONDOWN:
        topLeft = (x, y)
        cropTopRow, cropLeftColomn = y, x

        cv2.rectangle(firstImage, topLeft, topLeft, (100, 0, 0), thickness=5, lineType=cv2.LINE_8)
    elif action == cv2.EVENT_LBUTTONUP:
        bottomRight = (x, y)
        cropBottomRow, cropRightColomn = y, x
        cv2.rectangle(firstImage, topLeft, bottomRight, (100, 0, 0), thickness=5, lineType=cv2.LINE_8)
        #cv2.imshow("window", firstImage)

        # cropedImage = dummy[cropTopRow:cropBottomRow, cropLeftColomn:cropRightColomn]
        # cv2.imshow("croped", cropedImage)
        # cv2.waitKey(1000)

    # cv2.imwrite("croped.png", cropedImage)


parkingMVP()