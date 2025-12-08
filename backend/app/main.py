from fastapi import FastAPI
from routers import user_router, auth_router

app = FastAPI(
    title="Price Tracking API",
    version="1.0.0",
    description="API for price tracking",
)

app.include_router(user_router.router)
app.include_router(auth_router.router)
