import cv2
import matplotlib.pyplot as plt
from parking_proj_git.parking_class import ParkingMark

#TODO change parking_prij_git ro just parking_proj (how to do this without messing everything up? )
#TODO change parking_class to ParkingMark
#TODO find a funner name for parkingMVP - parking protector?

IMAGE_PATH_TEMPLATE = (r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git" 
                          r"\test pictures\notebook_sequential_images\image_{}.jpg")
FIRST_IMAGE_PATH = IMAGE_PATH_TEMPLATE.format(1)

#TODO: run autocrop test with images 12 and 13 to see if change of thresh is needed for correct output
#it does. needs a thresh of ~35 for correct result.

#TODO: have in parking_class as well. (as parmeter?)
IMG_RESIZE_FACTOR = 0.7

def get_num_of_images():
    #TODO: Get the values automatically
    return 14

#TODO use ParkingMark object for the coordinates instead if the tuple. add parking obkect as parameter for crop_image function
# currently, the mark_parking object is made in the find_parking_spot function, so it isn't found in parking_mvp


def crop_image(img, crop_coordinates):
    cropTopRow, cropBottomRow, cropLeftColomn, cropRightColomn = crop_coordinates
    tempImageCrop = img[cropTopRow:cropBottomRow, cropLeftColomn:cropRightColomn]
    return tempImageCrop

# def crop_image(img, mark_parking_obj):
#     cropTopRow = mark_parking_obj.crop_top_row
#     cropBottomRow = mark_parking_obj.crop_bottom_row
#     cropLeftColomn = mark_parking_obj.crop_left_colomn
#     cropRightColomn = mark_parking_obj.crop_right_colomn
#     tempImageCrop = img[cropTopRow:cropBottomRow, cropLeftColomn:cropRightColomn]
#     return tempImageCrop

def read_resize_image(img_path, img_resize_factor):
    temp_image = cv2.imread(img_path)
    temp_image_resize = cv2.resize(temp_image, None, fx=img_resize_factor, fy=img_resize_factor, interpolation=cv2.INTER_LINEAR)
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

    base_image = read_resize_image(FIRST_IMAGE_PATH, IMG_RESIZE_FACTOR)
    parking_mark = ParkingMark(base_image)
    parking_mark.mark_parking()
    crop_coordinates = parking_mark.get_rectangle_coordinates()
    return crop_coordinates

def find_biggest_contour_area(contour_list, image_index):
    # TODO: can this block be a seperate function?
    try:
        biggest_contour = max(contour_list, key=cv2.contourArea)
    except ValueError:
        print("no contours detected in image {}".format(image_index))
        return False
    return biggest_contour

def is_parking_taken(biggest_contour, parking_area_img,image_index):

    biggest_contour_area = cv2.contourArea(biggest_contour)
    image_h, image_w = parking_area_img.shape[:2]

    if biggest_contour_area > (image_h * image_w) * 0.3:
        print("parking taken in image {}".format(image_index))
    else:
        print("small thing in image {}".format(image_index))

def draw_contour_bounding_box(biggest_contour, difference_with_contours_img):
    top_left_x, top_left_y, width, height = cv2.boundingRect(biggest_contour)
    top_left_corner = (top_left_x, top_left_y)
    borrom_right_corner = (top_left_x + width, top_left_y + height)
    cv2.rectangle(difference_with_contours_img, top_left_corner, borrom_right_corner, color=(0, 0, 255), thickness=2)


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

        biggest_contour = find_biggest_contour_area(contours, image_index)

        if biggest_contour is False:
            continue

        is_parking_taken(biggest_contour, second_image_crop, image_index)

        draw_contour_bounding_box(biggest_contour, difference_with_contours)

        cv2.imshow("image {}".format(image_index),difference_with_contours)
        cv2.waitKey(1500)
        cv2.destroyWindow("image {}".format(image_index))

       # first_image_crop = second_image_crop
        #TODO: decide weather to procese after spot is taken or to stop the procces.
        #if the former, do I need to be able to idenify when the taken spot has become empty?


parking_MVP()

#! Other notes:
#! - Automatic formatting
#! - Linters and inspections
#! - __main__
#! - argparse
#! - Generators