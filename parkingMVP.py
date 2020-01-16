import cv2
import matplotlib.pyplot as plt
from parking_proj_git.parking_class import ParkingMark

#TODO change parking_prij_git ro just parking_proj (how to do this without messing everything up? )
#TODO change parking_class to ParkingMark
#TODO find a funner name for parkingMVP

IMAGE_PATH_TEMPLATE = (r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git" 
                          r"\test pictures\notebook_sequential_images\image_{}.jpg")
FIRST_IMAGE_PATH = IMAGE_PATH_TEMPLATE.format(1)

#TODO: run autocrop test with images 12 and 13 to see if change of thresh is needed for correct output
#it does. needs a thresh of ~35 for correct result.

#TODO: have in parking_class as well. make it a constant and a parameter of the read-resize function
IMG_RESIZE_FACTOR = 0.7

def get_num_of_images():
    #TODO: Get the values automatically
    return 14

#TODO make a crop-coordinated class, with the coordinates as atributes
#TODO use ParkingMark object for the coordinates instead if the tuple. add parking obkect as parameter for crop_image function

def crop_image(img, crop_coordinates):
    cropTopRow, cropBottomRow, cropLeftColomn, cropRightColomn = crop_coordinates
    tempImageCrop = img[cropTopRow:cropBottomRow, cropLeftColomn:cropRightColomn]
    return tempImageCrop

def read_resize_image(img_path, img_resize_factor):
    temp_image = cv2.imread(img_path)
    temp_image_resize = cv2.resize(temp_image, None, fx=img_resize_factor, fy=img_resize_factor, interpolation=cv2.INTER_LINEAR)
    temp_image_resize = temp_image_resize[..., ::-1]
    return temp_image_resize

def compare_images(firstImage, secondImage):
    # for notebook_sequential_images, witch are darker then the norebook from above
    thresh = 65
    maxVal = 255

    difference = cv2.subtract(firstImage, secondImage)
    difference_grayscale = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    retrieval, difference_threshold = cv2.threshold(difference_grayscale, thresh, maxVal, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(difference_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    difference_threshold_copy = difference_threshold.copy()
    difference_threshold_bgr = cv2.cvtColor(difference_threshold_copy, cv2.COLOR_GRAY2BGR)
    difference_with_contours = cv2.drawContours(difference_threshold_bgr, contours, -1, (0, 255, 0), 1);

    return difference_with_contours, contours


# mark parking spot in picture with a rectangle
# crop_coordinates is a tuple of the coordinates of the 4 corners of the rectangle
def find_parking_spot():
    #TODO change to read-resize function
    img = cv2.imread(FIRST_IMAGE_PATH, 1)
    img_scale_factor = 0.7
    base_image = cv2.resize(img, None, fx=img_scale_factor, fy=img_scale_factor, interpolation=cv2.INTER_LINEAR)

    parking_mark = ParkingMark(base_image)
    parking_mark.mark_parking()
    crop_coordinates = parking_mark.get_rectangle_coordinates()
    return crop_coordinates


def parking_MVP():

    num_of_images = get_num_of_images()
    crop_coordinates = find_parking_spot()

    first_image = read_resize_image(FIRST_IMAGE_PATH,IMG_RESIZE_FACTOR)
    first_image_crop = crop_image(first_image, crop_coordinates)

    for image_index in range(2, num_of_images+1):

        second_image = read_resize_image(IMAGE_PATH_TEMPLATE.format(image_index),IMG_RESIZE_FACTOR)
        second_image_crop = crop_image(second_image, crop_coordinates)

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