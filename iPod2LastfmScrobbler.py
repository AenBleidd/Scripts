import datetime
import os
import pylast
import sqlite3
import sys

def showHelp():
    print("Usage:\n iPod2LastfmScrobbler.py settings.txt backup.db iPodFolder")

def getParams():
    if len(sys.argv) == 4:
        return sys.argv[1], sys.argv[2], sys.argv[3]

def getSettings(file):
    myvars = {}
    with open(file) as myfile:
        for line in myfile:
            name, var = line.partition("=")[::2]
            myvars[name.strip()] = var.strip()
    return myvars

def closeDatabace(connection):
    connection.close()

def verifyTableExists(connection, table):
    cur = connection.cursor()
    cur.execute("""
        select 
          count(*) 
        from 
          sqlite_master 
        where 
          type='table' 
          and name=:table_name;
        """,
        {"table_name": table}
        )
    table_exists = cur.fetchall()
    if table_exists[0][0] == 1:
        return True
    
    return False

def getDataFromBackupDatabase(connection):
    cur = connection.cursor()
    if verifyTableExists(connection, "stats") == False:
        cur.execute("""
            create table stats 
             (item_pid INTEGER NOT NULL, 
             date_played INTEGER DEFAULT 0, 
             play_count_user INTEGER DEFAULT 0, 
             PRIMARY KEY (item_pid));
             """)
        connection.commit()
        print("Table 'stats' created")
    cur.execute("select * from stats;")
    return cur.fetchall()

def getLibraryData(dbName):
    conn = sqlite3.connect(dbName)
    cur = conn.cursor()
    if verifyTableExists(conn, "item") == False:
        print("Cannot retrieve data from " + dbName + " from the table 'stats'")
        return
    cur.execute("""
        select
          pid
        , artist
        , album
        , title
        from
          item
        where
          is_song = 1;
        """)
    data = cur.fetchall()
    conn.close()

    return data

def getDynamicData(dbName):
    conn = sqlite3.connect(dbName)
    cur = conn.cursor()
    if verifyTableExists(conn, "item_stats") == False:
        print("Cannot retrieve data from " + dbName + " from the table 'item_stats'")
        return
    cur.execute("""
        select
          item_pid
        , date_played
        , play_count_user
        from
          item_stats
        where
          has_been_played = 1;
    """)
    data = cur.fetchall()
    conn.close()

    return data

def getItemFromLibraryData(data, pid):
    for item in data:
        if item[0] == pid:
            return item
    return None

def getItemFromBackupDatabase(data, pid):
    for item in data:
        if item[0] == pid:
            return item
    return None

def appleToUnixTimestampConverter(value):
    return value + 978307200

def writeDataToBackupDatabase(connection, pid, date, count):
    cur = connection.cursor()
    cur.execute("""
        select 
            count(*)
        from
            stats
        where
            item_pid = :pid
        
    """,
    {"pid": pid}
    )

    res = cur.fetchall()

    if res[0][0] == 0:
        cur.execute("""
            insert into stats
            select :pid, :date, :count;
        """,
        {
            "pid" : pid,
            "date" : date,
            "count" : count
        }
        )
    else:
        cur.execute("""
            update stats
            set
                date_played = :date
            ,   play_count_user = :count
            where
                item_pid = :pid;
        """,
        {
            "pid" : pid,
            "date" : date,
            "count" : count
        }
        )
    connection.commit()

def start():
    try:
        settingsName, backupName, iPodFolder = getParams()
    except BaseException:
        print("Missed parameters\n")
        showHelp()
        return

    settings = getSettings(settingsName)

    lastfm_network = pylast.LastFMNetwork(api_key=settings["Key"], api_secret=settings["Secret"], username=settings["User"], password_hash=pylast.md5(settings["Password"]))

    backupDB = sqlite3.connect(backupName)
    backupData = getDataFromBackupDatabase(backupDB)

    libraryName = iPodFolder + "\\iTunes\\iTunes Library.itlp\\Library.itdb"
    dynamicName = iPodFolder + "\\iTunes\\iTunes Library.itlp\\Dynamic.itdb"

    if os.path.isfile(libraryName) != True:
        print("Library.itdb file was not found")
        return

    if os.path.isfile(dynamicName) != True:
        print("Dynamic.itdb file was not found")
        return

    libraryData = getLibraryData(libraryName)
    dynamicData = getDynamicData(dynamicName)

    for item in dynamicData:
        libraryItem = getItemFromLibraryData(libraryData, item[0])
        backupItem = getItemFromBackupDatabase(backupData, item[0])
        prevCount = 0
        if backupItem != None:
            prevCount = backupItem[2]
            item = (item[0], item[1], item[2] - prevCount)
        if item[2] <= 0:
            continue
        value = (libraryItem[0], libraryItem[1], libraryItem[2], libraryItem[3], appleToUnixTimestampConverter(item[1]), item[2])
        i = 0
        while i < value[5]:
            lastfm_network.scrobble(artist=value[1], album=value[2], title=value[3], timestamp=value[4])
            print(value)
            i = i + 1
        writeDataToBackupDatabase(backupDB, value[0], value[4], value[5] + prevCount)

    backupDB.close()

start()