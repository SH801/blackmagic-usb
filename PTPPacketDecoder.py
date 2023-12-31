# -LICENSE-START-
# Copyright (c) 2020 Blackmagic Design
#
# Permission is hereby granted, free of charge, to any person or organization
# obtaining a copy of the software and accompanying documentation covered by
# this license (the "Software") to use, reproduce, display, distribute,
# execute, and transmit the Software, and to prepare derivative works of the
# Software, and to permit third-parties to whom the Software is furnished to
# do so, all subject to the following:
#
# The copyright notices in the Software and this entire statement, including
# the above license grant, this restriction and the following disclaimer,
# must be included in all copies of the Software, in whole or in part, and
# all derivative works of the Software, unless such copies or derivative
# works are solely in the form of machine-executable object code generated by
# a source language processor.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
# SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
# FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# -LICENSE-END-
# 

import fixedint
from MemoryLayout import *
from LensConfig import *
from PTPTypes import *
from PTPContainer import *
from PTPDeviceInfo import *
from PTPDevicePropDesc import *
from PTPPacketEncoder import *
from LogFunctions import *

# Provide default handler so that delegates are not forced to handle all of them
class PTPPacketDecoderDelegate:

	def __init__(self): pass

	# Responses
	def onResponseReceived(self, transactionId: TransactionID, responseCode: ResponseCode): pass
	
	# Generic Data Received
	def onDataReceived(self, dataContainer: Container): pass
	# Decoded Data Received

	def onDeviceInfoReceived(self, deviceInfo: PTPDeviceInfo): 									pass
	def onExposureReceived(self, exposure: fixedint.Int32): 									pass
	def onGainReceived(self, sensorGain: fixedint.Int32): 										pass
	def onRecordTimeRemainingReceived(	self, \
				   						remainingRecordTimes: List[str], \
										remainingRecordTimesInMinutes: List[fixedint.Int16]): 	pass
	def onBatteryLevelReceived(self, percentage: fixedint.UInt8): 								pass	   
	def onRecordingResolutionReceived(self, width: fixedint.Int16, height: fixedint.Int16): 	pass
	def onApertureFstopReceived(self, fstop: float, stopUnits: LensConfig.ApertureUnits): 		pass
	def onApertureNormalisedReceived(self, normalisedAperture: float): 							pass
	def onFocalLengthReceived(self, focalLength: fixedint.UInt32): 								pass
	def onFocusDistanceReceived(self, focusDistance: fixedint.Int16): 							pass
	def onISOReceived(self, iso: fixedint.Int32): 												pass
	def onShutterSpeedReceived(self, shutterSpeed: fixedint.Int32): 							pass
	def onShutterAngleReceived(self, shutterAngleX100: fixedint.Int32): 						pass
	def onFocusPositionReceived(self, focusPosition: fixedint.Int32): 							pass
	def onWhiteBalanceKelvinReceived(self, whiteBalance: fixedint.Int16): 						pass
	def onWhiteBalanceTintReceived(self, tint: fixedint.Int16): 								pass
	def onFrameRateReceived(self, frameRate: fixedint.Int32): 									pass
	def onOffSpeedFrameRateReceived(self, offSpeedFrameRate: fixedint.Int32): 					pass
	def onOffSpeedEnabledReceived(self, enabled: bool): 										pass
	def onZoomPositionReceived(self, zoomPosition: fixedint.Int32): 							pass
	def onNDFilterReceived(self, stops: float): 												pass    
	def onRecordingStarted(self): 																pass
	def onRecordingStopped(self): 																pass
	
	# Generic Events Received
	def onDevicePropertyChanged(self, devicePropCode: DevicePropCode): 							pass
	def onDevicePropertyDescriptionChanged(self, devicePropCode: DevicePropCode): 				pass

class PTPPacketDecoder:

	def __init__(self): pass

	def DecodePacket(data, ptpPacketDecoderDelegate):
		# decode packet. use static functions for response and event types

		container = Container()
		if container.deserializeContainerDataFromByteArray(data) is False: return

		match (container.m_containerData.type):
			
			case ContainerData.ContainerType.ResponseBlock:
				responseCode = ResponseCode.Undefined
				if container.m_containerData.code in ResponseCode:
					responseCode = ResponseCode(container.m_containerData.code)
				Logger.LogWithInfo("Response: {}. TransactionID: {}".format(responseCode.name, container.m_containerData.transactionId))
				ptpPacketDecoderDelegate.onResponseReceived(container.m_containerData.transactionId, responseCode)
			
			case ContainerData.ContainerType.EventBlock:
				eventCode = EventCode.Undefined
				if container.m_containerData.code in EventCode:
					eventCode = EventCode(container.m_containerData.code)
			
				match eventCode:
					case EventCode.DevicePropChanged:
						# PIMA 15740: 2000 table 21: Event Dataset shows that the parameters must be 4-bytes in size, even though the eventual value type isn't
						typeSize = MemoryLayout_UInt32__size
						validPayloadSize = fixedint.Int32(container.m_containerData.length) - PTPTypes.kContainerHeaderSize
						if (validPayloadSize < typeSize):
							return
						data = container.m_containerData.payload[:typeSize]
						rawData = fixedint.UInt16(UtilityFunctions.FromByteArray(data[:MemoryLayout_UInt16__size]))
						devicePropCode = DevicePropCode.Undefined
						if rawData in DevicePropCode:
							devicePropCode = DevicePropCode(rawData)

						Logger.LogWithInfo("Event: {}. Prop: {}".format(eventCode.name, devicePropCode))
						ptpPacketDecoderDelegate.onDevicePropertyChanged(devicePropCode)

					case EventCode.DevicePropDescChanged:
						typeSize = MemoryLayout_DevicePropCodeType__size
						validPayloadSize = fixedint.Int32(container.m_containerData.length) - PTPTypes.kContainerHeaderSize
						if (validPayloadSize < typeSize):
							return

						data = container.m_containerData.payload[:typeSize]
						devicePropCode = DevicePropCode(UtilityFunctions.FromByteArray(data[:typeSize]))
				
						Logger.LogWithInfo("Event: {}. Prop Desc: {}".format(eventCode.name, devicePropCode))
						ptpPacketDecoderDelegate.onDevicePropertyChanged(devicePropCode)
						ptpPacketDecoderDelegate.onDevicePropertyDescriptionChanged(devicePropCode)

					case EventCode.DeviceInfoChanged:
						Logger.LogWithInfo("Event: {}".format(eventCode.name))

					case EventCode.DeviceReset:
						Logger.LogWithInfo("Event: {}".format(eventCode.name))

					case EventCode.CaptureComplete:
						Logger.LogWithInfo("Event: {}".format(eventCode.name))

					case EventCode.StoreFull:
						Logger.LogWithInfo("Event: {}".format(eventCode.name))

					case EventCode.StoreAdded:
						Logger.LogWithInfo("Event: {}".format(eventCode.name))

					case EventCode.StoreRemoved:
						Logger.LogWithInfo("Event: {}".format(eventCode.name))

					case EventCode.ObjectAdded:
						Logger.LogWithInfo("Event: {}".format(eventCode.name))

					case EventCode.ObjectRemoved:
						Logger.LogWithInfo("Event: {}".format(eventCode.name))

					case EventCode.CancelTransaction:
						Logger.LogWithInfo("Event: {}".format(eventCode.name))

					case _:
						Logger.LogWithInfo("Unhandled Event: {}".format(eventCode))

			case ContainerData.ContainerType.DataBlock:
				operationCode = OperationCode.Undefined
				if container.m_containerData.code in OperationCode:
					operationCode = OperationCode(container.m_containerData.code)
				Logger.LogWithInfo("Data received for Operation: {} for TransactionID: {}".format(operationCode.name, container.m_containerData.transactionId))
				ptpPacketDecoderDelegate.onDataReceived(container)

			case _:
				Logger.LogWarning("Unknown packet received!")
	
	def DecodePayloadAsDeviceInfo(container: Container, ptpPacketDecoderDelegate, DispatchQueue):
		if OperationCode(container.m_containerData.code) != OperationCode.GetDeviceInfo: return None

		validPayloadSize = fixedint.Int32(container.m_containerData.length) - PTPTypes.kContainerHeaderSize
		data = container.m_containerData.payload[:validPayloadSize]

		deviceInfo = PTPDeviceInfo()
		
		if deviceInfo.deserializeFromPayload(data):
			deviceInfo.printDebug()
			DispatchQueue.put_nowait({	'type': 		'Function', \
			    						'function': 	ptpPacketDecoderDelegate.onDeviceInfoReceived, \
										'parameters':	(deviceInfo,)})
			return deviceInfo

		return None
	
	def DecodePayloadAsDevicePropDesc(container: Container, ptpPacketDecoderDelegate, DispatchQueue):
		if OperationCode(container.m_containerData.code) != OperationCode.GetDevicePropDesc: return None

		validPayloadSize = fixedint.Int32(container.m_containerData.length) - PTPTypes.kContainerHeaderSize
		data = container.m_containerData.payload[:validPayloadSize]

		devicePropDesc = PTPDevicePropDesc()		
		if devicePropDesc.deserializeFromPayload(data):
			devicePropDesc.printDebug()
			DispatchQueue.put_nowait({	'type': 		'Function', \
			    						'function': 	ptpPacketDecoderDelegate.onDevicePropDescReceived, \
										'parameters':	(devicePropDesc,)})

			# when prop desc changed the normalised slider position should be adjusted
			match devicePropDesc.m_devicePropCode:
				case DevicePropCode.FNumber:
					currentValue 	= devicePropDesc.getCurrentValue()
					minValue 		= devicePropDesc.getMinimumValue()
					maxValue 		= devicePropDesc.getMaximumValue()
					if 	(type(currentValue) 	== fixedint.UInt16) & \
						(type(minValue) 		== fixedint.UInt16) & \
						(type(maxValue) 		== fixedint.UInt16):					
						if (currentValue >= minValue) & (currentValue <= maxValue):
							DispatchQueue.put_nowait({	'type': 		'Function', \
														'function': 	ptpPacketDecoderDelegate.onApertureFstopReceived, \
														'parameters':	((float(currentValue) / 100.0, LensConfig.ApertureUnits.Fstops),)})
							DispatchQueue.put_nowait({	'type': 		'Function', \
														'function': 	ptpPacketDecoderDelegate.onApertureNormalisedReceived, \
														'parameters':	((float(currentValue - minValue) / float(maxValue - minValue)),)})
																
				case _: pass
			return devicePropDesc
		
		return None

	def DecodePayloadAsDevicePropValue(	container: Container, \
										devicePropCode: DevicePropCode, \
										ptpPacketDecoderDelegate: PTPPacketDecoderDelegate, \
										ptopDevicePropDescs: List[PTPDevicePropDesc],
										DispatchQueue) -> bool:
		if OperationCode(container.m_containerData.code) != OperationCode.GetDevicePropValue: return False

		validPayloadSize = fixedint.Int32(container.m_containerData.length) - PTPTypes.kContainerHeaderSize
		data = container.m_containerData.payload[:validPayloadSize]
		
		match devicePropCode:
			case DevicePropCode.BatteryLevel:
				batteryLevel = fixedint.UInt8(UtilityFunctions.FromByteArray(data[:MemoryLayout_UInt8__size]))
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onBatteryLevelReceived, \
											'parameters':	(batteryLevel,)})

			case DevicePropCode.ImageSize:
				imageSize = ""
				deserialiser = PTPDeserialiser(data)
				try:
					imageSize = deserialiser.deserialise(imageSize)
					dimensionArray = imageSize.split("x")
					if len(dimensionArray) == 2:
						width = int(dimensionArray[0])
						height = int(dimensionArray[1])
						DispatchQueue.put_nowait({	'type': 		'Function', \
													'function': 	ptpPacketDecoderDelegate.onRecordingResolutionReceived, \
													'parameters':	(fixedint.Int16(width), fixedint.Int16(height))})								
				except:
					Logger.LogError("Failed to decode image size data container")
			
			case DevicePropCode.FNumber:
				minFNumber = fixedint.UInt16(0)
				maxFNumber = fixedint.UInt16(2200)            
				fnumber = fixedint.Int16(UtilityFunctions.FromByteArray(data[:MemoryLayout_UInt16__size]))
			
				FNumberProps = list(filter(lambda x: x.m_devicePropCode == devicePropCode, ptopDevicePropDescs))
				if len(FNumberProps) != 0:
					FNumberProp = FNumberProps[0]
					if 	(type(FNumberProp.getMinimumValue()) == fixedint.UInt16) & \
						(type(FNumberProp.getMaximumValue()) == fixedint.UInt16):					
						minFNumber = fixedint.UInt16(FNumberProp.getMinimumValue())
						maxFNumber = fixedint.UInt16(FNumberProp.getMaximumValue())
						
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onApertureFstopReceived, \
											'parameters':	(float(fnumber) / 100.0, LensConfig.ApertureUnits.Fstops)})								
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onApertureNormalisedReceived, \
											'parameters':	(((float(fnumber) - float(minFNumber)) / (float(maxFNumber) - float(minFNumber))),)})								

			case DevicePropCode.FocalLength:
				focalLength = fixedint.UInt32(UtilityFunctions.FromByteArray(data[:MemoryLayout_UInt32__size]))
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onFocalLengthReceived, \
											'parameters':	(focalLength,)})								

			case DevicePropCode.FocusDistance:
				focusDistance = fixedint.Int16(UtilityFunctions.FromByteArray(data[:MemoryLayout_Int16__size]))
				Logger.LogWithInfo("Focus distance: {}".format(focusDistance))
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onFocusDistanceReceived, \
											'parameters':	(focusDistance,)})								

			case DevicePropCode.ExposureIndex:
				iso = fixedint.Int16(UtilityFunctions.FromByteArray(data[:MemoryLayout_Int16__size]))
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onISOReceived, \
											'parameters':	(iso,)})								

			case DevicePropCode.BMD_ShutterSpeed:
				shutterSpeed = fixedint.Int16(UtilityFunctions.FromByteArray(data[:MemoryLayout_Int16__size]))
				# PTP fires both shutter speed and angle. UI always updates both. Choose angle over speed for now
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onShutterSpeedReceived, \
											'parameters':	(shutterSpeed,)})								

			case DevicePropCode.BMD_ShutterAngle:
				shutterAngleX100 = fixedint.Int16(UtilityFunctions.FromByteArray(data[:MemoryLayout_Int16__size]))
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onShutterAngleReceived, \
											'parameters':	(shutterAngleX100,)})								

			case DevicePropCode.BMD_FocusPosition:
				focusPosition = fixedint.Int32(UtilityFunctions.FromByteArray(data[:MemoryLayout_Int32__size]))
				Logger.LogWithInfo("Focus position: {}".format(focusPosition))
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onFocusPositionReceived, \
											'parameters':	(focusPosition,)})								

			case DevicePropCode.BMD_WhiteBalanceKelvin:
				whiteBalanceKelvin = fixedint.Int16(UtilityFunctions.FromByteArray(data[:MemoryLayout_Int16__size]))
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onWhiteBalanceKelvinReceived, \
											'parameters':	(whiteBalanceKelvin,)})								

			case DevicePropCode.BMD_WhiteBalanceTint:
				whiteBalanceTint = fixedint.Int8(UtilityFunctions.FromByteArray(data[:MemoryLayout_Int8__size]))
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onWhiteBalanceTintReceived, \
											'parameters':	(whiteBalanceTint,)})								

			case DevicePropCode.BMD_FrameRate:
				frameRate = fixedint.Int32(UtilityFunctions.FromByteArray(data[:MemoryLayout_Int32__size]))
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onFrameRateReceived, \
											'parameters':	(frameRate,)})								

			case DevicePropCode.BMD_OffSpeedFrameRate:
				offSpeedFrameRate = fixedint.Int32(UtilityFunctions.FromByteArray(data[:MemoryLayout_Int32__size]))
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onOffSpeedFrameRateReceived, \
											'parameters':	(offSpeedFrameRate,)})								

			case DevicePropCode.BMD_OffSpeedEnabled:
				offSpeedEnabled = fixedint.UInt8(UtilityFunctions.FromByteArray(data[:MemoryLayout_UInt8__size]))
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onOffSpeedEnabledReceived, \
											'parameters':	(offSpeedEnabled != 0,)})								

			case DevicePropCode.BMD_ZoomPosition:
				zoomPosition = fixedint.Int32(UtilityFunctions.FromByteArray(data[:MemoryLayout_Int32__size]))
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onZoomPositionReceived, \
											'parameters':	(zoomPosition,)})								

			case DevicePropCode.BMD_RecordingState:
				recording = fixedint.UInt8(UtilityFunctions.FromByteArray(data[:MemoryLayout_UInt8__size]))
				if (recording != 0): 	
					DispatchQueue.put_nowait({	'type': 		'Function', \
												'function': 	ptpPacketDecoderDelegate.onRecordingStarted, \
												'parameters':	()})								
				else: 
					DispatchQueue.put_nowait({	'type': 		'Function', \
												'function': 	ptpPacketDecoderDelegate.onRecordingStopped, \
												'parameters':	()})								

			case DevicePropCode.BMD_NDFilter:
				ptpNDFilter = ContainerData.ptp_fixed_t(UtilityFunctions.FromByteArray(data[:MemoryLayout_ptp_fixed_t__size]))
				DispatchQueue.put_nowait({	'type': 		'Function', \
											'function': 	ptpPacketDecoderDelegate.onNDFilterReceived, \
											'parameters':	(PTPTypes.PTPfloatFromFixed(ptpNDFilter),)})								

			case _: pass
		
		return True
