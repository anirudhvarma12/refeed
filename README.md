# Installation
First run setup.py to create the schema and admin account

## Manage.py
manage.py is for managing the current installation. commands - 
* `set-url`: Sets the URL for the feed.
** Usage - python manage.py set-url http://myurl.com
* `set-description`: Sets the description of the feed
** Usage - python manage.py set-description "This feed is awesome"
* `set-title`: Sets the title of the feed
** Usage - python manage.py set-title "My Awesome feed"
* `add-user`: Add a new user who can add links.
** Usage - python manage.py add-user username password

# Run
python main.py
localhost:5000