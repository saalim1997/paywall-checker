from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .db import add_link, get_links, init_db
from .paywall import is_accessible
from .utils import get_proreader_url

app = FastAPI()


@app.on_event("startup")
def startup_event():
    init_db()


# @app.get("/")
# def read_root():
#     return {"message": "Paywall Checker Service Running"}


class LinkRequest(BaseModel):
    url: str


@app.post("/links/")
def save_link(link: LinkRequest):
    add_link(link.url)
    return {"message": "Link saved", "url": link.url}


@app.post("/check/")
def check_links():
    links = get_links(status="paywalled")
    results = []
    for link in links:
        link_id = link["id"]
        url = link["url"]
        accessible = is_accessible(url)
        results.append({"id": link_id, "url": url, "accessible": accessible})
    return results


# ------ Router Section ------
router = APIRouter()


@router.get("/links/")
def list_links():
    links = get_links()
    results = []
    for link in links:
        url = link["url"]
        paywall_status = link.get("paywall_status", "")
        if paywall_status == "paywalled":
            accessible_url = get_proreader_url(url)
        else:
            accessible_url = url
        results.append(
            {
                "id": link["id"],
                "url": url,
                "date_saved": link["date_saved"],
                "paywall_status": paywall_status,
                "accessible_url": accessible_url,
            }
        )
    return {"links": results}


# Register the router!
app.include_router(router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")
