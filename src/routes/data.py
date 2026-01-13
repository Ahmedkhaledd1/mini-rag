
import aiofiles
from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from helpers.config import Settings, get_settings
from fastapi.responses import JSONResponse
from controllers import DataController,ProjectController,ProcessController
from .schemas import ProcessRequest
from models import ResponseStatus
import logging
import os

logger=logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str,file: UploadFile,
                    app_settings : Settings =Depends(get_settings)):
    
    is_valid, message = DataController().validate_uploaded_file(file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"status":message}
            )
    
    file_path,file_name=DataController().generate_unique_filepath(file.filename,project_id)
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status":ResponseStatus.FILE_UPLOAD_FAILED.value}
            )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status":message
                ,"file_id":file_name}
        )


@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str,request: ProcessRequest):
    
    file_name=request.file_name
    chunk_size=request.chunk_size
    overlap_size=request.overlap_size
    process_controller=ProcessController(project_id=project_id)

    file_chunks=process_controller.process_file_content(
        filename=file_name,
        chunk_size=chunk_size,
        chunk_overlap=overlap_size)

    if file_chunks is None or len(file_chunks)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status":ResponseStatus.PROCESSING_FAILED.value}
            )
    
    return file_chunks






