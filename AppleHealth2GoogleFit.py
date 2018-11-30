# pip install --upgrade google-api-python-client
# pip install --upgrade oauth2client

import google.oauth2.credentials
import xml.etree.ElementTree as et
import sys
import zipfile

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

def processInputData(xmlfile):
    xml = et.parse(xmlfile)
    root = xml.getroot()
    print(root)
    records = []
    for record in root:
        if record.tag == 'Record':
            if record.attrib['type'] not in records:
                records.append(record.attrib['type'])
            # if record.attrib['type'] == 'HKQuantityTypeIdentifierHeartRate':
            #     print(record.tag, record.attrib)
            # elif record.attrib['type'] == 'HKQuantityTypeIdentifierStepCount':
            #     print(record.tag, record.attrib)
    print('===============================================')
    for r in records:
        print(r)


# settingsFileName = getParams()
settingsFileName = "AppleHealth2GoogleFit.settings"
clientIdFileName = "AppleHealth2GoogleFil.client_id.json"
settings = getSettings(settingsFileName)

zip = zipfile.ZipFile(settings['ArchivePath'], 'r')
for name in zip.namelist():
    name_conv = name.encode('cp437').decode('utf-8') 
    if name_conv == settings['DataFileName']:
        xmlfile = zip.open(name)
        processInputData(xmlfile)
        xmlfile.close()
