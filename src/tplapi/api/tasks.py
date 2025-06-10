from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response, status

from tplapi.models.models import get_tasks_db, Task

router = APIRouter()


@router.get("/task/{uuid}", response_model=Task)
async def get_task(
    request: Request,
    uuid: str,
    response: Response,
    if_none_match: str = None,
    if_modified_since: datetime = None,
    tasks_db: dict = Depends(get_tasks_db),
):
    if if_none_match is None:
        if_none_match = Header(None, alias="If-None-Match")
    if if_modified_since is None:
        if_modified_since = Header(None, alias="If-Modified-Since")
    if uuid in tasks_db:
        # Check Last-Modified header
        # if if_modified_since and if_modified_since >= last_modified_time:
        #    return JSONResponse(content=None, status_code=304)

        if tasks_db[uuid].status == "Error":
            response.status_code = status.HTTP_400_BAD_REQUEST
            return tasks_db[uuid]
        else:
            return tasks_db[uuid]
    else:
        raise HTTPException(status_code=404, detail="Not found")


@router.get("/task", response_model=List[Task])
async def get_tasks(tasks_db: Dict[str, Task] = Depends(get_tasks_db)):
    return list(tasks_db.values())
