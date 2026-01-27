
import aiofiles
from fastapi import FastAPI,APIRouter,Depends,UploadFile,status,Request
from helpers.config import Settings, get_settings
from fastapi.responses import JSONResponse
from controllers import DataController,ProjectController,ProcessController
from .schemas import ProcessRequest
from models import ResponseStatus
import logging
from models import ProjectModel
from models import ChunkModel
from models.db_schemes.data_chunks import  DataChunk
import os

logger=logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
)

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request,project_id: str,file: UploadFile,
                    app_settings : Settings =Depends(get_settings)):
    
    project_model=ProjectModel(db_client=request.app.db_client)
    
    project =await project_model.get_project_or_create(project_id=project_id)
    
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
                ,"file_id":file_name,
                "project_id":str(project.id)}
        )


@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request,project_id: str,process_request: ProcessRequest):

    project_model=ProjectModel(db_client=request.app.db_client)
    
    project =await project_model.get_project_or_create(project_id=project_id)
    chunk_model=ChunkModel(db_client=request.app.db_client)

    

    
    file_name=process_request.file_name
    chunk_size=process_request.chunk_size
    overlap_size=process_request.overlap_size
    do_reset=process_request.do_reset
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
    
    file_chunks_records=[
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id=project.id

        )
        for i, chunk in enumerate(file_chunks)
    ]

    if do_reset==1:
        await chunk_model.get_chunks_by_project_id(project_id=project.id)


    no_of_records= await chunk_model.insert_many_chunks(chunks=file_chunks_records,batch_size=100)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status":ResponseStatus.PROCESSING_SUCCESS.value,
                "total_chunks_created":no_of_records}
    )








