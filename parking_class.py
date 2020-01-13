import cv2

class MarkParking:

    #TODO: should baseImage and imgScaleFactor be classe atributes?
    baseImagePath = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\notebook_sequential_images\image_1.jpg"
    img = cv2.imread(baseImagePath, 1)
    imgScaleFactor = 0.7
    baseImage = cv2.resize(img, None, fx=imgScaleFactor, fy=imgScaleFactor, interpolation=cv2.INTER_LINEAR)

    def __init__(self):
        self.topLeft = None
        self.bottomRight = None
        self.cropTopRow = None
        self.cropBottomRow = None
        self.cropLeftColomn = None
        self.cropRightColomn = None

    def draw_rectangle(self, action, x, y, flags, userdata):

        if action == cv2.EVENT_LBUTTONDOWN:
            self.topLeft = (x, y)
            self.cropTopRow = y
            self.cropLeftColomn = x

            cv2.rectangle(self.baseImage, self.topLeft, self.topLeft, (100, 0, 0), thickness=5, lineType=cv2.LINE_8)
        elif action == cv2.EVENT_LBUTTONUP:
            self.bottomRight = (x, y)
            self.cropBottomRow = y
            self.cropRightColomn = x
            cv2.rectangle(self.baseImage, self.topLeft, self.bottomRight, (100, 0, 0), thickness=5, lineType=cv2.LINE_8)


    def put_white_text(self, img, x, y, text):
        cv2.putText(self.baseImage, '{}'.format(text),
                    (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 1);

    def mark_parking(self):
        ESC_KEY = 27

        cv2.namedWindow("Window")
        # highgui function called when mouse events occur
        cv2.setMouseCallback("Window", self.draw_rectangle)
        key = 0

        # TODO: change to for loop?
        while key != ESC_KEY:
            self.put_white_text(self.baseImage, 10, 30, 'Choose top left corner and drag to crop')
            self.put_white_text(self.baseImage, 10, 55, 'press ESC to exit')
            cv2.imshow("Window", self.baseImage)
            key = cv2.waitKey(20) & 0xFF

    def get_rectangle_coordinates(self):
        return self.cropTopRow, self.cropBottomRow, self.cropLeftColomn, self.cropRightColomn

