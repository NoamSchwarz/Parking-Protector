import cv2
import matplotlib.pyplot as plt


def test2():
    # upload paths for test images
    noCarsPath = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\10.12 view above notebook\no cars.jpeg"
    spotOneOccupiedPath =  r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\10.12 view above notebook\space #1 ocupied.jpeg"
    spotTwoOccupiedPath =  r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\10.12 view above notebook\space #2 ocupied.jpeg"
    spotThreeOccupiedPath =  r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\10.12 view above notebook\space #3 ocupied.jpeg"

    webcam_1 = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\29.12 homeParkingTest\homeparking1.jpg"
    webcam_2 = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\29.12 homeParkingTest\homeparking2.jpg"

    thresh = 100
    maxVal = 255

    # cropping coodinates for spot #2: x = 390:650 , y = 240:390

    #crop spot#2 out of no cars image
    noCars = cv2.imread(noCarsPath)
    noCarsCopy = noCars.copy()
    noCarsSpot2 = noCarsCopy[475:775,790:1300]
    noCarsSpot2 = noCarsSpot2[...,::-1]

    #crop xpot #2 out of space #2 occupied
    spotTwoOccupied = cv2.imread(spotTwoOccupiedPath)
    spotTwoCopy = spotTwoOccupied.copy()
    spotTwoOccupiedSpot2 = spotTwoCopy[475:775,790:1300]
    spotTwoOccupiedSpot2 = spotTwoOccupiedSpot2[...,::-1]

    #crop space #2 out of space 1 occupied
    spotOneOccupied = cv2.imread(spotOneOccupiedPath)
    spotOneCopy = spotOneOccupied.copy()
    spotOneOccupiedSpot2 = spotOneCopy[475:775,790:1300]
    spotOneOccupiedSpot2 = spotOneOccupiedSpot2 [...,::-1]

    #cropping coordinated for spot #3 y = 725:1000 , x = 800:1315

    #crop spot #3 out of no cars
    noCars = cv2.imread(noCarsPath)
    noCarsCopy = noCars.copy()
    noCarsSpot3 = noCarsCopy[725:1000, 800:1315]
    noCarsSpot3 = noCarsSpot3[..., ::-1]

    # crop spot #3 out of space #3 occupied
    spotThreeOccupied = cv2.imread(spotThreeOccupiedPath)
    spotThreeCopy = spotThreeOccupied.copy()
    spotThreeOccupiedSpot3 = spotThreeCopy[725:1000, 800:1315]
    spotThreeOccupiedSpot3 = spotThreeOccupiedSpot3[...,::-1]

    #crop spot #3 out of space #2 occupied
    spotTwoOccupied = cv2.imread(spotTwoOccupiedPath)
    spotTwoCopy = spotTwoOccupied.copy()
    spotTwoOccupiedSpot3 = spotTwoCopy[725:1000, 800:1315]
    spotTwoOccupiedSpot3 = spotTwoOccupiedSpot3[..., ::-1]

    #PICTURES FROM HOME PARKING
    emptySpotPath = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\real_cars_test\no_cars.jpg"
    spotTakenPath = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\real_cars_test\yes_car.jpg"

    #croping coordinates: y = 200:300 , x = 540:

    #threshold levels for real-life + dark image
    darkThreshold = 30

    #crop empty spot
    emptySpot = cv2.imread(emptySpotPath)
    emptySpotCopy = emptySpot.copy()
    emptySpotCrop = emptySpotCopy[200:300, 540:]
    emptySpotFinal = emptySpotCrop[..., ::-1]

    #crop taken spot
    spotTaken = cv2.imread(spotTakenPath)
    spotTakenCopy = spotTaken.copy()
    spotTakenCrop = spotTakenCopy[200:300, 540:]
    spotTakenFinal = spotTakenCrop[..., ::-1]


    difference = cv2.subtract(emptySpotFinal,spotTakenFinal)

    plt.imshow(difference)
    plt.show()

    differencGreyscale = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    # threshold image. for notebook images
    #retreval, differenceThreshold = cv2.threshold(differencGreyscale, thresh, maxVal, cv2.THRESH_BINARY)
    #threshold image for real-life + dark image
    retreval, differenceThreshold = cv2.threshold(differencGreyscale, darkThreshold, maxVal, cv2.THRESH_BINARY)

    plt.imshow(differenceThreshold,'gray')
    plt.show()

    # find and draw contours
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

test2()