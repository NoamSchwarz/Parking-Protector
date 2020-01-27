import cv2
import matplotlib.pyplot as plt
from parking_proj_git.parking_class import ParkingMark
import os
import os.path

#TODO change parking_prij_git ro just parking_proj (how to do this without messing everything up? )
#TODO change parking_class to ParkingMark
#TODO find a funner name for parkingMVP - parking protector?

IMG_FILE_PATH = os.path.abspath("notebook_sequential_images_V2")

IMAGE_PATH_TEMPLATE = IMG_FILE_PATH + "\image_{}.jpg"

FIRST_IMAGE_PATH = IMAGE_PATH_TEMPLATE.format(1)

IMG_RESIZE_FACTOR = 0.7


#TODO: understand how this works because i copied it from stackoverflow
def get_num_of_images(img_file_path):
    file_count = len([name for name in os.listdir(img_file_path) if os.path.isfile(os.path.join(img_file_path, name))])
    return file_count


def crop_image(img, parking_mark_object):
    crop_top_row = parking_mark_object.crop_top_row
    crop_bottom_row = parking_mark_object.crop_bottom_row
    crop_left_colomn = parking_mark_object.crop_left_colomn
    crop_right_colomn = parking_mark_object.crop_right_colomn
    temp_image_crop = img[crop_top_row:crop_bottom_row, crop_left_colomn:crop_right_colomn]
    return temp_image_crop

#TODO put IMG_RESIZE_FACTOR into read_image() , shouldn't be a paramete
def read_image(img_path, img_resize_factor):
    temp_image = cv2.imread(img_path)
    temp_image_resize = cv2.resize(temp_image, None, fx=img_resize_factor, fy=img_resize_factor, interpolation=cv2.INTER_LINEAR)
    return temp_image_resize


def compare_images(first_image, second_image, image_index):
    # for notebook_sequential_images, witch are darker then the notebook from above
    thresh = 50
    maxVal = 255

    difference = cv2.subtract(first_image, second_image)
    difference_grayscale = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    retrieval, difference_threshold = cv2.threshold(difference_grayscale, thresh, maxVal, cv2.THRESH_BINARY)
    #contours is an array
    contours, hierarchy = cv2.findContours(difference_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    difference_threshold_copy = difference_threshold.copy()
    difference_threshold_bgr = cv2.cvtColor(difference_threshold_copy, cv2.COLOR_GRAY2BGR)
    difference_with_contours = cv2.drawContours(difference_threshold_bgr, contours, -1, (0, 255, 0), 1);

    biggest_contour = find_biggest_contour_area(contours, image_index)
    draw_contour_bounding_box(biggest_contour, difference_with_contours)

    cv2.imshow("image {}".format(image_index), difference_with_contours)
    cv2.waitKey(1500)
    cv2.destroyWindow("image {}".format(image_index))

    #return difference_with_contours, contours
    return biggest_contour

# mark parking spot in picture with a rectangle
def find_parking_spot():
    base_image = read_image(FIRST_IMAGE_PATH, IMG_RESIZE_FACTOR)
    parking_mark = ParkingMark(base_image)
    parking_mark.mark_parking()
    return parking_mark

#TODO change to find_biggest_contour because the area calculation is done in is-parking_taken
def find_biggest_contour_area(contour_list, image_index):
    try:
        biggest_contour = max(contour_list, key=cv2.contourArea)
    except ValueError:
        print("no contours detected in image {}".format(image_index))
        return False
    return biggest_contour


def is_parking_taken(biggest_contour, parking_area_img,image_index):
    #TODO check again: what exactly is the unit that contourArea returns
    if biggest_contour is False:
        return
    #area of contours in units of non-zero pixels
    biggest_contour_area = cv2.contourArea(biggest_contour)
    image_h, image_w = parking_area_img.shape[:2]

    if biggest_contour_area > (image_h * image_w) * 0.3:
        print("parking taken in image {}".format(image_index))
    else:
        print("small thing in image {}".format(image_index))


def draw_contour_bounding_box(biggest_contour, difference_with_contours_img):
    if biggest_contour is False:
        return
    top_left_x, top_left_y, width, height = cv2.boundingRect(biggest_contour)
    top_left_corner = (top_left_x, top_left_y)
    borrom_right_corner = (top_left_x + width, top_left_y + height)
    cv2.rectangle(difference_with_contours_img, top_left_corner, borrom_right_corner, color=(0, 0, 255), thickness=2)


def main():
    num_of_images = get_num_of_images(IMG_FILE_PATH)
    #TODO : SEPERATE FIRST IMAGE FROM REST OF THE IMAGES.  call it empty parking lot, so we know it has a special perpous
    # ( empty parking lot can simply be a copy of the first image in the file)
    parking_mark = find_parking_spot()

    first_image = read_image(FIRST_IMAGE_PATH, IMG_RESIZE_FACTOR)
    first_image_crop = crop_image(first_image, parking_mark)

    #TODO: replace get_num_of _images with function of read_next_image which will not be dependant on the source of the
    #TODO read_next_image will replace the current read_image function
    #images, just on the location of the directory the images are in.
    #TODO: replace for loop with while wihch is dependant on get_next_image
    #(for example, if there are no more images, get_next_image will return False, and the loop will exit)
    for image_index in range(2, num_of_images+1):

        second_image = read_image(IMAGE_PATH_TEMPLATE.format(image_index), IMG_RESIZE_FACTOR)
        second_image_crop = crop_image(second_image, parking_mark)

        biggest_contour = compare_images(first_image_crop, second_image_crop, image_index)

        is_parking_taken(biggest_contour, second_image_crop, image_index)

        first_image_crop = second_image_crop


if __name__ == '__main__':
    main()