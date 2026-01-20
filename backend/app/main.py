from fastapi import FastAPI
from app.routers import user_router, auth_router, product_router, price_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.redis import redis_client
from contextlib import asynccontextmanager

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to Redis")
    await redis_client.connect()
    yield
    print("Closing Redis connection")
    if redis_client.redis:
        await redis_client.redis.close()

app = FastAPI(
    title="Price Tracking API",
    version="1.0.0",
    description="API for price tracking",
    lifespan=lifespan
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
