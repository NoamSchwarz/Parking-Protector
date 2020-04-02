import cv2
import os

IMG_FILE_PATH = os.path.abspath("input_images")
IMG_PATH_TEMPLATE = IMG_FILE_PATH + "\image_{}.jpg"
IMG_RESIZE_FACTOR = 0.7


def read_image(img_path):
    img_resize_factor = IMG_RESIZE_FACTOR
    temp_image = cv2.imread(img_path)
    temp_image_resize = cv2.resize(temp_image, None, fx=img_resize_factor, fy=img_resize_factor,
                                   interpolation=cv2.INTER_LINEAR)
    return temp_image_resize


class ParkingImage:
    def __init__(self, image_path, image_index):
        self.image = read_image(image_path)
        self.image_index = image_index


    def crop_image(self, parking_mark_object):
        crop_top_row = min(parking_mark_object.crop_top_row, parking_mark_object.crop_bottom_row)
        crop_bottom_row = max(parking_mark_object.crop_top_row, parking_mark_object.crop_bottom_row)
        crop_left_column = min(parking_mark_object.crop_left_column, parking_mark_object.crop_right_column)
        crop_right_column = max(parking_mark_object.crop_left_column, parking_mark_object.crop_right_column)
        temp_image_crop = self.image[crop_top_row:crop_bottom_row, crop_left_column:crop_right_column]
        self.image = temp_image_crop





