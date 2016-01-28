import dbservice


def check_password(pwd, confirm_pwd):
    return pwd == confirm_pwd


def setup():
    print("Welcome to onetime setup for Re-feed.")
    print("Please enter admin id")
    username = input()
    print("Enter admin password")
    password = input()
    print("Confirm password")
    confirm_pwd = input()
    if check_password(password, confirm_pwd):
        print("passwords match, creating user")
        dbservice.create_db()
        dbservice.add_user(username, password)
    else:
        print("Passwords do not match")
        setup()

setup()
