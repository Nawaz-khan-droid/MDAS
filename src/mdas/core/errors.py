class MDASException(Exception):
    pass

class InputValidationError(MDASException):
    pass

class BackendUnavailableError(MDASException):
    pass

class ModelUnavailableError(MDASException):
    pass

class UnsupportedLanguageError(MDASException):
    def __init__(self, code, name, confidence, method, message="MDAS V1 currently supports English text."):
        self.code = code
        self.name = name
        self.confidence = confidence
        self.method = method
        self.message = message
        super().__init__(self.message)
