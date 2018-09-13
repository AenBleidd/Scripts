import datetime
import os
import sys
import subprocess

from winreg import *

CURRENT_POWERPLAN_PATH = "SYSTEM\\CurrentControlSet\\Control\\Power\\User\\Default\\PowerSchemes"
ALL_POWERPLANS_PATH = "SYSTEM\\CurrentControlSet\\Control\\Power\\User\\PowerSchemes\\"
MAX_CPULOAD_PATH_VAL1 = "54533251-82be-4824-96c1-47b60b740d00"
MAX_CPULOAD_PATH_VAL2 = "bc5038f7-23e0-4960-96da-33abaf5935ec"

log = open(os.path.abspath(__file__)+'.log', 'a+')

def getValue():
    if len(sys.argv) == 2:
        try:
            return int(sys.argv[1])
        except BaseException:
            return 0
    else:
        return 0

def getCurrentPowerPlan():
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE, CURRENT_POWERPLAN_PATH)
        val = QueryValueEx(key, "ActivePowerScheme")
        CloseKey(key)
        return val[0]
    except BaseException:
        return ""

def runProcess(command):
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	output, err = process.communicate()
	retcode = process.returncode
	return (retcode, output, err)

def changeLoad(value):
    try:
        activePowerPlan = getCurrentPowerPlan()
        if activePowerPlan == "":
            return
        keyPath = ALL_POWERPLANS_PATH + activePowerPlan + "\\" + MAX_CPULOAD_PATH_VAL1 + "\\" + MAX_CPULOAD_PATH_VAL2
        key = OpenKey(HKEY_LOCAL_MACHINE, keyPath)
        acValue = QueryValueEx(key, "ACSettingIndex")[0] + value
        dcValue = QueryValueEx(key, "DCSettingIndex")[0] + value
        CloseKey(key)

        bChanged = False
        if acValue > 0 and acValue <= 100:
            runProcess(["powercfg", "/SETACVALUEINDEX", activePowerPlan, MAX_CPULOAD_PATH_VAL1, MAX_CPULOAD_PATH_VAL2, str(acValue)])
            bChanged = True
            log.write(str(datetime.datetime.now()) + ': Ac value changed to ' + str(acValue))
        if dcValue > 0 and dcValue <= 100:
            runProcess(["powercfg", "/SETDCVALUEINDEX", activePowerPlan, MAX_CPULOAD_PATH_VAL1, MAX_CPULOAD_PATH_VAL2, str(dcValue)])
            bChanged = True
            log.write(str(datetime.datetime.now()) + ': Dc value changed to ' + str(dcValue))
        if bChanged:
            runProcess(["powercfg", "/S", activePowerPlan])
    except WindowsError as e:
        log.write(str(datetime.datetime.now()) + ': ' + e.strerror)
        return
    return

def main():
    changeLoad(getValue())
    return

main()

log.close()
