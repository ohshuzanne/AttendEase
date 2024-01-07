import cv2
import os

#Setting the camera number that you are using and the height/width because we are going to use graphics later on
capture = cv2.VideoCapture(0)
capture.set(3,640)
capture.set(4,480)

screenBg = cv2.imread('Resources/background.png')


#importing the images in modes directory into a list
#set the directory to the mode folder within the resources folder
modeFolderPath = 'Resources/Modes'
modePathList = os.listdir(modeFolderPath)
#initialize the list of modes

imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(modeFolderPath, path)))


#This is the standard code to run your webcam
while True:
    success, img = capture.read()

    #we are setting where the webcam capture is showing (basically in the box)
    #this is a method to overlay your webcam INTO the graphics (background image)
    screenBg[162:162 + 480, 55:55 + 640] = img
    screenBg[44:44 + 633, 808:808 + 414] = imgModeList[1] 

    cv2.imshow("Face Attendance System",screenBg)
    cv2.waitKey(1) #delay is set to 1 ms