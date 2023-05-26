from enum import Enum

class ErrorMessage(Enum):
    WRONG_STATUS_CODE = 'Expected code 400'
    WRONG_INSTANCE_RESULT = 'Expected correct assertion'
    WRONG_ERROR_CLASS = 'Expected ZeroDivisionError'