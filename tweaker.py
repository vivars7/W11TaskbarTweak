import platform
import sys
import screeninfo
import time
from subprocess import call
from enum import Enum
from winreg import *

class POSITION(Enum):
    TOP = 1
    BOTTOM = 2
    RIGHT = 4
    LEFT = 3
    
'''
Taskbar position's binary value.
'''
def getPositionBinary(POSITION):
    position = {POSITION.TOP : b'\x01', POSITION.BOTTOM : b'\x03', POSITION.LEFT : b'\x00', POSITION.RIGHT : b'\x02'}.get(POSITION, "Unknown Position Err")
    return position

'''
Set taskbar position for a main monitor.
'''
def setPositionMainMonitor(POSITION):
    key = OpenKey(HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3", 0, KEY_ALL_ACCESS)
    (value_data, value_type) = QueryValueEx(key, "Settings")
    modify_value_data = value_data[:12] + getPositionBinary(POSITION) + value_data[13:]
    SetValueEx(key, "Settings", None, value_type, modify_value_data)

'''
Set taskbar position for sub monitors.
'''
def setPositionSubMonitors(POSITION):
    key = OpenKey(HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\MMStuckRects3", 0, KEY_ALL_ACCESS)
    for i in range(0, QueryInfoKey(key)[1]):
        (value_name, value_data, value_type) = EnumValue(key, i)
        modify_value_data = value_data[:12] + getPositionBinary(POSITION) + value_data[13:]
        SetValueEx(key, value_name, None, value_type, modify_value_data)

'''
Detect OS version
'''
def detectWindows11():
    info = sys.getwindowsversion()
    if info.major >= 10:
        if info.build >= 22000:
            return True
    return False

'''
Detect OS
'''
def isWindows():
    os_type = platform.system()
    return os_type == 'Windows'

'''
Restart "Windows Explorer" after change position.
'''
def restartExplorer():
    call('taskkill /IM explorer.exe /F', shell=True)
    time.sleep(2)
    call(["start", "explorer.exe"],shell=True)

'''
Count the number of monitors
'''
def countMonitors():
    return len(screeninfo.get_monitors())

'''
Run!!
'''
def run(POSITION):
    '''
    detect os & os version - w11 only.
    '''
    if isWindows() == False:
        return
    if detectWindows11() == False:
        return

    setPositionMainMonitor(POSITION)
    '''
    check the number of monitors.
    '''
    if countMonitors() > 1:
        setPositionSubMonitors(POSITION)

    '''
    restart windows explorer.
    '''
    restartExplorer()