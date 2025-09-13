import os

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

router = APIRouter()

# Configure OAuth
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    # Force HTTPS for Google OAuth
    redirect_uri = redirect_uri.replace("http://", "https://")
    print("Redirect URI:", redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/callback", name="auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        print("Token:", token)
        user = await oauth.google.parse_id_token(request, token)
        print("User:", user)
        # Store user info in session
        request.session["user"] = dict(user)
        return RedirectResponse("/")
    except Exception as e:
        print("OAuth callback error:", e)
        raise HTTPException(status_code=500, detail="OAuth callback failed")


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse("/")


def get_current_user(request: Request):
    user = request.session.get("user")
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


@router.get("/me")
async def me(user: dict = Depends(get_current_user)):
    return user
