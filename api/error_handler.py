class APIException(Exception):
    def __init__(self, message, status_code=400, error="Operation Failed"):
        self.message = message
        self.status_code = status_code
        self.error = error

    def to_dict(self):
        print('4')
        return {
            "status": "error",
            "message": self.message,
            "error": self.error
        }
