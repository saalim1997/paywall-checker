from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .auth import get_current_user
from .db import add_link, get_links, init_db
from .paywall import is_accessible
from .utils import get_proreader_url

router = APIRouter()


@router.on_event("startup")
def startup_event():
    init_db()


class LinkRequest(BaseModel):
    url: str


@router.post("/links/")
def save_link(link: LinkRequest, user=Depends(get_current_user)):
    add_link(link.url, user["email"])
    return {"message": "Link saved", "url": link.url}


@router.post("/check/")
def check_links(user=Depends(get_current_user)):
    links = get_links(user["email"], status="paywalled")
    results = []
    for link in links:
        link_id = link["id"]
        url = link["url"]
        accessible = is_accessible(url)
        results.append({"id": link_id, "url": url, "accessible": accessible})
    return results


# # ------ Router Section ------
# router = APIRouter()


@router.get("/links/")
def list_links(user=Depends(get_current_user)):
    links = get_links(user["email"])
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
