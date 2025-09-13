import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from src.paywall_checker.api import router
from src.paywall_checker.auth import router as auth_router
from src.paywall_checker.db import init_db

app = FastAPI()
app.add_middleware(
    SessionMiddleware, secret_key=os.environ.get("SECRET_KEY", "dev")
)


@app.on_event("startup")
def startup_event():
    init_db()


app.include_router(auth_router)
app.include_router(router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

for route in app.routes:
    print(route.name, route.path)
