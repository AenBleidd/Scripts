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
    res = re.search('.*, name:(.+), manufacturer:(.+), model:(.+), hardware:(.+), software:(.+)>', record.attrib['device'])
    source['device'] = {}
    source['device']['name'] = res.group(1)
    source['device']['manufacturer'] = res.group(2)
    source['device']['model'] = res.group(3)
    source['device']['hardware'] = res.group(4)
    source['device']['software'] = res.group(5)
    return source

def processInputData(xmlfile):
    xml = et.parse(xmlfile)
    root = xml.getroot()
    print(root)
    records = []
    sources = []
    for record in root:
        if record.tag == 'Record':
            if record.attrib['type'] not in records:
                records.append(record.attrib['type'])
            # creationDate = datetime.strptime(record.attrib['creationDate'], '%Y-%m-%d %H:%M:%S %z')
            source = getSource(record)
            if source is not None and source not in sources:
                sources.append(source)
            # if record.attrib['type'] == 'HKQuantityTypeIdentifierHeartRate':
            #     print(record.tag, record.attrib)
            # if record.attrib['type'] == 'HKQuantityTypeIdentifierStepCount':
            #     print(record.tag, record.attrib)
            #     break
    print('===============================================')
    for r in records:
        print(r)
    print('===============================================')
    for s in sources:
        print(s)

settingsFileName = getParams()
settings = getSettings(settingsFileName)
clientIdFileName = settings['ClientIdFileName']

flow = InstalledAppFlow.from_client_secrets_file(
    clientIdFileName,
    scopes=[
        'https://www.googleapis.com/auth/fitness.activity.read',
        'https://www.googleapis.com/auth/fitness.activity.write'
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
