sessions = {}

def create_session(user):
    sessions[user["user_id"]] = user
    return user["session_token"]

def get_user_by_session(session_token):
    for user in sessions.values():
        if user["session_token"] == session_token:
            return user
    return None
