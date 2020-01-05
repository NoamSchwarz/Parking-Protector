import cv2
import matplotlib.pyplot as plt

def test1():
    path1 = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\10.12 view above notebook\space #1 ocupied.jpeg"
    path2 = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\10.12 view above notebook\no cars.jpeg"

    thresh = 100
    maxVal = 255

    #load, resize and crop image of ocupied parking spot #1
    spot1 = cv2.imread(path1)
    spot1Copy = spot1 .copy()
    spot1ScaleDown = cv2.resize(spot1Copy, None, fx=0.5, fy=0.5, interpolation= cv2.INTER_LINEAR)
    spot1Crop = spot1ScaleDown[120:260,390:650]
    # swich BGE to RGB in image
    spot1Crop = spot1Crop[...,::-1]

    #load, resize and crop image of UNocupied parking spot
    allUnocupied = cv2.imread(path2)
    allUnocupiedCopy = allUnocupied.copy()
    allUnocupiedScaleDown = cv2.resize(allUnocupiedCopy, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    allUnocupiedCrop = allUnocupiedScaleDown[120:260, 390:650]
    # swich BGE to RGB in image
    allUnocupiedCrop = allUnocupiedCrop[...,::-1]

    #get differenct betweeb ocupied and unocupied spot #1
    difference = cv2.subtract(allUnocupiedCrop,spot1Crop)

    #DONT FORGET - CHANLES IS WRITTEN IMAGE WIL BR REVERSED BECAUSE OPENCV WORKS IN BGR
    cv2.imwrite("difference_ocuSpot1_and_unocuSpot1.jpeg", difference)

    #make difference image greyscale for threshold
    differencGreyscale = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    #threshold image. doesn't use retreval
    retreval, differenceThreshold =  cv2.threshold(differencGreyscale, thresh,maxVal, cv2.THRESH_BINARY)

    #find and draw contours
    contours, hierarchy = cv2.findContours(differenceThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    differenceThresholdCopy = differenceThreshold.copy()
    differenceThresholdBGR = cv2.cvtColor(differenceThresholdCopy, cv2.COLOR_GRAY2BGR)
    differenceWithContours = cv2.drawContours(differenceThresholdBGR, contours, -1, (0, 255, 0), 1);

    #find biggest contour and boundBox it
    biggestContour = max(contours,key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(biggestContour)
    # draw the book contour (in green)
    cv2.rectangle(differenceWithContours, (x, y), (x + w, y + h), (0, 0, 255), 2)

    #compute % of boundBox area in parking area
    boundBoxArea = (x + w) * (y + h)
    parkingAreaX,parkingAreaY = spot1Crop.shape[:2]
    parkingArea = parkingAreaX * parkingAreaY
    percentage = 100 * (float(boundBoxArea)/float(parkingArea))

    if percentage > 10:
        print("PARKING TAKEN")


    print(differencGreyscale[120:125,170:175 ])
    plt.figure(figsize=[15, 15]);
    plt.subplot(221); plt.imshow(allUnocupiedCrop); plt.title("unocupied");
    plt.subplot(222); plt.imshow(spot1Crop); plt.title("spot 1");
    plt.subplot(223); plt.imshow(differenceThreshold,'gray'); plt.title("difference threshold");
    plt.subplot(224); plt.imshow(difference); plt.title("difference");

    plt.show()
    #plt.savefig("difference_with_threshold")

    print(boundBoxArea, parkingArea, percentage)
    plt.imshow(differenceWithContours)
    plt.show()


test1()
