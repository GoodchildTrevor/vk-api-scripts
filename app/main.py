from fastapi import FastAPI

from app.routers import files, groups, wall

app = FastAPI(
    title="VK API Scripts",
    description="REST API wrapper for common VK API operations",
    version="1.0.0",
)

app.include_router(wall.router)
app.include_router(groups.router)
app.include_router(files.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
