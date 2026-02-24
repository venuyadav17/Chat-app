from datetime import datetime
from sheets.client import get_sheet, SPREADSHEET_ID


def save_message(sender, receiver, message):
    get_sheet().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Messages!A:D",
        valueInputOption="RAW",
        body={
            "values": [[sender, receiver, message, str(datetime.now())]]
        }
    ).execute()


def get_private_chat(user1, user2):
    result = get_sheet().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Messages!A:D"
    ).execute()

    rows = result.get("values", [])

    messages = []
    for r in rows:
        if len(r) < 3:
            continue

        sender, receiver, msg = r[:3]
        ts = r[3] if len(r) > 3 else ""

        if (
            sender == user1 and receiver == user2
        ) or (
            sender == user2 and receiver == user1
        ):
            messages.append([sender, receiver, msg, ts])

    return messages
