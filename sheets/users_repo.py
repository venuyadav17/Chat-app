import uuid
import hashlib
from datetime import datetime
from sheets.client import get_sheet, SPREADSHEET_ID


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return _hash_password(password) == password_hash


def _read_all_users():
    result = get_sheet().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Users!A:E"
    ).execute()

    return result.get("values", [])


def find_user_by_email(email):
    rows = _read_all_users()

    for r in rows[1:]:
        if len(r) >= 4 and r[2] == email:
            return {
                "user_id": r[0],
                "username": r[1],
                "email": r[2],
                "password_hash": r[3],
            }
    return None


def create_user(username, email, password):
    password_hash = _hash_password(password)

    get_sheet().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Users!A:E",
        valueInputOption="RAW",
        body={
            "values": [[
                str(uuid.uuid4()),
                username,
                email,
                password_hash,
                str(datetime.now())
            ]]
        }
    ).execute()


def get_all_users():
    rows = _read_all_users()
    users = []

    for r in rows[1:]:
        if len(r) >= 3:
            users.append({
                "user_id": r[0],
                "username": r[1],
                "email": r[2]
            })
    return users
