import cv2
import matplotlib.pyplot as plt
from parking_proj_git.parking_class import ParkingMark

FIRST_IMAGE_PATH = (r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git"
                      r"\test pictures\notebook_sequential_images\image_1.jpg")

SECOND_IMAGE_PATH_TEMPLATE = (r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git" 
                          r"\test pictures\notebook_sequential_images\image_{}.jpg")

#TODO change all camle case variables and functions name to underscore
#TODO: finish

#TODO: run autocrop test with images 12 and 13 to see if change of thresh is needed for correct output
#currently it gives small thing in parking instead of parking taken

#TODO: have in parking_class as well. make global?
imgScaleFactor = 0.7

def get_num_of_images():
    #TODO: Get the values automatically
    return 14

#TODO: consider makeing cropCoordinates a named tuple
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
    differenc_greyscale = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    retreval, difference_threshold = cv2.threshold(differenc_greyscale, thresh, maxVal, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(difference_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    difference_threshold_copy = difference_threshold.copy()
    difference_threshold_bgr = cv2.cvtColor(difference_threshold_copy, cv2.COLOR_GRAY2BGR)
    difference_with_contours = cv2.drawContours(difference_threshold_bgr, contours, -1, (0, 255, 0), 1);

    return difference_with_contours, contours


# mark parking spot in picture with a rectangle
# crop_coordinates is a tuple of the coordinates of the 4 corners of the rectangle
def find_parking_spot():
    mark_parking = ParkingMark()
    mark_parking.mark_parking()
    crop_coordinates = mark_parking.get_rectangle_coordinates()
    return crop_coordinates


def parking_MVP():

    num_of_images = get_num_of_images()
    crop_coordinates = find_parking_spot()

    #TODO: pass as parameter for parkingMVP function + as a constant

    first_image_crop = crop_image(FIRST_IMAGE_PATH, crop_coordinates)

    #TODO turn secondImage_path to constant and then use templat.format()
    for image_index in range(2, num_of_images+1):
        second_image_path = SECOND_IMAGE_PATH_TEMPLATE.format(image_index)
        second_image_crop = crop_image(second_image_path, crop_coordinates)

        # plt.figure(figsize=[15, 15])
        # plt.subplot(121); plt.imshow(first_image_crop); plt.title("image {} crop".format(image_index-1))
        # plt.subplot(122); plt.imshow(second_image_crop); plt.title("image {} crop".format(image_index))
        # plt.show()

        # compare firstImageCrop to secondImageCrop, find contours and mark them on image
        difference_with_contours, contours = compare_images(first_image_crop, second_image_crop)

        #incase compared photos are exactly/mostly the same and no contours are found
        #TODO: can this block be a seperate function?
        try:
            biggest_contour = max(contours, key=cv2.contourArea)
        except ValueError:
            print("no contours detected in image {}".format(image_index))
            continue

        biggest_contour_area = cv2.contourArea(biggest_contour)
        image_h, image_w = second_image_crop.shape[:2]

        if biggest_contour_area > (image_h*image_w)*0.3:
            print("parking taken in image {}".format(image_index))
        else:
            print("small thing in image {}".format(image_index))

        #TODO: can be seperate function? or part of try-except block? (this block needs biggestContour)
        #draw boundindgBox abour biggest contour
        top_left_x, top_left_y, width, height = cv2.boundingRect(biggest_contour)
        top_left_corner = (top_left_x,top_left_y)
        borrom_right_corner = (top_left_x + width, top_left_y + height)
        cv2.rectangle(difference_with_contours, top_left_corner , borrom_right_corner , color = (0, 0, 255), thickness=2)

        # cv2.imshow("{}".format(image_index), difference_with_contours)
        # cv2.waitKey(1500)
        # cv2.destroyWindow("{}".format(image_index))

        first_image_crop = second_image_crop
        #TODO: decide weather to procese after spot is taken or to stop the procces.
        #if the former, do I need to be able to idenify when the taken spot has become empty?


parking_MVP()

#! Other notes:
#! - Automatic formatting
#! - Linters and inspections
#! - __main__
#! - argparse
#! - Generators