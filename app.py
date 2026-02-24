from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from datetime import datetime
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


def _format_time(ts: str) -> str:
    if not ts:
        return ""
    try:
        # ts is stored as ISO string from datetime.now()
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%H:%M")
    except Exception:
        return ts


def _format_messages(messages):
    formatted = []
    for m in messages:
        sender, receiver, msg = m[:3]
        ts = m[3] if len(m) > 3 else ""
        formatted.append([sender, receiver, msg, _format_time(ts)])
    return formatted


# ---------------- CHAT ----------------
@app.get("/chat", response_class=HTMLResponse)
def chat(
    request: Request,
    email: str,
    peer: str | None = None
):
    base_users = [u for u in get_all_users() if u["email"] != email]

    # Attach last message preview and time per conversation
    users = []
    for u in base_users:
        convo_messages = get_private_chat(email, u["email"])
        last_text = ""
        last_time = ""
        if convo_messages:
            last = convo_messages[-1]
            last_text = last[2]
            ts = last[3] if len(last) > 3 else ""
            last_time = _format_time(ts)

        users.append({
            **u,
            "last_message": last_text,
            "last_time": last_time,
        })

    messages = []
    if peer:
        raw_messages = get_private_chat(email, peer)
        messages = _format_messages(raw_messages)

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


# ---------------- MESSAGES API (polling) ----------------
@app.get("/api/messages")
def api_messages(me: str, peer: str):
    """
    Lightweight JSON endpoint for polling messages between two users.
    """
    raw_messages = get_private_chat(me, peer)
    messages = _format_messages(raw_messages)
    return JSONResponse({"messages": messages})
