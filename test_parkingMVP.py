import unittest
import cv2
import os
from parking_proj_git import parkingMVP


class TestParkingMVP(unittest.TestCase):

    def setUp(self):
        self.input_file_path = os.path.abspath("input_images")

    # only relevant when using input from file instead of camera
    def test_get_num_of_images(self):
        image_count = parkingMVP.get_num_of_images(self.input_file_path)
        self.assertEqual(image_count, 17)


    def test_compare_images(self):

        expected = "[[[118   7]] [[118   9]] [[116  11]] [[112  11]] [[111  10]] [[111  12]] [[110  13]] [[108  11]]" \
                   " [[106  11]] [[105  12]] [[105  15]] [[104  16]] [[105  17]] [[105  18]] [[104  19]] [[103  19]] " \
                   "[[101  21]] [[100  20]] [[ 99  20]] [[ 98  19]] [[ 97  19]] [[ 96  18]] [[ 94  18]] [[ 92  16]] " \
                   "[[ 91  17]] [[ 90  17]] [[ 88  15]] [[ 80  15]] [[ 79  14]] [[ 80  13]] [[ 78  15]] [[ 64  15]]" \
                   " [[ 63  16]] [[ 56  16]] [[ 55  17]] [[ 54  17]] [[ 54  18]] [[ 53  19]] [[ 51  19]] [[ 49  21]]" \
                   " [[ 48  21]] [[ 47  22]] [[ 46  22]] [[ 45  23]] [[ 44  23]] [[ 43  24]] [[ 41  24]] [[ 40  25]]" \
                   " [[ 37  25]] [[ 36  24]] [[ 36  19]] [[ 35  18]] [[ 35  17]] [[ 32  17]] [[ 31  16]] [[ 29  16]]" \
                   " [[ 28  15]] [[ 27  15]] [[ 26  14]] [[ 26  13]] [[ 25  12]] [[ 25  10]] [[ 25  11]] [[ 23  13]]" \
                   " [[ 23  14]] [[ 24  15]] [[ 24  19]] [[ 25  20]] [[ 25  22]] [[ 24  23]] [[ 23  22]] [[ 23  21]]" \
                   " [[ 23  25]] [[ 24  26]] [[ 24  28]] [[ 25  29]] [[ 25  31]] [[ 26  32]] [[ 26  38]] [[ 27  39]] " \
                   "[[ 27  40]] [[ 29  42]] [[ 30  42]] [[ 31  43]] [[ 31  45]] [[ 34  48]] [[ 35  48]] [[ 36  49]] " \
                   "[[ 40  49]] [[ 41  50]] [[ 42  49]] [[ 43  49]] [[ 44  50]] [[ 57  50]] [[ 58  49]] [[ 59  49]] " \
                   "[[ 60  50]] [[ 62  50]] [[ 63  49]] [[ 71  49]] [[ 72  48]] [[ 82  48]] [[ 83  47]] [[ 84  48]] " \
                   "[[ 87  48]] [[ 88  47]] [[101  47]] [[102  46]] [[104  46]] [[105  47]] [[106  46]] [[114  46]]" \
                   " [[115  45]] [[122  45]] [[123  44]] [[126  44]] [[127  43]] [[128  43]] [[130  41]] [[131  41]] " \
                   "[[131  37]] [[132  36]] [[132  34]] [[133  33]] [[133  26]] [[132  25]] [[132  22]] [[131  21]] " \
                   "[[131  20]] [[130  19]] [[130  18]] [[129  17]] [[129  16]] [[127  14]] [[127  13]] [[125  11]]" \
                   " [[125  10]] [[124   9]] [[122   9]] [[121   8]] [[121   7]] [[121   8]] [[120   9]] [[119   8]]" \
                   " [[119   7]]]"

        test_image_file_path = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\test_compare_images_function"
        prev_image = cv2.imread(test_image_file_path + "\image_2_cropped.jpg")
        curr_image = cv2.imread(test_image_file_path + "\image_3_cropped.jpg")
        result = parkingMVP.compare_images(prev_image, curr_image, 3)
        actual = str(result).replace("\n", "")
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
