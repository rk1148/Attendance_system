#step - 5  Database setup


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' :"https://faceattendancerealtime-a6e5b-default-rtdb.firebaseio.com/" 
})

ref = db.reference('Students')

data = {
    "785696":
        {
            "name":"Ms. Dhoni",
            "major": "AI",
            "starting_year": 2017,
            "total_attendance":6,
            "standing":"Good",
            "year":4,
            "last_attendance_time":"2022-12-11  00:54:34" 
        },
        "456789":
        {
            "name":"Raj Khandelwal",
            "major": "AIML",
            "starting_year": 2018,
            "total_attendance":12,
            "standing":"Very Good",
            "year":2,
            "last_attendance_time":"2022-12-11  00:54:34" 
        },
        "789456":
        {
            "name":"Elon Musk",
            "major": "AI",
            "starting_year": 2017,
            "total_attendance":8,
            "standing":"Good",
            "year":5,
            "last_attendance_time":"2022-12-11  00:54:34" 
        }

}
#send the data
for key,value in data.items():
    ref.child(key).set(value)

