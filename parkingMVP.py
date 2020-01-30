import cv2
from parking_class import ParkingMark
import matplotlib.pyplot as plt
import os
import os.path


IMG_FILE_PATH = os.path.abspath("input_images")
IMAGE_PATH_TEMPLATE = IMG_FILE_PATH + "\image_{}.jpg"
ALL_SPOTS_EMPTY_IMG = IMG_FILE_PATH + r"\all_spots_empty.jpg"
IMG_RESIZE_FACTOR = 0.7


def get_num_of_images(img_file_path):
    file_count = len([name for name in os.listdir(img_file_path) if os.path.isfile(os.path.join(img_file_path, name))])
    return file_count


def crop_image(img, parking_mark_object):
    crop_top_row = min(parking_mark_object.crop_top_row, parking_mark_object.crop_bottom_row)
    crop_bottom_row = max(parking_mark_object.crop_top_row, parking_mark_object.crop_bottom_row)
    crop_left_column = min(parking_mark_object.crop_left_column, parking_mark_object.crop_right_column)
    crop_right_column = max(parking_mark_object.crop_left_column, parking_mark_object.crop_right_column)
    temp_image_crop = img[crop_top_row:crop_bottom_row, crop_left_column:crop_right_column]
    return temp_image_crop


def read_image(img_path):
    img_resize_factor = IMG_RESIZE_FACTOR
    temp_image = cv2.imread(img_path)
    temp_image_resize = cv2.resize(temp_image, None, fx=img_resize_factor, fy=img_resize_factor, interpolation=cv2.INTER_LINEAR)
    return temp_image_resize


def show_contours_image(results_image, input_image, image_index):
    plt.figure(figsize=[15, 15])
    plt.subplot(121)
    plt.imshow(results_image)
    plt.title("detected contours")
    plt.subplot(122)
    plt.imshow(input_image)
    plt.title("input image #{}".format(image_index))
    plt.show(block=False)
    plt.pause(2)
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
    base_image = read_image(ALL_SPOTS_EMPTY_IMG)
    parking_mark = ParkingMark(base_image)
    parking_mark.mark_parking()
    return parking_mark


def find_biggest_contour(contour_list, image_index):
    try:
        biggest_contour = max(contour_list, key=cv2.contourArea)
    except ValueError:
        print("In image {} parking is free".format(image_index))
        return False
    return biggest_contour


def is_parking_taken(biggest_contour, parking_area_img,image_index):
    if biggest_contour is False:
        return
    #area of contours in units of non-zero pixels
    biggest_contour_area = cv2.contourArea(biggest_contour)
    image_h, image_w = parking_area_img.shape[:2]

    if biggest_contour_area > (image_h * image_w) * 0.3:
        print("In image {} parking is taken".format(image_index))
    else:
        print("Small object found in image {}".format(image_index))


def draw_contour_bounding_box(biggest_contour, difference_with_contours_img):
    if biggest_contour is False:
        return
    top_left_x, top_left_y, width, height = cv2.boundingRect(biggest_contour)
    top_left_corner = (top_left_x, top_left_y)
    bottom_right_corner = (top_left_x + width, top_left_y + height)
    cv2.rectangle(difference_with_contours_img, top_left_corner, bottom_right_corner, color=(0, 0, 255), thickness=2)


def main():
    num_of_images = get_num_of_images(IMG_FILE_PATH)
    parking_mark = mark_parking_spot()

    previous_image = read_image(IMAGE_PATH_TEMPLATE.format(1))
    previous_image_crop = crop_image(previous_image, parking_mark)

    for image_index in range(2, num_of_images):
        current_image = read_image(IMAGE_PATH_TEMPLATE.format(image_index))
        current_image_crop = crop_image(current_image, parking_mark)
        biggest_contour = compare_images(previous_image_crop, current_image_crop, image_index)
        is_parking_taken(biggest_contour, current_image_crop, image_index)
        previous_image_crop = current_image_crop


if __name__ == '__main__':
    main()