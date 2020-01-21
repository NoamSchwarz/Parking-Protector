import cv2

class ParkingMark:

    def __init__(self, base_image):
        self.top_left = None
        self.bottom_right = None
        self.crop_top_row = None
        self.crop_bottom_row = None
        self.crop_left_colomn = None
        self.crop_right_colomn = None
        self.base_image = base_image

    def draw_rectangle(self, action, x, y, flags, userdata):
        if action == cv2.EVENT_LBUTTONDOWN:
            self.top_left = (x, y)
            self.crop_top_row = y
            self.crop_left_colomn = x

            cv2.rectangle(self.base_image, self.top_left, self.top_left, (100, 0, 0), thickness=5, lineType=cv2.LINE_8)
        elif action == cv2.EVENT_LBUTTONUP:
            self.bottom_right = (x, y)
            self.crop_bottom_row = y
            self.crop_right_colomn = x
            cv2.rectangle(self.base_image, self.top_left, self.bottom_right, (100, 0, 0), thickness=5, lineType=cv2.LINE_8)

    def put_white_text(self, img, x, y, text):
        cv2.putText(img, '{}'.format(text), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

    def mark_parking(self):
        ESC_KEY = 27

        cv2.namedWindow("Window")
        # highgui function called when mouse events occur
        cv2.setMouseCallback("Window", self.draw_rectangle)
        key = 0

        while key != ESC_KEY:
            self.put_white_text(self.base_image, 10, 55, 'press ESC to exit')
            self.put_white_text(self.base_image, 10, 30, 'Choose top left corner and drag to crop')
            cv2.imshow("Window", self.base_image)
            key = cv2.waitKey(20) & 0xFF
        cv2.destroyWindow("Window")


