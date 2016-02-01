import sys
import dbservice


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
    if command == 'add-user':
        username = sys.argv[2]
        password = sys.argv[3]
        create_user(username, password)
    else:
        print(
            "Available commands are add-user")
        sys.exit()
