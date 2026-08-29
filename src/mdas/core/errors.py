class MDASException(Exception):
    pass

class InputValidationError(MDASException):
    pass

class BackendUnavailableError(MDASException):
    pass

class ModelUnavailableError(MDASException):
    pass
