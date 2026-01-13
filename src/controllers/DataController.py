from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseStatus
from .ProjectController import ProjectController
import re
import os

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
    
    def generate_unique_filepath(self,original_filename:str,project_id:str):
        random_file_name=self.generate_random_string()
        project_path=ProjectController().get_project_path(project_id)
        cleaned_file_name=self.get_clean_filename(original_filename)

        new_file_path=os.path.join(project_path,random_file_name+"_"+cleaned_file_name)

        while os.path.exists(new_file_path):
            random_file_name=self.generate_random_string()
            new_file_path=os.path.join(project_path,random_file_name+"_"+cleaned_file_name)
            
        return new_file_path,random_file_name+"_"+cleaned_file_name




    def get_clean_filename(self,original_filename:str):
        cleaned_filename=re.sub(r'[^\w.]', '', original_filename.strip())
        cleaned_filename=cleaned_filename.replace(' ','_')
        return cleaned_filename
