import sys
import dbservice


def set_url(url):
    dbservice.set_main_url(url)
    print("saved")


def set_description(description):
    dbservice.set_description(description)
    print("saved")


def set_title(title):
    dbservice.set_title(title)
    print("saved")


def create_user(username, password):
    user = dbservice.get_user(username)
    if user is None:
        dbservice.add_user(username, password)
    else:
        print("User already exists")

if len(sys.argv) == 0:
    print("See usage details")
    sys.exit()
else:
    command = sys.argv[1]
    if command == 'set-url':
        url = sys.argv[2]
        set_url(url)
    elif command == 'set-description':
        desc = sys.argv[2]
        set_description(desc)
    elif command == 'set-title':
        set_title(sys.argv[2])
    elif command == 'add-user':
        username = sys.argv[2]
        password = sys.argv[3]
        create_user(username, password)
    else:
        print(
            "Available commands are set-url, set-description,set-title,add-user")
        sys.exit()
