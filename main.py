#HI THIS IS SUZANNE :D

import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import db
from firebase_admin import storage
from firebase_admin import credentials
import numpy as np
from datetime import datetime


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendease-ec204-default-rtdb.firebaseio.com/",
    'storageBucket': "attendease-ec204.appspot.com"
})

bucket = storage.bucket()

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


#intializing modeType to change the modes later on
modeType = 0
cntr = 0
id = 0
studentIdImage = []


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
    screenBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]  # Adjust index if needed

    if faceCurrentFrame:

        for encodeFace, faceLocation in zip(encodeCurrentFrame, faceCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDistance)

            if matches[matchIndex]:
                y1,x2,y2,x1 = faceLocation
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                bbox = 55 + x1, 162 + y1, x2-x1, y2-y1
                screenBg = cvzone.cornerRect(screenBg, bbox, rt=0)
                id = studentIds[matchIndex]

                if cntr == 0:  # Only retrieve and print studentInfo for the first recognized face
                    print("Registered Student Detected.")
                    print(studentIds[matchIndex])
                    studentInfo = db.reference(f'Students/{id}').get()
                    print(studentInfo)
                    cntr = 1
                    modeType = 1

        if cntr != 0:

            
            if cntr == 1:
                #get image from storage
                    blob = bucket.get_blob(f'Images/{id}.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    #converting the image to a format that can be read by cv2
                    studentIdImage = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

                    #update student attendance data
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                    "%Y-%m-%d %H:%M:%S")
                    
                    secondsElapsed = (datetime.now()-datetimeObject).total_seconds()

                    if secondsElapsed > 30:
                        ref = db.reference(f'Students/{id}')
                        studentInfo['total_attendance'] += 1
                        ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        modeType = 3
                        cntr = 0
                        screenBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                        
            
            if modeType != 3:

                if 10 < cntr < 20:
                    modeType = 2
                
                screenBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if cntr <= 10:
                    cv2.putText(screenBg, str(studentInfo['total_attendance']),(861,125),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)
                    
                    cv2.putText(screenBg, str(studentInfo['major']),(1006,550),
                                cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
                    
                    cv2.putText(screenBg, str(id),(1006,493),
                                cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
                    
                    cv2.putText(screenBg, str(studentInfo['standing']),(910,625),
                                cv2.FONT_HERSHEY_SIMPLEX,0.6,(100,100,100),1)
                    
                    cv2.putText(screenBg, str(studentInfo['year']),(1025,625),
                                cv2.FONT_HERSHEY_SIMPLEX,0.6,(100,100,100),1)
                    
                    cv2.putText(screenBg, str(studentInfo['starting_year']),(1125,625),
                                cv2.FONT_HERSHEY_SIMPLEX,0.6,(100,100,100),1)
                    
                    (width, height), _ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_SIMPLEX,1,1)

                    #we are using a double // because that gets rid of trailing float numbers
                    center_offset = (414 - width)//2
                    cv2.putText(screenBg, str(studentInfo['name']),(808 + center_offset,445),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,50),1)
                    
                    screenBg[175:175 + 216, 909:909 + 216 ] = studentIdImage
            
                cntr += 1

                if cntr >= 20:
                    cntr = 0
                    modeType = 0
                    studentInfo = []
                    studentIdImage = []

                    screenBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        cntr = 0

    cv2.imshow("Face Attendance System", screenBg)
    cv2.waitKey(1)  # Delay is set to 1 millisecond

