from enum import Enum

class ResponseStatus(Enum):
    SUCCESS = "file uploaded successfully"
    FILE_TYPE_NOT_SUPPORTED = "file type not supported"
    FILE_SIZE_EXCEEDED = "file size exceeded"
    FILE_UPLOAD_ERROR = "file upload error"