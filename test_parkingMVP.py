import unittest
import cv2
from parking_proj_git import parkingMVP

#TODO: test for cropImage
# have pairs of an image, and the crop of the image that is supposed to come out. compare the two.
# another option, check to see if the size of the cropped image is what it is supposed to come out.

#TODO test for compaer_images
#input two images, and have the output for difference_with_contours and the contour list that is supposed to come out
#compare the output that we are supposed to get to what we actually get.
#have an array with pairs of images, and another array with the desierd output.

class TestCompareImages(unittest.TestCase):

    def setUp(self):
        first_image_path = (r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures"
        r"\test_compare_images_function\notebook_sequential_images_image_2_crop.png")

        second_image_path = (r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures"
        r"\test_compare_images_function\notebook_sequential_images_image_3_crop.png")

        correct_result_path = (r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git"
                       r"\test pictures\test_compare_images_function\result_for_images_2_and_3.png")

        self.first_image = cv2.imread(first_image_path)
        self.second_image= cv2.imread(second_image_path)
        self.correct_result = cv2.imread(correct_result_path)

    #TODO compare_images now returns only biggest_contour, so this test doesn't work anymore
    def test_compare_images(self):
        parkingMVP.compare_images(self.first_image,self.second_image,2)
        result,contours = parkingMVP.compare_images(self.first_image, self.second_image,2)
        output = "not correct"
        if result.all() == self.correct_result.all():
            output = "correct"
        self.assertEquals(output,"correct")

if __name__ == '__main__':
    unittest.main()

#TODO: test for parkiingMVP
#have two image, and the apropriate output (parking taken/not taken) for those two images.
# have a list of tuples, where each tuple is an image and the opropriate output for that image (parking taken/not taken)