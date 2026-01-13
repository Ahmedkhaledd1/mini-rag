from .BaseController import BaseController
from .ProjectController import ProjectController
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum
import os

class ProcessController(BaseController):
    def __init__(self, project_id:str):
        super().__init__()
        self.project_id=project_id
        self.project_path=ProjectController().get_project_path(project_id)
    

    def get_file_extension(self,filename:str):
        file_extension=os.path.splitext(filename)[-1]
        return file_extension

    def get_file_loader(self,filename:str):
        file_path=os.path.join(self.project_path,filename)
        file_extension=self.get_file_extension(filename)
        if file_extension==ProcessingEnum.TXT.value:

            return TextLoader(file_path=file_path, encoding='utf-8')
        if file_extension==ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path=file_path)
        

        return None
    
    def get_file_content(self,filename:str):
        loader=self.get_file_loader(filename)
        return loader.load() 
    

    def process_file_content(self,filename:str,chunk_size:int=100,chunk_overlap:int=20):
        documents=self.get_file_content(filename)
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        )

        file_content_texts=[
            doc.page_content for doc in documents
        ]
        file_content_metadata=[
            doc.metadata for doc in documents
        ]
        chunks=text_splitter.create_documents(
            file_content_texts,
            file_content_metadata
        )
        return chunks
    