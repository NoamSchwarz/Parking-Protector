import cv2

#for next time:
#instead of showing croped image, save it to file.

topLeft = None
bottomRight = None
cropTopRow = None
cropBottomRow = None
cropLeftColomn = None
cropRightColomn = None
cropedImage = None

def cropRectangle(action, x,y,flags, userdata):
    global topLeft,bottomRight,cropTopRow,cropBottomRow,cropLeftColomn,cropRightColomn

    if action==cv2.EVENT_LBUTTONDOWN:
        topLeft = (x,y)
        cropTopRow,cropLeftColomn = y,x

        cv2.rectangle(source,topLeft,topLeft,(100,0,0),thickness=5, lineType=cv2.LINE_8)
    elif action==cv2.EVENT_LBUTTONUP:
        bottomRight = (x,y)
        cropBottomRow,cropRightColomn = y,x
        cv2.rectangle(source, topLeft, bottomRight, (100, 0, 0), thickness=5, lineType=cv2.LINE_8)
        cv2.imshow("window", source)

        cropedImage = dummy[cropTopRow:cropBottomRow, cropLeftColomn:cropRightColomn]
        # cv2.imshow("croped", cropedImage)
        # cv2.waitKey(1000)

        cv2.imwrite("croped.png", cropedImage)


sourcePath  = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\10.12 view above notebook\view_above_notebbok_in_order\image_1.jpeg"
img= cv2.imread(sourcePath, 1)
cv2.imshow("img",img)
cv2.waitKey(2000)
source = cv2.resize(img,None,fx=0.5,fy=0.5,interpolation= cv2.INTER_LINEAR)
# Make a dummy image, will be useful to clear the drawing
dummy = source.copy()
cv2.namedWindow("Window")
# highgui function called when mouse events occur
cv2.setMouseCallback("Window", cropRectangle)
k = 0
# loop until escape character is pressed
while k != 27:
    cv2.putText(source, 'Choose top left corner and drag to crop',
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2);
    cv2.putText(source, 'press ESC to exit',
                (10, 55), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2);
    cv2.imshow("Window", source)
    k = cv2.waitKey(20) & 0xFF
