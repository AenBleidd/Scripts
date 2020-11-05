# pip install --upgrade google-api-python-client
# pip install --upgrade oauth2client
# pip install --upgrade google-auth-oauthlib

import google.oauth2.credentials
import json
import math
import re
import sys
import xml.etree.ElementTree as et
import zipfile

from datetime import datetime, date, timedelta
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

def getGoogleActivityByAppleWorkout(workout):
    if workout not in listWorkoutMapping:
        return None
    activity = listWorkoutMapping[workout]
    if activity not in listActivityTypeGoogle:
        return None
    return (activity, listActivityTypeGoogle[activity])

def getGoogleActivityIdByAppleWorkout(workout):
    _, id = getGoogleActivityByAppleWorkout(workout)
    return id

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

def saveSettings(file, settings):
    with open(file, 'w', encoding='utf-8') as myfile:
        for key, value in settings.items():
            myfile.write(key)
            myfile.write('=')
            myfile.write(str(value))
            myfile.write('\n')

def getDeviceInfo(data):
    res = re.search('.*, name:(.+), manufacturer:(.+), model:(.+), hardware:(.+), .*>', data)
    if (res == None):
        res = re.search('.*, name:(.+), manufacturer:(.+), model:(.+), localIdentifier:(.+)>', data)
    device = {}
    if (res != None):
        device['name'] = res.group(1)
        device['manufacturer'] = res.group(2)
        device['model'] = res.group(3)
        device['hardware'] = res.group(4)
        return device
    res = re.search('.*, name:(.+), manufacturer:(.+), localIdentifier:(.+)>', data)
    device['name'] = res.group(1)
    device['manufacturer'] = res.group(2)
    device['model'] = res.group(3)
    device['hardware'] = res.group(3)
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
    if 'sourceVersion' in record.attrib:
        data['sourceVersion'] = record.attrib['sourceVersion']
    else:
        data['sourceVersion'] = '0.0.0.0'
    if 'unit' in record.attrib:
        data['unit'] = record.attrib['unit']
    else:
        data['unit'] = ''
    data['creationDate'] = record.attrib['creationDate']
    data['startDate'] = record.attrib['startDate']
    data['endDate'] = record.attrib['endDate']
    if 'value' in record.attrib:
        data['value'] = record.attrib['value']
    else:
        data['value'] = ''
    return data

def getHeight(record):
    data = getRecordData(record)
    #print('Height:', data['value'], data['unit'])
    return data

def getBodyMass(record):
    data = getRecordData(record)
    #print('BodyMass:', data['value'], data['unit'])
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
    #print('HeartRate:', data['value'], data['motionContext'])
    return data

def getStepCount(record):
    data = getRecordData(record)
    #print('StepCount:', data['value'])
    return data

def getDistance(record):
    data = getRecordData(record)
    #print('Distance:', data['value'], data['unit'])
    return data

def getEnergyBurned(record, energyType):
    data = getRecordData(record)
    data['type'] = energyType
    #print('EnergyBurned:', data['value'], data['unit'], data['type'])
    return data

def getWorkoutData(record):
    if (record.attrib['sourceName'] == 'Strava'):
        return None
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
    #activity, _ = getGoogleActivityByAppleWorkout(data['workoutActivityType'])
    #print("Workout:", data['workoutActivityType'], 'Activity:', activity)
    return data

def getSleep(record):
    data = getRecordData(record)
    #print('Sleep:', data['value'])
    return data

def getMindfullSession(record):
    data = getRecordData(record)
    #print('MindfullSesstion')
    return data

def getFlightsClimbed(record):
    data = getRecordData(record)
    #print('FlightsClimbed')
    return data

def getDateTime(raw):
    return datetime.strptime(raw, '%Y-%m-%d %H:%M:%S %z')

def getDate(raw):
    return getDateTime(raw).date()

def getMilliSeconds(raw):
    return math.floor(getDateTime(raw).timestamp() * 1000)

def getMilliSecondsStr(raw):
    return str(getMilliSeconds(raw))

def getNanoSeconds(raw):
    return getMilliSeconds(raw) * 1000000

def getNanoSecondsStr(raw):
    return str(getNanoSeconds(raw))

skippedRecords = []
ignoredRecords = [
    'Me',
    'HKQuantityTypeIdentifierAppleExerciseTime',
    'HKQuantityTypeIdentifierRestingHeartRate',
    'HKQuantityTypeIdentifierWalkingHeartRateAverage',
    'ActivitySummary',
    'HKQuantityTypeIdentifierHeartRateVariabilitySDNN',
    'HKQuantityTypeIdentifierVO2Max',
    'HKCategoryTypeIdentifierAppleStandHour',
    'HKCategoryTypeIdentifierHighHeartRateEvent',
    'HKQuantityTypeIdentifierHeadphoneAudioExposure',
    'HKQuantityTypeIdentifierAppleStandTime',
    'HKDataTypeSleepDurationGoal',
    'HKQuantityTypeIdentifierEnvironmentalAudioExposure',
    'HKCategoryTypeIdentifierHandwashingEvent'
]
def addSkippedRecord(record):
    if not record in skippedRecords and not record in ignoredRecords:
        skippedRecords.append(record)

def getDeviceTypeByName(name):
    if name.find('iPhone') > -1:
        return 'phone'
    if name.find('Apple Watch') > -1:
        return 'watch'
    return 'unknown'

def createDataSource(dataSource, fitnessService, dataStreamName, fieldName, fieldFormat, dataTypeName, typeName):
    ds = {}
    dt = {}
    field = {}
    app = {}
    device = {}
    ds['dataStreamName'] = dataStreamName
    dt['field'] = []
    field['name'] = fieldName
    field['format'] = fieldFormat
    dt['field'].append(field)
    dt['name'] = dataTypeName
    ds['dataType'] = dt
    app['name'] = 'AppleHealth2GoogleFit'
    ds['application'] = app
    device['model'] = dataSource['device']['model']
    device['version'] = dataSource['device']['hardware']
    device['type'] = getDeviceTypeByName(dataSource['device']['name'])
    device['manufacturer'] = dataSource['device']['manufacturer']
    device['uid'] = '1000001'
    ds['device'] = device
    ds['type'] = typeName
    ds = fitnessService.users().dataSources().create(userId='me', body=ds).execute()
    return ds

def getDataSourceForData(source, availableDataSources, localDataSources, createdDataSources, fitnessService, dataStreamName, fieldName, fieldFormat, dataTypeName, typeName):
    ds = None
    for lds in localDataSources:
        if lds['sourceName'] == source['sourceName']:
            ds = lds
            break
    if ds == None:
        for lds in localDataSources:
            if getDeviceTypeByName(lds['device']['name']) == 'phone':
                ds = lds
                break
    if ds == None:
        raise ValueError('No source found with the name', source['sourceName'])
    adsFound = None
    for cds in createdDataSources:
        if (
            'device' in cds
            and cds['dataType']['name'] == dataTypeName
            and cds['device']['model'] == ds['device']['model']
            and cds['device']['version'] == ds['device']['hardware']
        ):
            adsFound = cds
            break
    if adsFound != None:
        return adsFound
    for ads in availableDataSources:
        if (
            'device' in ads
            and ads['dataType']['name'] == dataTypeName
            and ads['device']['model'] == ds['device']['model']
            and ads['device']['version'] == ds['device']['hardware']
        ):
            adsFound = ads
            break
    if adsFound == None:
        adsFound = createDataSource(ds, fitnessService, dataStreamName, fieldName, fieldFormat, dataTypeName, typeName)
        createdDataSources.append(adsFound)
    return adsFound

def processData(rawData, valueType, valueTypeLong, valueData, valueName, valueNameShort, valueMode, availableDataSources, localDataSources, createdDataSources, fitnessService):
    datasets = []
    processed = 0
    for data in rawData:
        processed = processed + 1
        point = {}
        value = {}
        value[valueType] = valueData(data)
        point['modifiedTimeMillis'] = getMilliSecondsStr(data['creationDate'])
        point['startTimeNanos'] = getNanoSecondsStr(data['startDate'])
        point['dataTypeName'] = valueName
        point['endTimeNanos'] = getNanoSecondsStr(data['endDate'])
        point['value'] = []
        point['value'].append(value)
        point['rawTimestampNanos'] = getNanoSecondsStr(data['creationDate'])
        dataSource = getDataSourceForData(data, availableDataSources, localDataSources, createdDataSources, fitnessService, valueMode, valueNameShort, valueTypeLong, valueName, 'raw') 
        dataset = {}
        dataset['dataSourceId'] = dataSource['dataStreamId']
        dataset['point'] = []
        dataset['point'].append(point)
        dataset['minStartTimeNs'] = point['startTimeNanos']
        dataset['maxEndTimeNs'] = point['endTimeNanos']
        found = False
        if datasets:
            for ds in datasets:
                if ds['dataSourceId'] == dataset['dataSourceId']:
                    ds['point'].append(point)
                    if ds['minStartTimeNs'] > dataset['minStartTimeNs']:
                        ds['minStartTimeNs'] = dataset['minStartTimeNs']
                    if ds['maxEndTimeNs'] < dataset['maxEndTimeNs']:
                        ds['maxEndTimeNs'] = dataset['maxEndTimeNs']
                    found = True
                    break
        if not found:
            datasets.append(dataset)
    for ds in datasets:
        ds['point'].sort(key = lambda x: x['endTimeNanos'], reverse = True)
        id = ds['minStartTimeNs'] + '-' + ds['maxEndTimeNs']
        fitnessService.users().dataSources().datasets().patch(userId="me", dataSourceId=ds['dataSourceId'], datasetId=id, body=ds, currentTimeMillis=None).execute()
    print('Records processed:', processed)
    return

def processDataHeight(data, availableDataSources, localDataSources, createdDataSources, fitnessService):
    processData(data, 'fpVal', 'floatPoint', lambda d: float(d['value']) / 100, 'com.google.height', 'height', 'manual', availableDataSources, localDataSources, createdDataSources, fitnessService)
    return

def processDataBodyMass(data, availableDataSources, localDataSources, createdDataSources, fitnessService):
    processData(data, 'fpVal', 'floatPoint', lambda d: float(d['value']), 'com.google.weight', 'weight', 'manual', availableDataSources, localDataSources, createdDataSources, fitnessService)
    return

def processDataHeartRate(data, availableDataSources, localDataSources, createdDataSources, fitnessService):
    processData(data, 'fpVal', 'floatPoint', lambda d: d['value'], 'com.google.heart_rate.bpm', 'bpm', 'raw', availableDataSources, localDataSources, createdDataSources, fitnessService)
    return

def processDataStepCount(data, availableDataSources, localDataSources, createdDataSources, fitnessService):
    processData(data, 'intVal', 'integer', lambda d: d['value'], 'com.google.step_count.delta', 'steps', 'raw', availableDataSources, localDataSources, createdDataSources, fitnessService)
    return

def processDataDistance(data, availableDataSources, localDataSources, createdDataSources, fitnessService):
    processData(data, 'fpVal', 'floatPoint', lambda d: float(d['value']) * 1000, 'com.google.distance.delta', 'distance', 'raw', availableDataSources, localDataSources, createdDataSources, fitnessService)
    return

def processDataEnergyBurned(data, availableDataSources, localDataSources, createdDataSources, fitnessService):
    processData(data, 'fpVal', 'floatPoint', lambda d: float(d['value']), 'com.google.calories.expended', 'calories', 'raw', availableDataSources, localDataSources, createdDataSources, fitnessService)
    return

def processDataWorkout(data, availableDataSources, localDataSources, createdDataSources, fitnessService):
    processData(data, 'intVal', 'integer', lambda d: getGoogleActivityIdByAppleWorkout(d['workoutActivityType']), 'com.google.activity.segment', 'activity', 'raw', availableDataSources, localDataSources, createdDataSources, fitnessService)
    return

def processDataSleep(data, availableDataSources, localDataSources, createdDataSources, fitnessService):
    processData(data, 'intVal', 'integer', lambda d: 72, 'com.google.activity.segment', 'activity', 'raw', availableDataSources, localDataSources, createdDataSources, fitnessService)
    return

def processDataMindfullSesstion(data, availableDataSources, localDataSources, createdDataSources, fitnessService):
    processData(data, 'intVal', 'integer', lambda d: 122, 'com.google.activity.segment', 'activity', 'raw', availableDataSources, localDataSources, createdDataSources, fitnessService)
    return

def processDataFlightsClimbed(data, availableDataSources, localDataSources, createdDataSources, fitnessService):
    processData(data, 'intVal', 'integer', lambda d: 77, 'com.google.activity.segment', 'activity', 'raw', availableDataSources, localDataSources, createdDataSources, fitnessService)
    return

def processInputData(xmlfile, availableDataSources, fitnessService, skipCategories, lastDate = None):
    print('===============================================')
    print('Start Processing')
    if lastDate is not None and lastDate != 'None':
        lastDate = datetime.strptime(str(lastDate), '%Y-%m-%d').date()
    xml = et.parse(xmlfile)
    root = xml.getroot()
    sources = []
    minDate = None
    dataHeight = []
    dataBodyMass = []
    dataHeartRate = []
    dataStepCount = []
    dataDistance = []
    dataEnergyBurned = []
    dataWorkout = []
    dataSleep = []
    dataMindfullSession = []
    dataFlightsClimbed = []
    exportDate = None
    for record in root:
        if record.tag == 'Record':
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
                if ('HeartRate' not in skipCategories):
                    dataHeartRate.append(getHeartRate(record))
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierStepCount':
                if ('StepCount' not in skipCategories):
                    dataStepCount.append(getStepCount(record))
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
                if ('Distance' not in skipCategories):
                    dataDistance.append(getDistance(record))
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierActiveEnergyBurned':
                if ('EnergyBurned' not in skipCategories):
                    dataEnergyBurned.append(getEnergyBurned(record, 'active'))
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierBasalEnergyBurned':
                if ('EnergyBurned' not in skipCategories):
                    dataEnergyBurned.append(getEnergyBurned(record, 'basal'))
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierHeight':
                if ('Height' not in skipCategories):
                    dataHeight.append(getHeight(record))
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierBodyMass':
                if ('BodyMass' not in skipCategories):
                    dataBodyMass.append(getBodyMass(record))
                continue
            if record.attrib['type'] == 'HKCategoryTypeIdentifierSleepAnalysis':
                if ('Sleep' in skipCategories):
                    continue
                if record.attrib['value'] == 'HKCategoryValueSleepAnalysisInBed':
                    dataSleep.append(getSleep(record))
                else:
                    addSkippedRecord(record.attrib['value'])        
                continue
            if record.attrib['type'] == 'HKCategoryTypeIdentifierMindfulSession':
                if ('MindfullSession' not in skipCategories):
                    dataMindfullSession.append(getMindfullSession(record))
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierFlightsClimbed':
                if ('FlightsClimbed' not in skipCategories):
                    dataFlightsClimbed.append(getFlightsClimbed(record))
                continue
            if record.attrib['type'] == 'HKQuantityTypeIdentifierDistanceCycling' and 'HKQuantityTypeIdentifierDistanceCycling' in skipCategories:
                continue
            addSkippedRecord(record.attrib['type'])
            continue
        if record.tag == 'Workout':
            if ('Workout' in skipCategories):
                continue
            creationDate = getDate(record.attrib['creationDate'])
            if lastDate is not None and creationDate <= lastDate:
                continue
            if minDate is not None and creationDate > minDate:
                continue
            workoutRecord = getWorkout(record)
            if (workoutRecord != None):
                dataWorkout.append(workoutRecord)
            continue
        if record.tag == 'ExportDate':
            exportDate = getDate(record.attrib['value'])
            continue
        addSkippedRecord(record.tag)
        continue
    print('minDate:', minDate)
    yesterday = date.today() - timedelta(1)
    if minDate is None:
        return lastDate
    if minDate > yesterday:
        return lastDate
    if minDate >= exportDate:
        return lastDate
    if len(skippedRecords) > 0:
        print('===============================================')
        print('Skipped records:')
        for sr in skippedRecords:
            print(sr)
        print('===============================================')
        print("Can't proceed with data skipped")
        return lastDate
    createdDataSources = []
    if ('Height' not in skipCategories):
        print('===============================================')
        print('Processing Height data')
        processDataHeight(dataHeight, availableDataSources, sources, createdDataSources, fitnessService)
    if ('BodyMass' not in skipCategories):
        print('===============================================')
        print('Processing BodyMass data')
        processDataBodyMass(dataBodyMass, availableDataSources, sources, createdDataSources, fitnessService)
    if ('HeartRate' not in skipCategories):
        print('===============================================')
        print('Processing HeartRate data')
        processDataHeartRate(dataHeartRate, availableDataSources, sources, createdDataSources, fitnessService)
    if ('StepCount' not in skipCategories):
        print('===============================================')
        print('Processing StepCount data')
        processDataStepCount(dataStepCount, availableDataSources, sources, createdDataSources, fitnessService)
    if ('Distance' not in skipCategories):
        print('===============================================')
        print('Processing Distance data')
        processDataDistance(dataDistance, availableDataSources, sources, createdDataSources, fitnessService)
    if ('EnergyBurned' not in skipCategories):
        print('===============================================')
        print('Processing EnergyBurned data')
        processDataEnergyBurned(dataEnergyBurned, availableDataSources, sources, createdDataSources, fitnessService)
    if ('Workout' not in skipCategories):
        print('===============================================')
        print('Processing Workout data')
        processDataWorkout(dataWorkout, availableDataSources, sources, createdDataSources, fitnessService)
    if ('Sleep' not in skipCategories):
        print('===============================================')
        print('Processing Sleep data')
        processDataSleep(dataSleep, availableDataSources, sources, createdDataSources, fitnessService)
    if ('MindfullSession' not in skipCategories):
        print('===============================================')
        print('Processing MindfullSession data')
        processDataMindfullSesstion(dataMindfullSession, availableDataSources, sources, createdDataSources, fitnessService)
    if ('FlightsClimbed' not in skipCategories):
        print('===============================================')
        print('Processing FlightsClimbed data')
        processDataFlightsClimbed(dataFlightsClimbed, availableDataSources, sources, createdDataSources, fitnessService)
    print('===============================================')
    print('Processing done')
    return minDate

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
        'https://www.googleapis.com/auth/fitness.location.write',
        'https://www.googleapis.com/auth/fitness.sleep.read',
        'https://www.googleapis.com/auth/fitness.sleep.write'
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

zip = zipfile.ZipFile(settings['ArchivePath'], 'r')
skipCategories = settings['SkipCategories'].split(';')
lastDate = None
if 'LastDate' in settings:
    lastDate = settings['LastDate']
for name in zip.namelist():
    name_conv = name.encode('cp437').decode('utf-8') 
    if name_conv == settings['DataFileName']:
        while True:
            available_data_sources = fitness_service.users().dataSources().list(userId="me").execute()
            xmlfile = zip.open(name)
            lastDateNew = processInputData(xmlfile, available_data_sources['dataSource'], fitness_service, skipCategories, lastDate)
            xmlfile.close()
            settings['LastDate'] = lastDateNew
            saveSettings(settingsFileName, settings)
            if lastDateNew == lastDate:
                break
            lastDate = lastDateNew
