MemoryLayout_Int8__size     = 1
MemoryLayout_UInt8__size    = 1
MemoryLayout_Int16__size    = 2
MemoryLayout_UInt16__size   = 2
MemoryLayout_Int32__size    = 4
MemoryLayout_UInt32__size   = 4
MemoryLayout_Int64__size    = 8
MemoryLayout_UInt64__size   = 8

MemoryLayout_OperationCodeType__size            = MemoryLayout_UInt16__size
MemoryLayout_ResponseCodeType__size             = MemoryLayout_UInt16__size
MemoryLayout_ObjectFormatCodeType__size         = MemoryLayout_UInt16__size
MemoryLayout_EventCodeType__size                = MemoryLayout_UInt16__size
MemoryLayout_DevicePropCodeType__size           = MemoryLayout_UInt16__size
MemoryLayout_DataTypeCodeType__size             = MemoryLayout_UInt16__size
MemoryLayout_DevicePropPermissionsType__size    = MemoryLayout_UInt8__size
MemoryLayout_DevicePropFormType__size           = MemoryLayout_UInt8__size
MemoryLayout_ptp_fixed_t__size                  = MemoryLayout_Int16__size

import fixedint

class MemoryLayout:

    def size(value):
            
        match type(value):
            case fixedint.Int8:     size = MemoryLayout_Int8__size
            case fixedint.UInt8:    size = MemoryLayout_UInt8__size
            case fixedint.Int16:    size = MemoryLayout_Int16__size
            case fixedint.UInt16:   size = MemoryLayout_UInt16__size
            case fixedint.Int32:    size = MemoryLayout_Int32__size
            case fixedint.UInt32:   size = MemoryLayout_UInt32__size
            case fixedint.Int64:    size = MemoryLayout_Int64__size
            case fixedint.UInt64:   size = MemoryLayout_UInt64__size
            case _:                 size = None    

        return size                

    def sizeTypeString(typeString):

        match typeString:
            case 'int':                     size = MemoryLayout_Int32__size
            case 'Int8':                    size = MemoryLayout_Int8__size
            case 'UInt8':                   size = MemoryLayout_UInt8__size
            case 'Int16':                   size = MemoryLayout_Int16__size
            case 'UInt16':                  size = MemoryLayout_UInt16__size
            case 'Int32':                   size = MemoryLayout_Int32__size
            case 'UInt32':                  size = MemoryLayout_UInt32__size
            case 'Int64':                   size = MemoryLayout_Int64__size
            case 'UInt64':                  size = MemoryLayout_UInt64__size
            case 'OperationCode':           size = MemoryLayout_OperationCodeType__size
            case 'ResponseCode':            size = MemoryLayout_ResponseCodeType__size
            case 'ObjectFormatCode':        size = MemoryLayout_ObjectFormatCodeType__size
            case 'EventCode':               size = MemoryLayout_EventCodeType__size
            case 'DevicePropCode':          size = MemoryLayout_DevicePropCodeType__size
            case 'DataTypeCode':            size = MemoryLayout_DataTypeCodeType__size
            case 'DevicePropPermissions':   size = MemoryLayout_DevicePropPermissionsType__size
            case 'DevicePropForm':          size = MemoryLayout_DevicePropFormType__size
            case _:                         size = None    

        return size                
