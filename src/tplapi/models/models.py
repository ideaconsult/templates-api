from typing import Dict, Optional

from pydantic import BaseModel


class Task(BaseModel):
    uri: Optional[str] = None
    id: str
    name: str
    error: Optional[str] = None
    policyError: Optional[str] = None
    status: str
    started: int
    completed: Optional[int] = None
    result: str
    result_uuid: Optional[str] = None
    errorCause: Optional[str] = None


# --- In-memory "database" simulation ---
_global_tasks_db: Dict[str, Task] = {}


# --- Dependency to get the tasks database ---
def get_tasks_db() -> Dict[str, Task]:
    """
    Dependency that provides the in-memory tasks database.
    In a real app, this would provide a database session or connection.
    """
    return _global_tasks_db
