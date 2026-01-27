from pymongo import InsertOne
from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .db_schemes.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId


class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNKS_NAME.value]

    async def create_data_chunk(self, data_chunk: DataChunk):
        result= await self.collection.insert_one(data_chunk.model_dump(by_alias=True, exclude_unset=True))
        data_chunk.id = result.inserted_id

        return data_chunk
    
    async def get_chunk(self,chunk_id:str):
        record=await self.collection.find_one({"_id":ObjectId(chunk_id)})

        if record is None:
            return None
        
        return DataChunk(**record)       # change the record dict to pydantic model


    async def insert_many_chunks(self,chunks:list,batch_size:int=100):

        for i in range(0,len(chunks),batch_size):
            batch=chunks[i:i+batch_size]
            operations=[
                InsertOne(chunk.model_dump(by_alias=True, exclude_unset=True)) for chunk in batch
            ]

            await self.collection.bulk_write(operations)

        return len(chunks)
    

    async def get_chunks_by_project_id(self,project_id:ObjectId):
        result=await self.collection.delete_many({"chunk_project_id":project_id})
        return result.deleted_count