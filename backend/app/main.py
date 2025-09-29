from fastapi import FastAPI

app = FastAPI()

@app.get("/sup")
async def root():
    return {"message", "Hey Jake, You will be sth great!"}
