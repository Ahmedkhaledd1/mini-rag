from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseStatus

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale=1048576  # 1 MB in bytes

    def validate_uploaded_file(self,file:UploadFile):

        if file.content_type not in self.settings.FILE_ALLOWED_TYPES:
            return False,ResponseStatus.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.settings.FILE_MAX_SIZE * self.size_scale:
            return False,ResponseStatus.FILE_SIZE_EXCEEDED.value
        return True,ResponseStatus.SUCCESS.value