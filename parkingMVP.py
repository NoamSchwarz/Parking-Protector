import cv2
import matplotlib.pyplot as plt
import parking_proj_git.parking_class

#TODO: run autocrop test with images 12 and 13 to see if change of thresh is needed for correct output
#currently it gives small thing in parking instead of parking taken

#TODO: have in parking_class as well. make global?
imgScaleFactor = 0.7

def get_num_of_images():
    #TODO: Get the values automatically
    return 14

def crop_image(imagePath, cropCoordinates):
    cropTopRow, cropBottomRow, cropLeftColomn, cropRightColomn = cropCoordinates
    tempImage = cv2.imread(imagePath)
    tempImageResized = cv2.resize(tempImage, None, fx=imgScaleFactor, fy=imgScaleFactor, interpolation=cv2.INTER_LINEAR)
    tempImageResized = tempImageResized[..., ::-1]
    tempImageCrop = tempImageResized[cropTopRow:cropBottomRow, cropLeftColomn:cropRightColomn]
    return tempImageCrop

def compare_images(firstImage, secondImage):
    # for notebook_sequential_images, witch are darker then the norebook from above
    thresh = 65
    maxVal = 255

    difference = cv2.subtract(firstImage, secondImage)
    differencGreyscale = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    retreval, differenceThreshold = cv2.threshold(differencGreyscale, thresh, maxVal, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(differenceThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    differenceThresholdCopy = differenceThreshold.copy()
    differenceThresholdBGR = cv2.cvtColor(differenceThresholdCopy, cv2.COLOR_GRAY2BGR)
    differenceWithContours = cv2.drawContours(differenceThresholdBGR, contours, -1, (0, 255, 0), 1);

    return differenceWithContours, contours

def parkingMVP():
    # test with multiple pictures and light change
    ESC_KEY = 27
    numOfImages = get_num_of_images()

    # mark parking spot in picture with a rectangle
    # cropCoordinates is a tuple of the coordinates of the 4 corners of the rectangle
    markParking = parking_proj_git.parking_class.MarkParking()
    markParking.mark_parking()
    cropCoordinates = markParking.get_rectangle_coordinates()

    # test with multiple pictures and light change
    #TODO: pass as parameter for parkingMVP function?
    firstImagePath = (r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git"
                      r"\test pictures\notebook_sequential_images\image_1.jpg")
    firstImageCrop = crop_image(firstImagePath, cropCoordinates)

    for i in range(2, numOfImages+1):

        secondImagePath = (r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git" 
                          r"\test pictures\notebook_sequential_images\image_{}.jpg".format(i))
        # crop image_2
        secondImageCrop = crop_image(secondImagePath, cropCoordinates)

         # plt.figure(figsize=[15, 15])
        # plt.subplot(121); plt.imshow(firstImageCrop); plt.title("first image crop")
        # plt.subplot(122); plt.imshow(secondImageCrop); plt.title("second image crop")
        # plt.show()

        # compare firstImageCrop to secondImageCrop, find contours and mark them on image
        differenceWithContours, contours = compare_images(firstImageCrop, secondImageCrop)

        #incase compared photos are exactly/mostly the same and no contours are found
        #TODO: can this block be a seperate function?
        try:
            biggestContour = max(contours, key=cv2.contourArea)
        except ValueError:
            print("no contours detected in image {}".format(i))
            continue

        biggestContourArea = cv2.contourArea(biggestContour)
        image_h, image_w = secondImageCrop.shape[:2]

        if biggestContourArea > (image_h*image_w)*0.3:
            print("parking taken in image {}".format(i))
        else:
            print("small thing in image {}".format(i))

        #TODO: can be seperate function? or part of try-except block? (this block needs biggestContour)
        #draw boundindgBox abour biggest contour
        topLeftX, topLeftY, width, hight = cv2.boundingRect(biggestContour)
        topLeftCoror = (topLeftX,topLeftY)
        bottomRightCornor = (topLeftX + width, topLeftY + hight)
        cv2.rectangle(differenceWithContours, topLeftCoror , bottomRightCornor , color = (0, 0, 255), thickness=2)

        firstImageCrop = secondImageCrop
        #TODO: decide weather to procese after spot is taken or to stop the procces.
        #if the former, do I need to be able to idenify when the taken spot has become empty?


parkingMVP()

#! Other notes:
#! - Automatic formatting
#! - Linters and inspections
#! - __main__
#! - argparse
#! - Generators