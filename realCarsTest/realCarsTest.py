import cv2
import matplotlib.pyplot as plt

emptySpotPath = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\real_cars_test\no_cars.jpg"
spotTakenPath = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\real_cars_test\yes_car.jpg"

darkThreshold = 30
maxVal = 255

# crop empty spot
emptySpot = cv2.imread(emptySpotPath)
emptySpotCopy = emptySpot.copy()
emptySpotCrop = emptySpotCopy[200:300, 540:]
emptySpotFinal = emptySpotCrop[..., ::-1]

# crop taken spot
spotTaken = cv2.imread(spotTakenPath)
spotTakenCopy = spotTaken.copy()
spotTakenCrop = spotTakenCopy[200:300, 540:]
spotTakenFinal = spotTakenCrop[..., ::-1]

difference = cv2.subtract(emptySpotFinal, spotTakenFinal)

plt.imshow(difference)
plt.show()

differencGreyscale = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

retreval, differenceThreshold = cv2.threshold(differencGreyscale, darkThreshold, maxVal, cv2.THRESH_BINARY)

plt.imshow(differenceThreshold, 'gray')
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
