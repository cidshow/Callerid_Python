

#   https://github.com/OrhanYigitDurmaz/CallerID-Python

import ctypes
import os
import struct

CallerIDFuncType = ctypes.CFUNCTYPE(None, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p)
SignalFuncType = ctypes.CFUNCTYPE(None, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)

@CallerIDFuncType
def CallerIDEvent(DeviceSerial, Line, PhoneNumber, DateTime, Other):
    CallerIDEvent.counter += 1
    print(f"CallerID: {PhoneNumber}   DateTime: {DateTime}   Line: {Line}   Counter: {CallerIDEvent.counter}")

CallerIDEvent.counter = 0 # arama counter'ını sıfırla

@SignalFuncType
def SignalEvent(DeviceModel, DeviceSerial, Signal1, Signal2, Signal3, Signal4):
    if DeviceModel == "" or DeviceModel is None:
        if SignalEvent.connected:
            print("Device disconnected")
        SignalEvent.connected = False
    else:
        if not SignalEvent.connected:
            print(f"Device Connected:  Model: {DeviceModel}  Serial: {DeviceSerial}")
        SignalEvent.connected = True

SignalEvent.connected = False

SetEventsFuncType = ctypes.CFUNCTYPE(None, CallerIDFuncType, SignalFuncType)

def main():
    print("\n\n***************** CIDSHOW Caller ID *****************\n\n\n")


    if struct.calcsize("P") * 8 == 64:
        dll_path = os.path.join(os.getcwd(), "./cidshow_x64/cid.dll")
    else:
        dll_path = os.path.join(os.getcwd(), "./cidshow_x86/cid.dll")

    try:
        cid_dll = ctypes.CDLL(dll_path)
    except OSError as e:
        print("\n\n    DLL error")
        print("\n\n    Press any key to exit...")
        input()
        return

    # Get the SetEvents function from the DLL
    try:
        SetEvents = SetEventsFuncType(("SetEvents", cid_dll))
    except AttributeError:
        print("\n\n    DLL error")
        print("\n\n    Press any key to exit...")
        input()
        return

    # Set the events
    SetEvents(CallerIDEvent, SignalEvent)

 
    print("Ready for test call..\n")

    # Wait for a key press
    input()

if __name__ == "__main__":
    main()