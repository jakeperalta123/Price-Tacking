from fastapi import FastAPI
from app.routers import user_router, auth_router, product_router, price_router

app = FastAPI(
    title="Price Tracking API",
    version="1.0.0",
    description="API for price tracking",
)

app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(product_router.router)
app.include_router(price_router.router)
