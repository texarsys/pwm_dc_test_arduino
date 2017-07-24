# Copyright (C) Texar Systems Private Limited, India - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

# Notes on Usage:
# 1. This device file is meant for the Keysight Oscilloscope EDUX1002A. It may work for other oscilloscopes
#     as well, but you need to double check with the programmers manual of the oscilloscope to confirm the SCPI commands
#
# 2. In case you are modifying the device file, use Python 2.x and install the python package pyVISA.
#
# 3. Install the Visa driver (E.g., Keysight Visa or NI Visa) before using the device file.
#
# 4. How to get the device configuration "Instument ID"?
#     Connect the oscilloscope via USB and run the following set of commands in the python 2.x shell
#
#       import visa
#       rm = visa.ResourceManager("C:\Windows\System32\\agvisa32.dll") #the user may need to provide visa dll name including the path.
#       rm.list_resources()
#
#     The last command displays the instrument id of the oscilloscope. You can also query the identification of the
#     instrument using this instrument id. Refer the statements below.
#
#       inst = rm.open_resource('USB0::10893::6027::cn56520244::0::INSTR')  # the input argument is the instrument id.
#       inst.query("*IDN?")
#
#  For queries on the topic, reach us at support@texarsys.com

import wx
import visa

# As the argument of visa.ResourceManager(), the user need to provide visa dll name including the path. In this device file,
# we are providing the keysight visa dll (agvisa32.dll). In case no input dll is provided, the default visa dll is used.
rm = visa.ResourceManager("C:\Windows\System32\\agvisa32.dll")

class OsciKeysight():
    def __init__(self):
        """
        The constructor of the class
        """
        self.previous_val = 0 #initialise previous duty cycle value

    def setDeviceConfig(self, device_config_dict):
        """
        This action is called by EZPy when
        1. the device is created
        2. the device config is updated (to be implemented)
        """
        instrument_id = str(device_config_dict["Instrument ID"])
        try:
            self.inst = rm.open_resource(instrument_id)
        except:
            dlg = wx.MessageDialog(None,'Instrument,'+instrument_id + 'not connected','Info', wx.OK)
            dlg.ShowModal()
            raise

        self.inst.timeout = 15000               # timeout set to 15 seconds
        self.inst.clear()
        self.inst.write("*CLS")
        self.inst.write(":TIMebase:MODE ROLL")  # set the oscilloscope to roll mode to minimise the dutycycle query time

    def startOfTestcase(self):
        """
        This action is called at the start of the testcase. The device config parameters to be extracted here for later use.
        """
        pass  # nothing to do here. Hence pass statement is called.

    def endOfTestcase(self):
        """
        This action is called at the end of the testcase
        """
        pass  # nothing to do here. Hence pass statement is called.

    def getDc(self, input_dict):
        """
        This action is called from the scheduler window of the testcase.
        """
        output_dict = {}

        dc_ch1 = self.inst.query(":MEASure:DUTycycle? CHANNEL1")

        #if the oscilloscope reports a dc value higher than 100, discard it and instead use the previous value
        if float(eval(dc_ch1)) > 100 :
            output_dict["DC Osci"] = self.previous_val
        else:
            output_dict["DC Osci"] = str(eval(dc_ch1))
            self.previous_val = str(eval(dc_ch1))
        return output_dict

    @classmethod
    def getDeviceDict(self):
        """
        This method defines the parameters for
        1. the device config window
        2. all the action config windows
        """
        tmp_device_dict = {}                 # initialise the device dictionary to an empty dictionary
        tmp_device_dict["Version"] = "1.0"   # version of the device file.

        # ******************** Device config window definition **********************************************************
        # This part of the code defines the "Device Config Window". The users need to modify only the first statement
        # below to include any configuration needed for the device. This first statement can also be an empty dictionary
        # in case no configuration is needed for the device
        tmp_device_config_dict = {"Instrument ID": " "}               # instrument id configuration
        tmp_device_dict["DeviceConfig"] = tmp_device_config_dict      # do not modify this statement.
        # ***************************************************************************************************************


        # ******************** Action config window definitions *********************************************************
        tmp_device_dict["Actions"] = {}                              # do not modify.

        # Add action configuration
        tmp_action_name = "getDc"
        tmp_action_inp_dict = { }
        tmp_action_out_dict = {"DC Osci"   : ""}                     # Configuration for Duty cycle from the Oscilloscope.
        tmp_device_dict["Actions"][tmp_action_name] = [tmp_action_inp_dict, tmp_action_out_dict]  # do not modify
        # ***************************************************************************************************************

        return tmp_device_dict
