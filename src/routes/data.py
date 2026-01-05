
from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from helpers.config import Settings, get_settings
from fastapi.responses import JSONResponse
from controllers import DataController

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
