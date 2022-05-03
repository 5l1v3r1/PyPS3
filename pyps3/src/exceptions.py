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
class InvalidNotificationType(Exception): pass
class InvalidNotificationMessage(Exception): pass
class InvalidNotificationSound(Exception): pass
class DivIsNone(Exception): pass
class SpeedIsNone(Exception): pass
class EmptyFirmwareResponse(Exception): pass
class GetCurrentGameException(Exception): pass
class GetFirmwareException(Exception): pass
class GetProcListException(Exception): pass
class GetProcsException(Exception): pass
class MemWriteException(Exception): pass
class MemReadException(Exception): pass
class RebootException(Exception): pass
class ShutdownException(Exception): pass
class ProcessIsNone(Exception): pass
class PatchAddressIsNone(Exception): pass
class ReadAddressIsNone(Exception): pass
class HexValueIsNone(Exception): pass