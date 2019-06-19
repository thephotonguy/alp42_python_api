import ctypes
from sys import exit
import numpy as np
import time

ALP_ERRORS = {1001: 'The specified ALP device has not been found or is not ready.',
                      1002: 'The ALP device is not in idle state.',
                      1003: 'The specified ALP device identifier is not valid.',
                      1004: 'The specified ALP device is already allocated.',
                      1005: 'One of the parameters is invalid.',
                      1006: 'Error accessing user data.',
                      1007: 'The requested memory is not available (full?).',
                      1008: 'The sequence specified is currently in use.',
                      1009: 'The ALP device has been stopped while image data transfer was active.',
                      1010: 'Initialization error.',
                      1011: 'Communication error.',
                      1012: 'The specified ALP has been removed.',
                      1013: 'The onboard FPGA is unconfigured.',
                      1014: 'The function is not supported by this version of the driver file VlxUsbLd.sys.',
                      1018: 'Waking up the DMD from PWR_FLOAT did not work (ALP_DMD_POWER_FLOAT)',
                      1019: 'Support in ALP drivers missing. Update drivers and power-cycle device.',
                      1020: 'SDRAM Initialization failed.'}

class alp42():
    def __init__(self, libpath):
        self.alplib = ctypes.cdll.LoadLibrary(libpath)  # Loads the dll
        print("Library loaded")

        #Class paramenters:
        self.DeviceId = ctypes.c_long(0)
        self.SequenceId = ctypes.c_long(0)


    def errorCheck(self, returnValue, errorString = ' ', warning = False):
        if not(returnValue==0):
            errormsg = errorString + '\n' + ALP_ERRORS[returnValue]
            if warning:
                raise Exception(errormsg)
            else:
                print(errormsg)

    def devAlloc(self):
        DeviceNum = ctypes.c_long(0)
        InitFlag = ctypes.c_long(1)
        returnValue = self.alplib.AlpDevAlloc(DeviceNum, InitFlag, ctypes.byref(self.DeviceId))
        self.errorCheck(returnValue)
        print(self.DeviceId)

    def devInquire(self, InquireType):
        InquireType = ctypes.c_long(InquireType)
        retInquire = ctypes.c_long(0)
        returnValue = self.alplib.AlpDevInquire(self.DeviceId, InquireType, ctypes.byref(retInquire))
        self.errorCheck(returnValue)
        return retInquire

    def devControl(self, ControlType, ControlValue):
        ControlType = ctypes.c_long(ControlType)
        ControlValue = ctypes.c_long(ControlValue)
        returnValue = self.alplib.AlpDevControl(self.DeviceId, ControlType, ControlValue)
        self.errorCheck(returnValue)

    def devHalt(self):
        returnValue = self.alplib.AlpDevHalt(self.DeviceId)
        self.errorCheck(returnValue)

    def devFree(self):
        returnValue = self.alplib.AlpDevFree(self.DeviceId)
        self.errorCheck(returnValue)

    def seqAlloc(self, Bitplanes, PicNum):
        Bitplanes = ctypes.c_long(Bitplanes)
        PicNum = ctypes.c_long(PicNum)
        returnValue = self.alplib.AlpSeqAlloc(self.DeviceId, Bitplanes, PicNum, ctypes.byref(self.SequenceId))
        self.errorCheck(returnValue)

    def seqControl(self, ControlType, ControlValue):
        ControlType = ctypes.c_long(ControlType)
        ControlValue = ctypes.c_long(ControlValue)
        returnValue = self.alplib.AlpSeqControl(self.DeviceId, self.SequenceId, ControlType, ControlValue)
        self.errorCheck(returnValue)

    def seqTiming(self, IlluminateTime, PictureTime, SynchDelay, SynchPulseWidth, TriggerInDelay):
        IlluminateTime = ctypes.c_long(IlluminateTime)
        PictureTime = ctypes.c_long(PictureTime)
        SynchDelay = ctypes.c_long(SynchDelay)
        SynchPulseWidth = ctypes.c_long(SynchPulseWidth)
        TriggerInDelay = ctypes.c_long(TriggerInDelay)
        returnValue = self.alplib.AlpSeqTiming(self.DeviceId, self.SequenceId, IlluminateTime, PictureTime, SynchDelay, SynchPulseWidth, TriggerInDelay)
        self.errorCheck(returnValue)

    def seqPut(self, PicOffset, PicLoad, img):
        PicOffset = ctypes.c_long(PicOffset)
        PicLoad = ctypes.c_long(PicLoad)
        imgSeq = np.ravel(img)
        imgSeq = (ctypes.c_ubyte*len(imgSeq))(*imgSeq)
        returnValue = self.alplib.AlpSeqPut(self.DeviceId, self.SequenceId, PicOffset, PicLoad, imgSeq)
        self.errorCheck(returnValue)

    def seqFree(self):
        returnValue = self.alplib.AlpSeqFree(self.DeviceId, self.SequenceId)
        self.errorCheck(returnValue)

    def projControl(self, ControlType, ControlValue):
        ControlType = ctypes.c_long(ControlType)
        ControlValue = ctypes.c_long(ControlValue)
        returnValue = self.alplib.AlpProjControl(self.DeviceId, ControlType, ControlValue)
        self.errorCheck(returnValue)

    def projStart(self):
        returnValue = self.alplib.AlpProjStart(self.DeviceId, self.SequenceId)
        self.errorCheck(returnValue)

    def projStartCont(self):
        returnValue = self.alplib.AlpProjStartCont(self.DeviceId, self.SequenceId)
        self.errorCheck(returnValue)

    def projHalt(self):
        returnValue = self.alplib.AlpProjHalt(self.DeviceId)
        self.errorCheck(returnValue)

    def projWait(self):
        returnValue = self.alplib.AlpProjWait(self.DeviceId)
        self.errorCheck(returnValue)







DMD = alp42(libpath='C:\\Users\\anchi\\Desktop\\ALPV42_Python\\alpV42.dll')
DMD.devAlloc()
