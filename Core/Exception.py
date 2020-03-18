class MapCreationException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class LayerCreationException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class LayerAdditionException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
