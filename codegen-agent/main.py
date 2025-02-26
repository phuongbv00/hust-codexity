from fastapi import FastAPI
from config.config import Settings
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World", "config": Settings()}

# @app.post("/generate-code")
# async def generate_code(item: Item):
#     return item