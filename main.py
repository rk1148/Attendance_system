import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone

#step-7  
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


from datetime import datetime

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' :"https://faceattendancerealtime-a6e5b-default-rtdb.firebaseio.com/" ,
    'storageBucket':"faceattendancerealtime-a6e5b.appspot.com"
})

bucket = storage.bucket()

//***************************************** step-1
vedio_capture = cv2.VideoCapture(0)
vedio_capture.set(3,640)   #width of webcam window
vedio_capture.set(4,480)    #height of webcam window

************************************ step-1




/***************  step -2 --> graphics(import all the pictures for background graphics)
## import the mode images into the list 
imgBackground = cv2.imread('Resources/background.png')
#importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
# print(len(imgModeList))
/************************************** step-2



/************************************  step -4 Face recgnition
# load the encoding file
print("Loading Encode file....")
file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown,studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

#step-7
modeType = 0
counter =  0
id = -1
imgStudent = [] 


#overlay(ek k uper ek) webcam on the backgroung img
while True:
    success, img = vedio_capture.read()


    #image size ko chota krne k lia beacause it takes a lot of computation power
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    #conver it from rgb to bgr
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)            // step-3

    # once we done we need to feed in the value to our face recognition system it will detect and then it will give us some output . we need two things, 1. the faces in the current frame 2. encodeings in the current frame
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS,faceCurFrame)

    # imgBackground[162:162 + 480, 55:55 + 640] = img
    # imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


    #Agar face ko detect kr pa rha h to
    if faceCurFrame : 
        #we are going to loop through all these encodings and one by one we are going to compare it with our generated encodings whether they match or not
        for encodeFace,facelocatio in zip(encodeCurrFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #  print("matches", matches)
            #  print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            #  print("Match Index",matchIndex)

            if matches[matchIndex]:
                #  print("Known face Detection")
                #  studentIds[matchIndex]
                y1, x2, y2, x1 = facelocatio
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1,162+y1, x2-x1, y2-y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0) #rt = rectangle thickness

                #step7
                id = studentIds[matchIndex]
                # print(id)
                if counter == 0:
                    cvzone.putTextRect(imgBackground,"Loading",(275,400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)      #wait foe 1 mili second
                    counter = 1
                    modeType =1

        if counter!= 0:
            #for first frame
            if counter == 1:
                # get the data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo) 
                # get the image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(),np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR) 
                #step-8 update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],"%Y-%m-%d %H:%M:%S")

                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed) 

                if secondsElapsed > 30:  
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter  = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            # check do we have need to update it 
            if modeType != 3:

                if 10<counter<20:
                    modeType =2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]   
                
                #
                if counter<=10:
                    # step -7
                    cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125),
                                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    cv2.putText(imgBackground,str(studentInfo['major']),(1006,550),
                                cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgBackground,str(studentInfo['Id']),(1006 ,493),
                                cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgBackground,str(studentInfo['standing']),(910,625),
                                cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackground,str(studentInfo['year']),(1025,625),
                                cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackground,str(studentInfo['starting year']),(1125,625),
                                cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    
                    #name ko shi jgh pr rkhne k lia twxt ka size find krk, use total length me se minus krk use divide by 2 pe jo jgh aayega ,vhi se ise start krege.
                    (w,h), _ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (414-w)//2
                    cv2.putText(imgBackground,str(studentInfo['name']),(808+offset,445),
                                cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
                    
                    imgBackground[175:175+216,909:909+216] = imgStudent
            

                counter+=1

                if counter>=20:
                    counter  = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent  = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]   

    # Agar face detect nhinn ho rha h to 
    else:
        modeType = 0
        counter  = 0
 


    # cv2.imshow("webcam",img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)

    

