import cv2
import matplotlib.pyplot as plt
import parking_proj_git.parking_class

def get_num_of_images():
    #TODO: Get the values automatically
    return 14


def parkingMVP():
    # test with multiple pictures and light change
    ESC_KEY = 27
    numOfImages = get_num_of_images()

    #for notebook_sequential_images, witch are darker then the norebook from above
    thresh = 65
    maxVal = 255


    markParking = parking_proj_git.parking_class.MarkParking()
    markParking.mark_parking()
    cropTopRow, cropBottomRow, cropLeftColomn, cropRightColomn = markParking.get_rectangle_coordinates()

    # crop base image mark it firstImageCrop
    baseImage = markParking.baseImage
    firstImageCrop = baseImage[cropTopRow:cropBottomRow, cropLeftColomn:cropRightColomn]
    firstImageCrop = firstImageCrop[...,::-1]
    imageCounter = 1

    #! Prefer for loops
    # TODO: change to for loop
    while imageCounter < numOfImages+1 :
        # test with multiple pictures and light change
        #! consts should be passed as parameters. Alternatively, you can use a class.
        # TODO: put in class?
        secondImagePath = (r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git" 
                          r"\test pictures\notebook_sequential_images\image_{}.jpg".format(imageCounter))

        # crop image_2
        imgScaleFactor = markParking.imgScaleFactor

        secondImage = cv2.imread(secondImagePath)
        secondImageResized = cv2.resize(secondImage,None,fx=imgScaleFactor,fy=imgScaleFactor,interpolation= cv2.INTER_LINEAR)
        secondImageResized = secondImageResized[...,::-1]
        secondImageCrop = secondImageResized[cropTopRow:cropBottomRow, cropLeftColomn:cropRightColomn]

        #! If you have a repeating line structure that makes sense to keep together - make it a function instead.
        plt.figure(figsize=[15, 15])
        plt.subplot(121); plt.imshow(firstImageCrop); plt.title("first image crop")
        plt.subplot(122); plt.imshow(secondImageCrop); plt.title("second image crop")
        plt.show()

        # compare first_image to second_image , find contours
        #TODO: put in sepeate function
        #! A lot of these comments look like the block below them can be extracted into a separate,
        #! named function. This would make the code easier to reason about and test.
        difference = cv2.subtract(firstImageCrop, secondImageCrop)
        differencGreyscale = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        retreval, differenceThreshold = cv2.threshold(differencGreyscale, thresh, maxVal, cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(differenceThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        differenceThresholdCopy = differenceThreshold.copy()
        differenceThresholdBGR = cv2.cvtColor(differenceThresholdCopy, cv2.COLOR_GRAY2BGR)
        differenceWithContours = cv2.drawContours(differenceThresholdBGR, contours, -1, (0, 255, 0), 1);

        #incase compared photos are exactly/mostly the same and no contours are found
        try:
            biggestContour = max(contours, key=cv2.contourArea)
        except ValueError:
            print("no contours detected in image {}".format(imageCounter))

            #! By using a for loop, you'd not have to manually increment all cases.
            #! Additionally, if you have something that must happen in both the `except`
            #! and the `else` blocks, you can put it in a `finally` block.
            imageCounter += 1
            continue

        biggestContourArea = cv2.contourArea(biggestContour)
        image_h, image_w = secondImageCrop.shape[:2]

        if biggestContourArea > (image_h*image_w)*0.3:
            print("parking taken in image {}".format(imageCounter))
        else:
            print("small thing in image {}".format(imageCounter))

        #draw boundindgBox abour biggest contour
        topLeftX, topLeftY, width, hight = cv2.boundingRect(biggestContour)
        topLeftCoror = (topLeftX,topLeftY)
        bottomRightCornor = (topLeftX + width, topLeftY + hight)
        cv2.rectangle(differenceWithContours, topLeftCoror , bottomRightCornor , color = (0, 0, 255), thickness=2)

        imageCounter += 1

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