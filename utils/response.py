from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message: str = "success", data=None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }

    #通过jsonable_encoder把任何的Fastapi，pydantic、orm对象转换成dict格式 ->code,message,data
    #不用fastapi默认转换，用JSONResponse
    return JSONResponse(content=jsonable_encoder(content))















