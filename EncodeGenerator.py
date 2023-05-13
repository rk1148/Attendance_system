import cv2
# import face_recognition
import os
import pickle

# step-6 add data to data-base
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' :"https://faceattendancerealtime-a6e5b-default-rtdb.firebaseio.com/" ,
    'storageBucket':"faceattendancerealtime-a6e5b.appspot.com"
})
# step-6 



#importing students images 
folderPath = 'Images'
PathList = os.listdir(folderPath)
print(PathList)
imgList = []
studentIds = []

for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    # print(path)
    #print(os.path.splitext(path)[0])
    studentIds.append(os.path.splitext(path)[0])

# step-6 add data to database
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
# stpe-6
print(studentIds)


# #to create /run the encodings
# def findEncodings(imagesList):

#     encodeList = []
#     for img in  imagesList:
#         # step-1 change the color
#         img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)

#     return encodeList


# #call the  function
# print("Encoding started....")
# encodeListKnown = findEncodings(imgList)
# encodeListKnownWithIds = [encodeListKnown,studentIds]
# print("Encoding complete")

# #jo bhi data h meand ids & images ko file me save kr lege
# file = open("EncodeFile.p",'wb')
# pickle.dump(encodeListKnownWithIds,file)
# file.close()
# print("File saved")
