Refeed is a small webapp for groups to come together and curate a stream of content for others to consume. Re-feed provides a web interface to add links then generates an RSS out of that which can be consumed easily by any RSS reader out there.

# Installation
First run onetime.py to create the schema and admin account

## Settings.py
Set options for your installation here
* `title` = The main title for your feed.
* `description` = The description for your feed.
* `main_url` = The main URL for your feed
* `db_path` = The path to store your db file.

## Manage.py
manage.py is for managing the current installation. commands - 
* `add-user`: Add a new user who can add links.
** Usage - python manage.py add-user username password

# Run
python main.py
localhost:5000