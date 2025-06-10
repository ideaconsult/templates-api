import logging
import time
import traceback
from datetime import timedelta
from importlib.metadata import version

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request

from tplapi.api import info, tasks, templates
from tplapi.models.models import tasks_db
from tplapi.services import template_service
from .config.app_config import initialize_dirs

config, UPLOAD_DIR, NEXUS_DIR, TEMPLATE_DIR = initialize_dirs(migrate=True)

try:
    package_version = version("ramanchada-api")
except Exception:
    package_version = "Unknown"


app = FastAPI(
    title="Templates API",
    version=package_version,
    description="A web API for the Template Designer",
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Get the stack trace
    stack_trace = traceback.format_exc()

    # Log the stack trace
    logging.error(f"Unhandled exception: {str(exc)}\nStack trace:\n{stack_trace}")

    # Optionally print the stack trace to the console (for development purposes)
    print(f"Unhandled exception: {str(exc)}\nStack trace:\n{stack_trace}")

    # Return a generic error response
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


def cleanup_tasks():
    current_time = int(
        time.time() * 1000
    )  # Current time in seconds , ms are fractional
    two_hours_ago = current_time - (2 * 60 * 60 * 1000)  # Two hours in ms
    # two_hours_ago = current_time - (10 * 60 * 1000)  # 10 min  in ms
    # print(current_time,two_hours_ago)
    tasks_to_remove = [
        task_id
        for task_id, task_data in tasks_db.items()
        if task_data.completed < two_hours_ago and task_data.status != "Running"
    ]
    # print(tasks_to_remove)
    for task_id in tasks_to_remove:
        tasks_db.pop(task_id)


def cleanup_templates():
    template_service.cleanup(timedelta(hours=24 * 30 * 6))


app.include_router(tasks.router, prefix="", tags=["task"])
app.include_router(info.router, prefix="", tags=["info"])
app.include_router(templates.router, prefix="", tags=["templates"])

for route in app.routes:
    print(f"Route: {route.path} | Methods: {route.methods}")
scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_tasks, "interval", minutes=120)  # Clean up every 120 minutes
# scheduler.add_job(cleanup_templates, 'interval', hours=24)  # test, otherwise once a day would be ok
scheduler.start()
