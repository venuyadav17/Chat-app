from sheets.users_repo import find_user_by_email, verify_password


def signin_user(email, password):
    user = find_user_by_email(email)

    if not user:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    return user
