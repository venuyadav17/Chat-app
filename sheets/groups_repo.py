import uuid
from sheets.client import get_sheet, SPREADSHEET_ID


def create_group(name, creator):
    gid = str(uuid.uuid4())

    get_sheet().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Groups!A:C",
        valueInputOption="RAW",
        body={"values": [[gid, name, creator]]}
    ).execute()

    add_member(gid, creator)
    return gid


def add_member(group_id, email):
    get_sheet().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="GroupMembers!A:B",
        valueInputOption="RAW",
        body={"values": [[group_id, email]]}
    ).execute()
