# -*- coding: utf-8 -*-

import ctypes
import os
import struct
import sys

CallerIDFuncType = ctypes.CFUNCTYPE(None, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p)
SignalFuncType = ctypes.CFUNCTYPE(None, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)

@CallerIDFuncType
def CallerIDEvent(DeviceSerial, Line, PhoneNumber, DateTime, Other):
    CallerIDEvent.counter += 1
    print("CallerID: {}   DateTime: {}   Line: {}   Counter: {}".format(
        PhoneNumber, DateTime, Line, CallerIDEvent.counter))
    sys.stdout.flush()

CallerIDEvent.counter = 0

@SignalFuncType
def SignalEvent(DeviceModel, DeviceSerial, Signal1, Signal2, Signal3, Signal4):
   
    if DeviceModel and DeviceModel != "" and DeviceSerial and DeviceSerial != "":
        if not SignalEvent.connected:
            print(" Device connected:   {} - {}".format(DeviceModel, DeviceSerial))
            print(" Ready for test call\n")
            sys.stdout.flush()
        SignalEvent.connected = True
    else:
        if SignalEvent.connected:
            print(" Device disconnected")
            sys.stdout.flush()
        SignalEvent.connected = False

SignalEvent.connected = False

SetEventsFuncType = ctypes.CFUNCTYPE(None, CallerIDFuncType, SignalFuncType)

def check_soft_test_file():
    """python.exe'nin bulunduğu klasörde softTest.txt dosyasını kontrol et"""
    python_exe_dir = os.path.dirname(sys.executable)
    soft_test_path = os.path.join(python_exe_dir, "softTest.txt")
        
    
    if os.path.exists(soft_test_path):        
        print("\n Python.exe path: {}".format(sys.executable))
        print(" Found: {}".format(soft_test_path))
        print(" Test calls will be generated periodically.")
        print(" Physical calls are also detected.\n")
        return True
    else:
        """softTest.txt not found. Device and phone line needed. """
		         
        return False

 

def main():
    print("\n***************** CIDSHOW Test *****************\n")
    sys.stdout.flush()
   
 
    if struct.calcsize("P") * 8 == 64:
        dll_path = os.path.join(os.getcwd(), "./cidshow_x64/cid.dll")
    else:
        dll_path = os.path.join(os.getcwd(), "./cidshow_x86/cid.dll")
    
    print("\n Trying to load DLL from: {}".format(dll_path))    
    sys.stdout.flush()

    try:
        cid_dll = ctypes.CDLL(dll_path)
        print(" DLL loaded successfully!")
        sys.stdout.flush()
    
    except OSError as e:
        print("\nDLL error: {}".format(e))
        print("Current directory: {}".format(os.getcwd()))
        print("\nPress Enter to exit...")
        input()
        return

    try:
        SetEvents = getattr(cid_dll, "SetEvents")
        SetEvents.argtypes = [CallerIDFuncType, SignalFuncType]
        SetEvents.restype = None        
        sys.stdout.flush()
    except AttributeError:
        print("\nSetEvents function not found in DLL!")
        print("\nPress Enter to exit...")
        input()
        return

    try:
        SetEvents(CallerIDEvent, SignalEvent)
        print(" Events set successfully!\n")
        sys.stdout.flush()
    except Exception as e:
        print("Error setting events: {}".format(e))
        sys.stdout.flush()
    
    
    initial_connection = SignalEvent.connected
    if not initial_connection:        
        print(" Waiting for device to be connected...\n")
        sys.stdout.flush()
        check_soft_test_file()


    sys.stdout.flush()

    try:
        raw_input() if sys.version_info[0] == 2 else input()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

if __name__ == "__main__":
    main()