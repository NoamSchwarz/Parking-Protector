from cv2 import *
import time
import os

# takes signle image and saves it
# initialize the camera
# cam = VideoCapture(0)   # 0 -> index of camera
# s, img = cam.read()
# if s:    # frame captured without any errors
#     namedWindow("cam-test")
#     imshow("cam-test",img)
#     waitKey(0)
#     destroyWindow("cam-test")
#     imwrite("homeparking2.jpg",img) #save image


# re-running function using system vlock
starttime=time.time()
path = r"C:\Users\noamn\Documents\shecodes\parking_project\parking_proj_git\test pictures\notebook_sequential_images"
imageCounter = 1

while True:
    cam = VideoCapture(1,cv2.CAP_DSHOW)   # 0 -> index of camera
    s, img = cam.read()
    if s:    # frame captured without any errors
       # namedWindow("cam-test")
        imshow("image #%d.jpg" %imageCounter,img)
        waitKey(1500)
      #  destroyWindow("cam-test")
        cv2.imwrite(os.path.join(path, "image_%d.jpg" %imageCounter), img)
    cam.release()
    cv2.destroyAllWindows()
    imageCounter += 1

    time.sleep(20.0 - ((time.time() - starttime) % 20.0))



