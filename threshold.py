import cv2

windowName = "threshold image"
trackbarValue = "threshold scale"
scaleFactor = 0
maxScale = 255
imagePath = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\difference.png"

im = cv2.imread(imagePath)
src = cv2.resize(im,None,fx=0.5,fy=0.5,interpolation= cv2.INTER_LINEAR)
srcGreyscale = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
cv2.namedWindow(windowName,cv2.WINDOW_AUTOSIZE)

def threshold_image(*args):
    global scaleFactor
    scaleFactor = 0 + args[0]
    #change the thresholding type and see how it changes the result!
    th,dst = cv2.threshold(srcGreyscale,scaleFactor,maxScale,cv2.THRESH_BINARY)
    cv2.imshow(windowName,dst)

cv2.createTrackbar(trackbarValue, windowName, scaleFactor, maxScale, threshold_image)

threshold_image(0)
while True:
    c = cv2.waitKey(20)
    if c==27:
        break

cv2.destroyAllWindows()