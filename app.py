from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth.signup import signup_user
from auth.signin import signin_user
from sheets.users_repo import get_all_users
from sheets.messages_repo import save_message, get_private_chat

app = FastAPI()

# Static + templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ---------------- HOME ----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# ---------------- LOGIN ----------------
@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    user = signin_user(email, password)
    if not user:
        return RedirectResponse("/", status_code=302)

    return RedirectResponse(
        f"/chat?email={email}",
        status_code=302
    )


# ---------------- SIGNUP ----------------
@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup")
def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        success = signup_user(username, email, password)
        if success:
            return RedirectResponse("/?signup_success=1", status_code=302)
        else:
            return templates.TemplateResponse("signup.html", {
                "request": Request, 
                "error": "Email already registered. Try logging in."
            })
    except Exception as e:
        import traceback
        print(f"SIGNUP ERROR: {e}")
        return templates.TemplateResponse("signup.html", {
            "request": Request, 
            "error": f"Connection error: {str(e)}"
        })


# ---------------- CHAT ----------------
@app.get("/chat", response_class=HTMLResponse)
def chat(
    request: Request,
    email: str,
    peer: str | None = None
):
    users = [u for u in get_all_users() if u["email"] != email]

    messages = []
    if peer:
        messages = get_private_chat(email, peer)

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "email": email,
            "users": users,
            "messages": messages
        }
    )


# ---------------- SEND MESSAGE ----------------
@app.post("/send")
def send_message(
    sender: str = Form(...),
    receiver: str = Form(...),
    message: str = Form(...)
):
    save_message(sender, receiver, message)

    return RedirectResponse(
        f"/chat?email={sender}&peer={receiver}",
        status_code=302
    )
