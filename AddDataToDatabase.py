import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendease-ec204-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "tp012345":{
        "name": "Shi Yuqi",
        "major": "Physical Education",
        "starting_year": 2017,
        "total_attendance": 6,
        "standing": "A+",
        "year": 4,
        "last_attendance_time": "2024-01-08 14:10:30"
    },
    "tp054321":{
        "name": "Elon Musk",
        "major": "Ruining Lives",
        "starting_year": 1995,
        "total_attendance": 10,
        "standing": "A+",
        "year": 29,
        "last_attendance_time": "2024-01-08 13:10:30"
    },
    "tp063338":{
        "name": "Dalton Gan",
        "major": "Software Engineering",
        "starting_year": 2024,
        "total_attendance": 100,
        "standing": "A++",
        "year": 2,
        "last_attendance_time": "2024-01-02 12:06:02"
    },
    "tp068713":{
        "name": "Suzanne Lai",
        "major": "Artifical Intelligence",
        "starting_year": 2022,
        "total_attendance": 50,
        "standing": "A",
        "year": 2,
        "last_attendance_time": "2024-01-02 15:09:02"
    },
    "tp088888":{
        "name": "Karina",
        "major": "Slay",
        "starting_year": 2024,
        "total_attendance": 10,
        "standing": "A+",
        "year": 1,
        "last_attendance_time": "2024-01-09 06:06:06"
    },
    
    
}

for key,value in data.items():
    ref.child(key).set(value)