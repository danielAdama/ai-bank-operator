from typing import Optional, Any, AnyStr, Dict, Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status

def handle_error_render_json_response(
        ex, 
        data: Union[Dict, None] = None, 
        status_code = None
    ):
    err_msg = ex.detail if hasattr(ex, 'detail') else str(ex)
    err_dict = {
        "status_code": ex.status_code if hasattr(ex, 'status_code') else status_code,
        "detail": err_msg
    }

    res = {
        'success': False,
        'data': data,
        'message': err_dict["detail"]
    }

    content = jsonable_encoder(res)
    return JSONResponse(content=content, status_code=err_dict["status_code"])

def handle_success_render_json_response(
        msg: AnyStr, 
        data: Union[Dict, None] = None, 
        status_code: int = status.HTTP_201_CREATED,
    ):

    res = {
        'success': True,
        'data': data,
        'message': msg
    }

    content = jsonable_encoder(res)
    response = JSONResponse(content=content, status_code=status_code)
    
    return response