import cv2
from parking_class import ParkingMark
from image_class import ParkingImage
import matplotlib.pyplot as plt
import os
import os.path


IMG_FILE_PATH = os.path.abspath("input_images")
IMAGE_PATH_TEMPLATE = IMG_FILE_PATH + "\image_{}.jpg"
ALL_SPOTS_EMPTY_IMG = IMG_FILE_PATH + r"\all_spots_empty.jpg"
IMG_RESIZE_FACTOR = 0.7


def get_num_of_images(img_file_path):
    image_count = len([name for name in os.listdir(img_file_path) if os.path.isfile(os.path.join(img_file_path, name))])
    return image_count


def show_contours_image(results_image, input_image, image_index):
    plt.figure(figsize=[10, 10])
    plt.subplot(121)
    plt.imshow(results_image)
    plt.title("detected contours")
    plt.subplot(122)
    plt.imshow(input_image)
    plt.title("input image #{}".format(image_index))
    plt.show(block=False)
    plt.pause(1)
    plt.close()


def compare_images(first_image, second_image, image_index):

    thresh = 50
    max_val = 255

    difference = cv2.subtract(first_image, second_image)
    difference_grayscale = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    retrieval, difference_threshold = cv2.threshold(difference_grayscale, thresh, max_val, cv2.THRESH_BINARY)
    #contours is an array
    contours, hierarchy = cv2.findContours(difference_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    difference_threshold_copy = difference_threshold.copy()
    difference_threshold_bgr = cv2.cvtColor(difference_threshold_copy, cv2.COLOR_GRAY2BGR)
    difference_with_contours = cv2.drawContours(difference_threshold_bgr, contours, -1, (0, 255, 0), 1)

    biggest_contour = find_biggest_contour(contours, image_index)
    draw_contour_bounding_box(biggest_contour, difference_with_contours)

    show_contours_image(difference_with_contours, second_image,image_index)

    return biggest_contour


def mark_parking_spot():
    base_image = ParkingImage(ALL_SPOTS_EMPTY_IMG,0)
    parking_mark = ParkingMark(base_image)
    parking_mark.mark_parking()
    return parking_mark


def find_biggest_contour(contour_list, image_index):
    try:
        biggest_contour = max(contour_list, key=cv2.contourArea)
    except ValueError:
        print("In image {} parking is free".format(image_index))
        return []
    return biggest_contour


def is_parking_taken(biggest_contour, parking_area_img, image_index):
    if biggest_contour == []:
        return
    #area of contours in units of non-zero pixels
    biggest_contour_area = cv2.contourArea(biggest_contour)
    image_h, image_w = parking_area_img.shape[:2]

    if biggest_contour_area > (image_h * image_w) * 0.3:
        print("Parking is taken in image {}".format(image_index))
    else:
        print("Small object found in image {}".format(image_index))



def draw_contour_bounding_box(biggest_contour, difference_with_contours_img):
    # can't check "if not biggist_contour" because when biggest_contour is a numpy.ndarray (usually) that gives an error
    if biggest_contour == []:
        return
    top_left_x, top_left_y, width, height = cv2.boundingRect(biggest_contour)
    top_left_corner = (top_left_x, top_left_y)
    bottom_right_corner = (top_left_x + width, top_left_y + height)
    cv2.rectangle(difference_with_contours_img, top_left_corner, bottom_right_corner, color=(0, 0, 255), thickness=2)


def main():
    num_of_images = get_num_of_images(IMG_FILE_PATH)
    parking_mark = mark_parking_spot()

    previous_image = ParkingImage(IMAGE_PATH_TEMPLATE.format(1),1)
    previous_image.crop_image(parking_mark)

    for image_index in range(2, num_of_images):
        current_image = ParkingImage(IMAGE_PATH_TEMPLATE.format(image_index),image_index)
        current_image.crop_image(parking_mark)
        biggest_contour = compare_images(previous_image.image, current_image.image, image_index)
        is_parking_taken(biggest_contour, current_image.image, image_index)
        previous_image = current_image


if __name__ == '__main__':
    main()