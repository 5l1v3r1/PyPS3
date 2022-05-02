class ConsoleTimedOut(Exception): pass
class ConsoleDidNotRespond(Exception): pass
class ConsoleNotFound(Exception): pass
class ConsoleConnectionError(Exception): pass
class ConsoleRebootError(Exception): pass
class InvalidRebootType(Exception): pass
class InvalidHTTPResponse(Exception): pass
class InvalidLedCode(Exception): pass
class InvalidLedMode(Exception): pass
class InvalidBuzzMode(Exception): pass
class DivIsNone(Exception): pass
class EmptyFirmwareResponse(Exception): pass
class GetCurrentGameException(Exception): pass
class GetFirmwareException(Exception): pass
class GetProcListException(Exception): pass
class GetProcsException(Exception): pass
class MemWriteException(Exception): pass
class ProcessIsNone(Exception): pass
class PatchAddressIsNone(Exception): pass
class HexValueIsNone(Exception): pass