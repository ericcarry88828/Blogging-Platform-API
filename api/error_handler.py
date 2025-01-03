class APIException(Exception):
    def __init__(self, message, status_code=400, error="operation failed"):
        self.message = message
        self.status_code = status_code
        self.error = error

    def to_dict(self):
        return {
            "status": "error",
            "message": self.message,
            "error": self.error
        }
