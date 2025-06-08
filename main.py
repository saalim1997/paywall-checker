from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.paywall_checker.api import router
from src.paywall_checker.db import init_db

app = FastAPI()


@app.on_event("startup")
def startup_event():
    init_db()


app.include_router(router)

# Mount static last, so it overrides /
app.mount("/", StaticFiles(directory="static", html=True), name="static")
