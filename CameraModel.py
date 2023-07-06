# -LICENSE-START-
# Copyright (c) 2018 Blackmagic Design
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
from BaseEnum import *

CameraModelType = fixedint.UInt8
class CameraModel(BaseEnum):
	Unknown 				= CameraModelType(0)
	CinemaCamera 			= CameraModelType(1)
	PocketCinemaCamera 		= CameraModelType(2)
	ProductionCamera4K 		= CameraModelType(3)
	StudioCamera 			= CameraModelType(4)
	StudioCamera4K 			= CameraModelType(5)
	URSA 					= CameraModelType(6)
	MicroCinemaCamera 		= CameraModelType(7)
	MicroStudioCamera 		= CameraModelType(8)
	URSAMini 				= CameraModelType(9)
	URSAMiniPro 			= CameraModelType(10)
	URSABroadcast 			= CameraModelType(11)
	URSAMiniProG2 			= CameraModelType(12)
	PocketCinemaCamera4K 	= CameraModelType(13)
	PocketCinemaCamera6K 	= CameraModelType(14)
	PocketCinemaCamera6KPro = CameraModelType(15)
	URSAMiniPro12K 			= CameraModelType(16)
	URSABroadcastG2 		= CameraModelType(17)
	StudioCamera4KPlus 		= CameraModelType(18)
	StudioCamera4KPro 		= CameraModelType(19)
	PocketCinemaCamera6KG2 	= CameraModelType(20)
	StudioCamera4KExtreme 	= CameraModelType(21)

	def camerafromInt(value: CameraModelType):
		return CameraModel(value) if value in CameraModel else CameraModel.Unknown

	def camerafromName(name: str):
		nameToModel = {
			"Cinema Camera": 				CameraModel.CinemaCamera,
			"Micro Cinema Camera": 			CameraModel.MicroCinemaCamera,
			"Micro Studio Camera": 			CameraModel.MicroStudioCamera,
			"Pocket Cinema Camera": 		CameraModel.PocketCinemaCamera,
			"Pocket Cinema Camera 4K": 		CameraModel.PocketCinemaCamera4K,
			"Pocket Cinema Camera 6K": 		CameraModel.PocketCinemaCamera6K,
			"Pocket Cinema Camera 6K G2": 	CameraModel.PocketCinemaCamera6KG2,
			"Pocket Cinema Camera 6K Pro": 	CameraModel.PocketCinemaCamera6KPro,
			"Production Camera 4K": 		CameraModel.ProductionCamera4K,
			"Studio Camera": 				CameraModel.StudioCamera,
			"Studio Camera 4K": 			CameraModel.StudioCamera4K,
			"Studio Camera 4K Extreme": 	CameraModel.StudioCamera4KExtreme,
			"Studio Camera 4K Plus": 		CameraModel.StudioCamera4KPlus,
			"Studio Camera 4K Pro": 		CameraModel.StudioCamera4KPro,
			"URSA": 						CameraModel.URSA,
			"URSA Broadcast": 				CameraModel.URSABroadcast,
			"URSA Broadcast G2": 			CameraModel.URSABroadcastG2,
			"URSA Mini": 					CameraModel.URSAMini,
			"URSA Mini Pro": 				CameraModel.URSAMiniPro,
			"URSA Mini Pro 12K": 			CameraModel.URSAMiniPro12K,
			"URSA Mini Pro G2": 			CameraModel.URSAMiniProG2,
		}

		return nameToModel[name] if name in nameToModel.keys() else CameraModel.Unknown

	def isPocket(self) -> bool:
		match (self):
			case CameraModel.PocketCinemaCamera:		return True
			case CameraModel.PocketCinemaCamera4K:		return True
			case CameraModel.PocketCinemaCamera6K:		return True
			case CameraModel.PocketCinemaCamera6KG2:	return True
			case CameraModel.PocketCinemaCamera6KPro: 	return True
			case _: 									return False

