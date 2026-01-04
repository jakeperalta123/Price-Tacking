from fastapi import FastAPI
from app.routers import user_router, auth_router, product_router, price_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app = FastAPI(
    title="Price Tracking API",
    version="1.0.0",
    description="API for price tracking",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,         
    allow_methods=["*"],           
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(product_router.router)
app.include_router(price_router.router)
