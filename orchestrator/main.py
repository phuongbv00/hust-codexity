from fastapi import FastAPI
import uvicorn
from fastapi import FastAPI
from controllers import controllers
from config import config

app = FastAPI()

# Đăng ký router
app.include_router(controllers.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8083)
