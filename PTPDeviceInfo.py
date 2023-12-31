# /* -LICENSE-START-
# ** Copyright (c) 2020 Blackmagic Design
# **
# ** Permission is hereby granted, free of charge, to any person or organization
# ** obtaining a copy of the software and accompanying documentation covered by
# ** this license (the "Software") to use, reproduce, display, distribute,
# ** execute, and transmit the Software, and to prepare derivative works of the
# ** Software, and to permit third-parties to whom the Software is furnished to
# ** do so, all subject to the following:
# **
# ** The copyright notices in the Software and this entire statement, including
# ** the above license grant, this restriction and the following disclaimer,
# ** must be included in all copies of the Software, in whole or in part, and
# ** all derivative works of the Software, unless such copies or derivative
# ** works are solely in the form of machine-executable object code generated by
# ** a source language processor.
# **
# ** THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# ** IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# ** FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
# ** SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
# ** FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
# ** ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# ** DEALINGS IN THE SOFTWARE.
# ** -LICENSE-END-
# */


import fixedint
from typing import List
from LogFunctions import *
from PTPTypes import *
from PTPDeserialiser import *

class PTPDeviceInfo:
	
	def __init__(self):
		self.m_protocolVersion 			= fixedint.UInt16(0)
		self.m_vendorExtensionId 		= fixedint.UInt32(0)
		self.m_vendorExtensionVersion 	= fixedint.UInt16(0)
		self.m_vendorExtensionDesc 		= ""
		self.m_functionalMode 			= fixedint.UInt16(0)
		
		self.m_supportedOperationCode 	= [OperationCode]
		self.m_supportedEventCode 		= [EventCode]
		self.m_supportedDevicePropCode 	= [DevicePropCode]
		
		self.m_videoFormats 			= [fixedint.UInt16]
		self.m_imageFormats 			= [fixedint.UInt16]
		
		self.m_manufacturer 			= ""
		self.m_model 					= ""

	
	def deserializeFromPayload(self, data):
		Logger.LogWithInfo("deserializeFromPayload")
		deserialiser = PTPDeserialiser(data)
		try:
			self.m_protocolVersion 			= deserialiser.deserialise(self.m_protocolVersion)
			self.m_vendorExtensionId 		= deserialiser.deserialise(self.m_vendorExtensionId)
			self.m_vendorExtensionVersion 	= deserialiser.deserialise(self.m_vendorExtensionVersion)
			self.m_vendorExtensionDesc 		= deserialiser.deserialise(self.m_vendorExtensionDesc)
			self.m_functionalMode 			= deserialiser.deserialise(self.m_functionalMode)
			self.m_supportedOperationCode 	= deserialiser.deserialise(self.m_supportedOperationCode)
			self.m_supportedEventCode 		= deserialiser.deserialise(self.m_supportedEventCode)
			self.m_supportedDevicePropCode 	= deserialiser.deserialise(self.m_supportedDevicePropCode)
			self.m_videoFormats 			= deserialiser.deserialise(self.m_videoFormats)
			self.m_imageFormats 			= deserialiser.deserialise(self.m_imageFormats)
			self.m_manufacturer 			= deserialiser.deserialise(self.m_manufacturer)
			self.m_model 					= deserialiser.deserialise(self.m_model)
			return True
		except:
			Logger.LogError("deserializeFromPayload: failed")
			# Failed to deserialise PTP device info
			return False

	def printDebug(self):
		Logger.LogWithInfo("DeviceInfo:")
		Logger.LogWithInfo("m_protocolVersion: {}".format(self.m_protocolVersion))
		Logger.LogWithInfo("m_vendorExtensionId: {}".format(self.m_vendorExtensionId))
		Logger.LogWithInfo("m_vendorExtensionVersion: {}".format(self.m_vendorExtensionVersion))
		Logger.LogWithInfo("m_vendorExtensionDesc: {}".format(self.m_vendorExtensionDesc))
		Logger.LogWithInfo("m_functionalMode: {}".format(self.m_functionalMode))
		Logger.LogWithInfo("m_supportedOperationCode: {}".format(self.m_supportedOperationCode))
		Logger.LogWithInfo("m_supportedEventCode: {}".format(self.m_supportedEventCode))
		Logger.LogWithInfo("m_supportedDevicePropCode: {}".format(self.m_supportedDevicePropCode))
		Logger.LogWithInfo("m_manufacturer: {}".format(self.m_manufacturer))
		Logger.LogWithInfo("m_model: {}".format(self.m_model))
