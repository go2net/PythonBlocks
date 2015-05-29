# ctypes and os shouldn't be re-exported.
import ctypes as _ctypes
import os as _os


# Part One: Type Assignments for G and Instrument Drivers, see spec table
# 3.1.1.
#
# Remark: The pointer and probably also the array variants are of no
# significance in Python because there is no native call-by-reference.
# However, as long as I'm not fully sure about this, they won't hurt.

def _type_dublet(ctypes_type):
    return (ctypes_type, _ctypes.POINTER(ctypes_type))

def _type_triplet(ctypes_type):
    return _type_dublet(ctypes_type) + (_ctypes.POINTER(ctypes_type),)

UInt32, PUInt32, AUInt32    = _type_triplet(_ctypes.c_ulong)
Int32, PInt32, AInt32       = _type_triplet(_ctypes.c_long)
UInt16, PUInt16, AUInt16    = _type_triplet(_ctypes.c_ushort)
Int16, PInt16, AInt16       = _type_triplet(_ctypes.c_short)
UInt8, PUInt8, AUInt8       = _type_triplet(_ctypes.c_ubyte)
Int8, PInt8, AInt8          = _type_triplet(_ctypes.c_byte)
Addr, PAddr, AAddr          = _type_triplet(_ctypes.c_void_p)
Char, PChar, AChar          = _type_triplet(_ctypes.c_char)
Byte, PByte, AByte          = _type_triplet(_ctypes.c_ubyte)
Boolean, PBoolean, ABoolean = _type_triplet(UInt16)
Real32, PReal32, AReal32    = _type_triplet(_ctypes.c_float)
Real64, PReal64, AReal64    = _type_triplet(_ctypes.c_double)

# The following three type triplets are defined rather pathologically, both in
# the spec and the reference .h file.  Therefore, I can't use _type_triplet.

Buf         = PByte
PBuf        = Buf
ABuf        = _ctypes.POINTER(Buf)

String      = _ctypes.c_char_p  # PChar in the spec
PString     = _ctypes.c_char_p  # PChar in the spec
AString     = _ctypes.POINTER(String)

# It is impractical to have Buf defined as an array of unsigned chars,
# because ctypes forces me then to cast the string buffer to an array type.
# The only semantic difference is that String is null terminated while Buf
# is not (as I understand it).  However, in Python there is no difference.
# Since the memory representation is the same -- which is guaranteed by the C
# language specification -- the following Buf re-definitions are sensible:

Buf = PBuf = String
ABuf        = _ctypes.POINTER(Buf)

Rsrc        = String
PRsrc       = String
ARsrc       = _ctypes.POINTER(Rsrc)

Status, PStatus, AStatus    = _type_triplet(Int32)
Version, PVersion, AVersion = _type_triplet(UInt32)
Object, PObject, AObject    = _type_triplet(UInt32)
Session, PSession, ASession = _type_triplet(Object)

Attr        = UInt32
ConstString = _ctypes.POINTER(Char)


# Part Two: Type Assignments for G only, see spec table 3.1.2.  The
# difference to the above is of no significance in Python, so I use it here
# only for easier synchronisation with the spec.

AccessMode, PAccessMode = _type_dublet(UInt32)
BusAddress, PBusAddress = _type_dublet(UInt32)

BusSize     = UInt32

AttrState, PAttrState   = _type_dublet(UInt32)

# The following is weird, taken from news:zn2ek2w2.fsf@python.net
VAList      = _ctypes.POINTER(_ctypes.c_char)

EventType, PEventType, AEventType = _type_triplet(UInt32)

PAttr       = _ctypes.POINTER(Attr)
AAttr       = PAttr

EventFilter = UInt32

FindList, PFindList     = _type_dublet(Object)
Event, PEvent           = _type_dublet(Object)
KeyId, PKeyId           = _type_dublet(String)
JobId, PJobId           = _type_dublet(UInt32)

# Class of callback functions for event handling, first type is result type
if _os.name == 'nt':
    Hndlr = _ctypes.WINFUNCTYPE(Status, Session, EventType, Event,
                                  Addr)
else:
    Hndlr = _ctypes.CFUNCTYPE(Status, Session, EventType, Event,
                                Addr)
