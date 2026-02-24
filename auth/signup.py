from sheets.users_repo import find_user_by_email, create_user


def signup_user(username: str, email: str, password: str):
    existing = find_user_by_email(email)
    if existing:
        return False

    create_user(username, email, password)
    return True
