# pip install --upgrade google-api-python-client
# pip install --upgrade oauth2client
# pip install --upgrade google-auth-oauthlib

import google.oauth2.credentials
import json
import re
import sys
import xml.etree.ElementTree as et
import zipfile

from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from math import cos, sin, sqrt

listActivityTypeGoogle = {
    "Aerobics": 9,
    "Archery": 119,
    "Badminton": 10,
    "Baseball": 11,
    "Basketball": 12,
    "Biathlon": 13,
    "Biking": 1,
    "Handbiking": 14,
    "Mountain biking": 15,
    "Road biking": 16,
    "Spinning": 17,
    "Stationary biking": 18,
    "Utility biking": 19,
    "Boxing": 20,
    "Calisthenics": 21,
    "Circuit training": 22,
    "Cricket": 23,
    "Crossfit": 113,
    "Curling": 106,
    "Dancing": 24,
    "Diving": 102,
    "Elevator": 117,
    "Elliptical": 25,
    "Ergometer": 103,
    "Escalator": 118,
    "Fencing": 26,
    "Football (American)": 27,
    "Football (Australian)": 28,
    "Football (Soccer)": 29,
    "Frisbee": 30,
    "Gardening": 31,
    "Golf": 32,
    "Gymnastics": 33,
    "Handball": 34,
    "HIIT": 114,
    "Hiking": 35,
    "Hockey": 36,
    "Horseback riding": 37,
    "Housework": 38,
    "Ice skating": 104,
    "In vehicle": 0,
    "Interval Training": 115,
    "Jumping rope": 39,
    "Kayaking": 40,
    "Kettlebell training": 41,
    "Kickboxing": 42,
    "Kitesurfing": 43,
    "Martial arts": 44,
    "Meditation": 45,
    "Mixed martial arts": 46,
    "On foot": 2,
    "Other (unclassified fitness activity)": 108,
    "P90X exercises": 47,
    "Paragliding": 48,
    "Pilates": 49,
    "Polo": 50,
    "Racquetball": 51,
    "Rock climbing": 52,
    "Rowing": 53,
    "Rowing machine": 54,
    "Rugby": 55,
# continued
    "Running": 8,
    "Jogging": 56,
    "Running on sand": 57,
    "Running (treadmill)": 58,
    "Sailing": 59,
    "Scuba diving": 60,
    "Skateboarding": 61,
    "Skating": 62,
    "Cross skating": 63,
    "Indoor skating": 105,
    "Inline skating (rollerblading)": 64,
    "Skiing": 65,
    "Back-country skiing": 66,
    "Cross-country skiing": 67,
    "Downhill skiing": 68,
    "Kite skiing": 69,
    "Roller skiing": 70,
    "Sledding": 71,
    "Sleeping": 72,
    "Light sleep": 109,
    "Deep sleep": 110,
    "REM sleep": 111,
    "Awake (during sleep cycle)": 112,
    "Snowboarding": 73,
    "Snowmobile": 74,
    "Snowshoeing": 75,
    "Softball": 120,
    "Squash": 76,
    "Stair climbing": 77,
    "Stair-climbing machine": 78,
    "Stand-up paddleboarding": 79,
    "Still (not moving)": 3,
    "Strength training": 80,
    "Surfing": 81,
    "Swimming": 82,
    "Swimming (open water)": 84,
    "Swimming (swimming pool)": 83,
    "Table tennis (ping pong)": 85,
    "Team sports": 86,
    "Tennis": 87,
    "Tilting (sudden device gravity change)": 5,
    "Treadmill (walking or running)": 88,
    "Unknown (unable to detect activity)": 4,
    "Volleyball": 89,
    "Volleyball (beach)": 90,
    "Volleyball (indoor)": 91,
    "Wakeboarding": 92,
    "Walking": 7,
    "Walking (fitness)": 93,
    "Nording walking": 94,
    "Walking (treadmill)": 95,
    "Walking (stroller)": 116,
    "Waterpolo": 96,
    "Weightlifting": 97,
    "Wheelchair": 98,
    "Windsurfing": 99,
    "Yoga": 100,
    "Zumba": 101
}

listWorkoutMapping = {
#Individual Sports
    "HKWorkoutActivityTypeArchery": "Archery",
    "HKWorkoutActivityTypeBowling": "Other (unclassified fitness activity)",
    "HKWorkoutActivityTypeFencing": "Fencing",
    "HKWorkoutActivityTypeGymnastics": "Gymnastics",
    "HKWorkoutActivityTypeTrackAndField": "Other (unclassified fitness activity)",
#Team Sports
    "HKWorkoutActivityTypeAmericanFootball": "Football (American)",
    "HKWorkoutActivityTypeAustralianFootball": "Football (Australian)",
    "HKWorkoutActivityTypeBaseball": "Baseball",
    "HKWorkoutActivityTypeBasketball": "Basketball",
    "HKWorkoutActivityTypeCricket": "Cricket",
    "HKWorkoutActivityTypeHandball": "Handball",
    "HKWorkoutActivityTypeHockey": "Hockey",
    "HKWorkoutActivityTypeLacrosse": "Team sports",
    "HKWorkoutActivityTypeRugby": "Rugby",
    "HKWorkoutActivityTypeSoccer": "Football (Soccer)",
    "HKWorkoutActivityTypeSoftball": "Softball",
    "HKWorkoutActivityTypeVolleyball": "Volleyball",
#Exercise and Fitness
    "HKWorkoutActivityTypePreparationAndRecovery": "Calisthenics",
    "HKWorkoutActivityTypeFlexibility": "Calisthenics",
    "HKWorkoutActivityTypeWalking": "Walking",
    "HKWorkoutActivityTypeRunning": "Running",
    "HKWorkoutActivityTypeWheelchairWalkPace": "Wheelchair",
    "HKWorkoutActivityTypeWheelchairRunPace": "Wheelchair",
    "HKWorkoutActivityTypeCycling": "Biking",
    "HKWorkoutActivityTypeHandCycling": "Handbiking",
    "HKWorkoutActivityTypeCoreTraining": "Calisthenics",
    "HKWorkoutActivityTypeElliptical": "Elliptical",
    "HKWorkoutActivityTypeFunctionalStrengthTraining": "Strength training",
    "HKWorkoutActivityTypeTraditionalStrengthTraining": "Strength training",
    "HKWorkoutActivityTypeCrossTraining": "Crossfit",
    "HKWorkoutActivityTypeMixedCardio": "Spinning",
    "HKWorkoutActivityTypeHighIntensityIntervalTraining": "HIIT",
    "HKWorkoutActivityTypeJumpRope": "Jumping rope",
    "HKWorkoutActivityTypeStairClimbing": "Stair-climbing machine",
    "HKWorkoutActivityTypeStairs": "Stair climbing",
    "HKWorkoutActivityTypeStepTraining": "Aerobics",
#Studio Activities
    "HKWorkoutActivityTypeBarre": "Pilates",
    "HKWorkoutActivityTypeDance": "Other (unclassified fitness activity)",
    "HKWorkoutActivityTypeYoga": "Yoga",
    "HKWorkoutActivityTypeMindAndBody": "Meditation",
    "HKWorkoutActivityTypePilates": "Pilates",
#Racket Sports
    "HKWorkoutActivityTypeBadminton": "Badminton",
    "HKWorkoutActivityTypeRacquetball": "Racquetball",
    "HKWorkoutActivityTypeSquash": "Squash",
    "HKWorkoutActivityTypeTableTennis": "Table tennis (ping pong)",
    "HKWorkoutActivityTypeTennis": "Tennis",
#Outdoor Activities
    "HKWorkoutActivityTypeClimbing": "Other (unclassified fitness activity)",
    "HKWorkoutActivityTypeEquestrianSports": "Horseback riding",
    "HKWorkoutActivityTypeFishing": "Other (unclassified fitness activity)",
    "HKWorkoutActivityTypeGolf": "Golf",
    "HKWorkoutActivityTypeHiking": "Hiking",
    "HKWorkoutActivityTypeHunting": "Other (unclassified fitness activity)",
    "HKWorkoutActivityTypePlay": "Team sports",
#Snow and Ice Sports
    "HKWorkoutActivityTypeCrossCountrySkiing": "Cross-country skiing",
    "HKWorkoutActivityTypeCurling": "Curling",
    "HKWorkoutActivityTypeDownhillSkiing": "Downhill skiing",
    "HKWorkoutActivityTypeSnowSports": "Other (unclassified fitness activity)",
    "HKWorkoutActivityTypeSnowboarding": "Snowboarding",
    "HKWorkoutActivityTypeSkatingSports": "Skating",
#Water Activities
    "HKWorkoutActivityTypePaddleSports": "Stand-up paddleboarding",
    "HKWorkoutActivityTypeRowing": "Rowing",
    "HKWorkoutActivityTypeSailing": "Sailing",
    "HKWorkoutActivityTypeSurfingSports": "Surfing",
    "HKWorkoutActivityTypeSwimming": "Swimming",
    "HKWorkoutActivityTypeWaterFitness": "Other (unclassified fitness activity)",
    "HKWorkoutActivityTypeWaterPolo": "Waterpolo",
    "HKWorkoutActivityTypeWaterSports": "Other (unclassified fitness activity)",
#Martial Arts
    "HKWorkoutActivityTypeBoxing": "Boxing",
    "HKWorkoutActivityTypeKickboxing": "Kickboxing",
    "HKWorkoutActivityTypeMartialArts": "Martial arts",
    "HKWorkoutActivityTypeTaiChi": "Martial arts",
    "HKWorkoutActivityTypeWrestling": "Martial arts",
#Other Activities
    "HKWorkoutActivityTypeOther": "Other (unclassified fitness activity)"
}

def getGoogleActivityBeAppleWorkout(workout):
    if workout not in listWorkoutMapping:
        return None
    activity = listWorkoutMapping[workout]
    if activity not in listActivityTypeGoogle:
        return None
    return (activity, listActivityTypeGoogle[activity])

def calculateDistance(longitude_1, latitude_1, altitude_1, longitude_2, latitude_2, altitude_2):
    x_1 = altitude_1 * cos(latitude_1) * sin(longitude_1)
    y_1 = altitude_1 * sin(latitude_1)
    z_1 = altitude_1 * cos(latitude_1) * cos(longitude_1)
    x_2 = altitude_2 * cos(latitude_2) * sin(longitude_2)
    y_2 = altitude_2 * sin(latitude_2)
    z_2 = altitude_2 * cos(latitude_2) * cos(longitude_2)
    dist = sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2 + (z_2 - z_1) ** 2)
    return dist

def getParams():
    if len(sys.argv) != 2:
        raise Exception("Parameters file not specified")
    return sys.argv[1]

def getSettings(file):
    myvars = {}
    with open(file, encoding='utf-8') as myfile:
        for line in myfile:
            name, var = line.partition("=")[::2]
            myvars[name.strip()] = var.strip()
    return myvars

def getDeviceInfo(data):
    device = {}
    res = re.search('.*, name:(.+), manufacturer:(.+), model:(.+), hardware:(.+), software:(.+)>', data)
    device = {}
    device['name'] = res.group(1)
    device['manufacturer'] = res.group(2)
    device['model'] = res.group(3)
    device['hardware'] = res.group(4)
    device['software'] = res.group(5)
    return device

def getSource(record):
    source = {}
    if 'sourceName' not in record.attrib:
        return None
    source['sourceName'] = record.attrib['sourceName']
    if 'sourceVersion' not in record.attrib:
        return None
    source['sourceVersion'] = record.attrib['sourceVersion']
    if 'device' not in record.attrib:
        return None
    source['device'] = getDeviceInfo(record.attrib['device'])
    return source

def getRecordData(record):
    data = {}
    data['sourceName'] = record.attrib['sourceName']
    data['sourceVersion'] = record.attrib['sourceVersion']
    data['unit'] = record.attrib['unit']
    data['creationDate'] = record.attrib['creationDate']
    data['startDate'] = record.attrib['startDate']
    data['endDate'] = record.attrib['endDate']
    data['value'] = record.attrib['value']
    return data

def getHeight(record):
    data = getRecordData(record)
    print('Height:', data['value'], data['unit'])
    return data

def getBodyMass(record):
    data = getRecordData(record)
    print('BodyMass:', data['value'], data['unit'])
    return data

def getHeartRate(record):
    data = getRecordData(record)
    for c in record:
        if c.tag == 'MetadataEntry' and c.attrib['key'] == 'HKMetadataKeyHeartRateMotionContext':
            if c.attrib['value'] == '0':
                data['motionContext'] = 'notSet'
            elif c.attrib['value'] == '1':
                data['motionContext'] = 'sedentary'
            elif c.attrib['value'] == '2':
                data['motionContext'] = 'active'
            else:
                data['motionContext'] = None
            break
    print('HeartRate:', data['value'], data['motionContext'])
    return data

def getStepCount(record):
    data = getRecordData(record)
    print('StepCount:', data['value'])
    return data

def getDistance(record):
    data = getRecordData(record)
    print('Distance:', data['value'], data['unit'])
    return data

def getEnergyBurned(record, energyType):
    data = getRecordData(record)
    data['type'] = energyType
    print('EnergyBurned:', data['value'], data['unit'], data['type'])
    return data

def getWorkoutData(record):
    data = {}
    data['workoutActivityType'] = record.attrib['workoutActivityType']
    data['duration'] = record.attrib['duration']
    data['durationUnit'] = record.attrib['durationUnit']
    data['totalDistance'] = record.attrib['totalDistance']
    data['totalDistanceUnit'] = record.attrib['totalDistanceUnit']
    data['totalEnergyBurned'] = record.attrib['totalEnergyBurned']
    data['totalEnergyBurnedUnit'] = record.attrib['totalEnergyBurnedUnit']
    data['sourceName'] = record.attrib['sourceName']
    data['sourceVersion'] = record.attrib['sourceVersion']
    data['device'] = getDeviceInfo(record.attrib['device'])
    data['creationDate'] = record.attrib['creationDate']
    data['startDate'] = record.attrib['startDate']
    data['endDate'] = record.attrib['endDate']
    return data

def getWorkout(record):
    data = getWorkoutData(record)
    activity, _ = getGoogleActivityBeAppleWorkout(data['workoutActivityType'])
    print("Workout:", data['workoutActivityType'], 'Activity:', activity)
    return data

def getDate(raw):
    return datetime.strptime(raw, '%Y-%m-%d %H:%M:%S %z').date()

skippedRecords = []
ignoredRecords = [
    'ExportDate',
    'Me',
    'HKQuantityTypeIdentifierFlightsClimbed',
    'HKQuantityTypeIdentifierAppleExerciseTime',
    'HKQuantityTypeIdentifierRestingHeartRate',
    'HKQuantityTypeIdentifierWalkingHeartRateAverage',
    'ActivitySummary',
    'HKQuantityTypeIdentifierHeartRateVariabilitySDNN'
]
def addSkippedRecord(record):
    if not record in skippedRecords and not record in ignoredRecords:
        skippedRecords.append(record)

def processInputData(xmlfile, lastDate = None):
    xml = et.parse(xmlfile)
    root = xml.getroot()
    records = []
    sources = []
    minDate = None
    dataHeight = None
    dataBodyMass = None
    dataHeartRate = []
    dataStepCount = []
    dataDistance = []
    dataEnergyBurned = []
    dataWorkout = []
    for record in root:
        if record.tag == 'Record':
            if record.attrib['type'] not in records:
                records.append(record.attrib['type'])
            creationDate = getDate(record.attrib['creationDate'])
            if lastDate is not None and creationDate <= lastDate:
                continue
            if minDate is not None and creationDate > minDate:
                continue
            if minDate is None or minDate > creationDate:
                minDate = creationDate
            source = getSource(record)
            if source is not None and source not in sources:
                sources.append(source)
            if record.attrib['type'] == 'HKQuantityTypeIdentifierHeartRate':
                dataHeartRate.append(getHeartRate(record))
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierStepCount':
                dataStepCount.append(getStepCount(record))
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
                dataDistance.append(getDistance(record))
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned':
                dataEnergyBurned.append(getEnergyBurned(record, 'active'))
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierBasalEnergyBurned':
                dataEnergyBurned.append(getEnergyBurned(record, 'basal'))
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierHeight':
                dataHeight = getHeight(record)
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierBodyMass':
                dataBodyMass = getBodyMass(record)
                continue
            addSkippedRecord(record.attrib['type'])
            continue
        if record.tag == 'Workout':
            creationDate = getDate(record.attrib['creationDate'])
            if lastDate is not None and creationDate <= lastDate:
                continue
            if minDate is not None and creationDate > minDate:
                continue
            dataWorkout.append(getWorkout(record))
            continue
        addSkippedRecord(record.tag)
        continue
    print('===============================================')
    for r in records:
        print(r)
    print('===============================================')
    for s in sources:
        print(s)
    print('===============================================')
    print('minDate:', minDate)
    if len(skippedRecords) > 0:
        print('===============================================')
        print('Skipped records:')
        for sr in skippedRecords:
            print(sr)
        print('===============================================')
        print("Can't proceed with data skipped")
        return

settingsFileName = getParams()
settings = getSettings(settingsFileName)
clientIdFileName = settings['ClientIdFileName']

flow = InstalledAppFlow.from_client_secrets_file(
    clientIdFileName,
    scopes=[
        'https://www.googleapis.com/auth/fitness.activity.read',
        'https://www.googleapis.com/auth/fitness.activity.write',
        'https://www.googleapis.com/auth/fitness.body.read',
        'https://www.googleapis.com/auth/fitness.body.write',
        'https://www.googleapis.com/auth/fitness.location.read',
        'https://www.googleapis.com/auth/fitness.location.write'
        ]
    )
credentials = flow.run_local_server(
    host='localhost',
    port=8080, 
    authorization_prompt_message='Please visit this URL: {url}', 
    success_message='The auth flow is complete; you may close this window.',
    open_browser=True
    )
fitness_service = build("fitness", "v1", credentials = credentials)
# available_data_sources = json.loads(fitness_service.users().dataSources().list(userId="me").execute())
available_data_sources = fitness_service.users().dataSources().list(userId="me").execute()
for ds in available_data_sources['dataSource']:
    if "device" in ds:
        print(ds['dataStreamName'], '[', ds['device']['model'], ']')
    else:
        print(ds['dataStreamName'])
# print(available_data_sources)

zip = zipfile.ZipFile(settings['ArchivePath'], 'r')
for name in zip.namelist():
    name_conv = name.encode('cp437').decode('utf-8') 
    if name_conv == settings['DataFileName']:
        xmlfile = zip.open(name)
        processInputData(xmlfile)
        xmlfile.close()
