import cv2
import face_recognition
import pickle
import os 

studentIds = []

#importing the students' images
imagesFolderPath = 'Images'
imagesPathList = os.listdir(imagesFolderPath)

#initialize the list of modes
studentImageList = []
for path in imagesPathList:
    studentImageList.append(cv2.imread(os.path.join(imagesFolderPath, path)))
    #splitting the id from the .jpeg then isolating it when printing
    studentIds.append(os.path.splitext(path)[0]) 

def findEncodings(imagesList):
    encodeList = []
    for image in imagesList:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Get face encodings if faces are found
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
            # Take the first face encoding if available
            encode = face_encodings[0]
            encodeList.append(encode)
        else:
            # If no face found in the image, you might want to handle this case
            print("No face found in an image.")
            # You can choose to append a default encoding or skip this image
            # encodeList.append(default_encoding)
    
    # Generates all encodings
    return encodeList


print("Encoding Started...")
#saves all new/unknown image encodings into the known encoding list by looping through our student image list
encodeListKnown = findEncodings(studentImageList)

encodeListKnownIds = [encodeListKnown, studentIds]

print("Encoding Completed.")

file = open("EncodingsFile.p", 'wb')
pickle.dump(encodeListKnownIds, file)
file.close()

print("File Saved.")


#can comment this out, for testing if images are imported successfully
# print(len(stdntImagesList))