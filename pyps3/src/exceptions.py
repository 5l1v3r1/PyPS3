class ConsoleTimedOut(Exception): pass
class ConsoleDidNotRespond(Exception): pass
class ConsoleNotFound(Exception): pass
class ConsoleConnectionError(Exception): pass
class ConsoleRebootError(Exception): pass
class ConsoleIsBusy(Exception): pass
    
class InvalidParam(Exception): pass
class InvalidHTTPResponse(Exception): pass

class DivIsNone(Exception): pass
class SpeedIsNone(Exception): pass
class ParamIsNone(Exception): pass

class GetCurrentGameException(Exception): pass
class GetFirmwareException(Exception): pass
class GetProcListException(Exception): pass
class GetProcsException(Exception): pass
class MemWriteException(Exception): pass
class MemReadException(Exception): pass
class RebootException(Exception): pass
class ShutdownException(Exception): pass
class PokeException(Exception): pass
class PeekException(Exception): pass
class DumpException(Exception): pass

class EmptyFirmwareResponse(Exception): pass