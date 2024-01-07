import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone

# Setting the camera number that you are using and the height/width because we are going to use graphics later on
capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)

screenBg = cv2.imread('Resources/background.png')

# Importing the images in modes directory into a list
# Set the directory to the mode folder within the resources folder
modeFolderPath = 'Resources/Modes'
modePathList = os.listdir(modeFolderPath)
# Initialize the list of modes
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(modeFolderPath, path)))

# Load the encodings file
file = open("EncodingsFile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds

# This is the standard code to run your webcam
while True:
    success, img = capture.read()

    imageSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imageSmall = cv2.cvtColor(imageSmall, cv2.COLOR_BGR2RGB)

    faceCurrentFrame = face_recognition.face_locations(imageSmall)
    encodeCurrentFrame = face_recognition.face_encodings(imageSmall, faceCurrentFrame)

    # We are setting where the webcam capture is showing (basically in the box)
    # This is a method to overlay your webcam INTO the graphics (background image)
    screenBg[162:162 + 480, 55:55 + 640] = img
    # Use the correct index for the mode image
    screenBg[44:44 + 633, 808:808 + 414] = imgModeList[0]  # Adjust index if needed

    for encodeFace, faceLocation in zip(encodeCurrentFrame, faceCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDistance)

        if matches[matchIndex]:
            print("Registered Student Detected.")
            print(studentIds[matchIndex])
            y1,x2,y2,x1 = faceLocation
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            bbox = 55 + x1, 162 + y1, x2-x1, y2-y1
            screenBg = cvzone.cornerRect(screenBg, bbox, rt=0)
        else:
            print("Not a registered student. Please register yourself at the admin's office.")

    cv2.imshow("Face Attendance System", screenBg)
    cv2.waitKey(1)  # Delay is set to 1 millisecond
