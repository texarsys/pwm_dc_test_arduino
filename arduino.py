# Copyright (C) Texar Systems Private Limited, India - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

# Notes on Usage:
# 1. This device file is meant for communication with the arduino via USB.
#
# 2. The device configuration "Port" can be obtained from the Device manager. E.g, it can be COM2, COM3 etc
#
# 3. The software in the arduino needs to be programmed such a way that it understands the commands from this
#    device file. The arduino software needs to decode and interpret the data accordingly. However, this is
#    only a convention that we followed and the users are free to modify based on their need.
#    As coded below,
#        - the period data sent from the PC starts with alphabet 'p'
#        - the dutycycle data  sent from the PC starts with the alphabet 'd'
#        - the analog voltage reading request starts with the alphabet 'a'

# For queries on the topic, reach us at support@texarsys.com

import serial
import string
import time
import wx

class arduino():
    def __init__(self):
        """
        The constructor of the class
        """

    def setDeviceConfig(self, device_config_dict):
        """
        This action is called by EZPy when 
        1. the device is created
        2. the device config is updated
        """
        port = str(device_config_dict["Port"])
        try:
            self.serial_obj = serial.Serial(port, 9600, timeout=0.1) #baudrate = 9600
        except:
            dlg = wx.MessageDialog(None, 'Please check the connections. Error from class  '+ self.__class__.__name__, 'Info',
                                   wx.OK)
            dlg.ShowModal()
            raise

    def startOfTestcase(self):
        """
        This action is called at the start of the testcase. 
        """
        self.v_measured = 0  # initialise the measured voltage to zero.

    def endOfTestcase(self):
        """
        This action is called at the end of the testcase
        """
        pass  # nothing to do here. Hence pass statement is called.

    def getAdc(self, input_dict):
        """
        This action is called from the scheduler window of the testcase. 
        """
        output_dict = {}
        self.serial_obj.write("a")         # Request analog reading from arduino by sending "a"
        time.sleep(0.02)                   # Add a delay of 20ms (delay can be adjusted as needed). This delay is only for
                                           # providing arduino enough time to report the latest analog reading on receiving "a"
        adc_count = string.strip(self.serial_obj.readline()) # self.serial_obj.readline() reads out the analog voltage reading
                                                             # as a string. strip() removes the whitespace characters from the
                                                             # beginning and the end of the string.
        # print "adc_count = ", adc_count

        if adc_count!='':                                 # arduino seems to ocassionally send empty values. Ignore empty values
            self.v_measured = float(adc_count) / 204.6    # ADC reference voltage used is 5V. And 0-5 V is mapped to 0-1023 count.
                                                          # 1023/5.0 = 204.6. Hence divide the received adc count with 204.8
                                                          # to convert the adc count to voltage value.
        output_dict["Voltage measured"]   = str(self.v_measured)
        return output_dict

    def setPeriod(self, input_dict):
        """
        This action is called from the scheduler window of the testcase. 
        """
        period        = str(int(input_dict["Period"]))
        self.serial_obj.write("p"+period)
        time.sleep(0.2)

        output_dict = {}
        return output_dict

    def setDutycycle(self, input_dict):
        """
        This action is called from the scheduler window of the testcase. 
        """
        dutycycle        = str(int(input_dict["DutyCycle"]))
        self.serial_obj.write("d"+dutycycle)
        time.sleep(0.2)

        output_dict = {}
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
        tmp_device_config_dict = {"Port": " "}
        tmp_device_dict["DeviceConfig"]=tmp_device_config_dict      # do not modify this statement.
        # ***************************************************************************************************************


        # ******************** Action config window definitions *********************************************************
        tmp_device_dict["Actions"] = {}                              # do not modify.

        # Add action configuration
        tmp_action_name = "getAdc"
        tmp_action_inp_dict = { }
        tmp_action_out_dict = {"Voltage measured"   : ""}
        tmp_device_dict["Actions"][tmp_action_name] = [tmp_action_inp_dict, tmp_action_out_dict]  # do not modify

        tmp_action_name = "setPeriod"
        tmp_action_inp_dict = {"Period"   : ""}
        tmp_action_out_dict = { }
        tmp_device_dict["Actions"][tmp_action_name] = [tmp_action_inp_dict, tmp_action_out_dict]  # do not modify

        tmp_action_name = "setDutycycle"
        tmp_action_inp_dict = {"DutyCycle"   : ""}
        tmp_action_out_dict = { }
        tmp_device_dict["Actions"][tmp_action_name] = [tmp_action_inp_dict, tmp_action_out_dict]  # do not modify
        # ***************************************************************************************************************

        return tmp_device_dict
