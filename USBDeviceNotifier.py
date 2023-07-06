#
#  USBDeviceNotifier.swift
#  USBControl
#

import usb1
import fixedint
from LogFunctions import *
from USBBulkDevice import *
from StoppableThread import *

class Notification:
	USBDeviceConnected 		= "USBDeviceConnected"
	USBDeviceDisconnected 	= "USBDeviceDisconnected"
    
class USBWorkerThread(StoppableThread):

	def setUSBContext(self, usbContext):
		self.m_usbContext = usbContext

	def run(self):
		Logger.ThreadLogWithInfo("USBWorkerThread: started")
		while not self.stopped():
			try:
				# Logger.ThreadLogWithInfo("USBWorkerThread: waiting on handleEvents")
				# self.m_usbContext.handleEvents()
				self.m_usbContext.handleEventsTimeout(1)
				# Logger.ThreadLogWithInfo("USBWorkerThread: processed handleEvents")
			except (KeyboardInterrupt, SystemExit):
				Logger.ThreadLogWithInfo("USBWorkerThread: leaving usbprocessing due to interrupt/exit request")
		Logger.ThreadLogWithInfo("USBWorkerThread: stopped")
	    
class USBDeviceNotifier:

	# Create filter for USBDeviceNotifier
	def __init__(self, usbContext, usbManagerQueue):
		self.m_usbContext					= usbContext
		self.m_usbManagerQueue 			= usbManagerQueue
		# Filter options
		self.m_vendorId						= None
		self.m_productId					= None
		self.m_devClass						= None
		self.m_interfaceClass 				= None
		self.m_interfaceSubClass			= None
		self.m_interfaceProtocol			= None
		self.m_interfaceAlternateSetting	= None
		self.m_hotplugHandle				= None
		self.m_usbWorkerThread 				= USBWorkerThread(name="USBWorkerThread")

		self.m_usbWorkerThread.setUSBContext(self.m_usbContext)
		self.m_usbWorkerThread.start()

	def addFilterVendorId(self, vendorId: fixedint.UInt16):
		self.m_vendorId = vendorId
	
	def addFilterProductId(self, productId: fixedint.UInt16):
		self.m_productId = productId
	
	def addFilterDevClass(self, devClass: fixedint.UInt16):
		self.m_devClass = devClass

	def addFilterInterface(		self,
								interfaceClass = None,
								interfaceSubClass = None,
								interfaceProtocol = None,
								interfaceAlternateSetting = None):
		if interfaceClass is not None: 				self.m_interfaceClass = interfaceClass
		if interfaceSubClass is not None: 			self.m_interfaceSubClass = interfaceSubClass
		if interfaceProtocol is not None: 			self.m_interfaceProtocol = interfaceProtocol
		if interfaceAlternateSetting is not None:	self.m_interfaceAlternateSetting = interfaceAlternateSetting

	def _onHotplugEvent(self, context, device, event):
		match(event):
			case usb1.HOTPLUG_EVENT_DEVICE_ARRIVED:		self.rawDeviceAdded(device)
			case usb1.HOTPLUG_EVENT_DEVICE_LEFT:		self.rawDeviceRemoved(device)

	# Start Blackmagic Design USB device monitoring
	def start(self):

		vendorId 	= usb1.HOTPLUG_MATCH_ANY
		productId 	= usb1.HOTPLUG_MATCH_ANY
		devClass 	= usb1.HOTPLUG_MATCH_ANY
		if self.m_vendorId is not None: 	vendorId = self.m_vendorId
		if self.m_productId is not None: 	productId = self.m_productId
		if self.m_devClass is not None: 	devClass = self.m_devClass
	
		if not self.m_usbContext.hasCapability(usb1.CAP_HAS_HOTPLUG):
			Logger.LogError('Hotplug support is missing. Please update your libusb version.')
			return
		
		self.m_hotplugHandle = self.m_usbContext.hotplugRegisterCallback(	self._onHotplugEvent,
														events=usb1.HOTPLUG_EVENT_DEVICE_ARRIVED | usb1.HOTPLUG_EVENT_DEVICE_LEFT,
														vendor_id=vendorId,
														product_id=productId,
														dev_class=devClass )
		
	def rawDeviceAdded(self, device):
	
		did 				= str(device)
		vendorId 			= device.getVendorID()
		productId 			= device.getProductID()
		name 				= str(device)
		interfaceNumber 	= None
		interfaceSetting	= None

		Logger.LogWithInfo("Device added: {}".format(device))

		if (self.m_interfaceClass is not None) & (self.m_interfaceSubClass is not None):
			for configuration in device.iterConfigurations():
				for interface in configuration:
					for setting in interface.iterSettings():
						if 	(setting.getClass() == self.m_interfaceClass) & \
							(setting.getSubClass() == self.m_interfaceSubClass):
							interfaceNumber = setting.getNumber()
							interfaceSetting = setting
							break

		if (interfaceNumber is not None):
			Logger.LogWithInfo("Found correct interface {} on device {}".format(interfaceNumber, name))

			device = USBBulkDevice(	id=did, \
									usbContext=self.m_usbContext, \
									vendorId=vendorId, \
									productId=productId, \
									name=name, \
									deviceInterface=device, \
									interfaceNumber=interfaceNumber, \
									interfaceSetting=interfaceSetting)
		
			self.m_usbManagerQueue.put_nowait({'type': 'Notification', 'name': Notification.USBDeviceConnected, 'userInfo': {"device": device}})
    
	def fakeRemove(self):
		self.m_usbManagerQueue.put_nowait({'type': 'Notification', 'name': Notification.USBDeviceDisconnected, 'userInfo': {"id": 'Bus 020 Device 030: ID 1edb:be44'}})

	def rawDeviceRemoved(self, device):
		print(device)
		Logger.LogWithInfo("Device removed: {}".format(device))

		# deviceId = device.id
		self.m_usbManagerQueue.put_nowait({'type': 'Notification', 'name': Notification.USBDeviceDisconnected, 'userInfo': {"id": device}})

	def stop(self):
		if self.m_hotplugHandle is not None:
			if not self.m_usbContext.hasCapability(usb1.CAP_HAS_HOTPLUG):
				Logger.LogError('Hotplug support is missing. Please update your libusb version.')
				return
			self.m_usbContext.hotplugDeregisterCallback(self.m_hotplugHandle)			
			self.m_hotplugHandle = None

		if self.m_usbWorkerThread is not None:
			self.m_usbWorkerThread.stop()
			Logger.ThreadLogWithInfo("Sent shutdown to USBWorkerThread")	
			self.m_usbWorkerThread.join()
			self.m_usbWorkerThread = None

	def __del__(self):
		self.stop()

