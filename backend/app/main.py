from fastapi import FastAPI

from app.core.config import settings

from app.api.routes.advisory import router as advisory_router
from app.api.routes.disease_information import router as disease_information_router
from app.api.routes.diseases import router as diseases_router
from app.api.routes.explorer import router as explorer_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


app.include_router(diseases_router)
app.include_router(disease_information_router)
app.include_router(explorer_router)
app.include_router(advisory_router)


@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }