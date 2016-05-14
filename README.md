Refeed is a small webapp for groups to come together and curate a stream of content for others to consume. Re-feed provides a web interface to add links then generates an RSS out of that which can be consumed easily by any RSS reader out there.

# Installation
First run onetime.py to create the schema and admin account

## Settings.py
Set options for your installation here
* `title` = The main title for your feed.
* `description` = The description for your feed.
* `main_url` = The main URL for your feed
* `db_path` = The path to store your db file.
*  [Optional] `slack_token` = The Slack generated token which would be used for verification.
*  [Optional] `slack_user` = The user name of the user to be used to store links added via the slash command in slack. You should use an already existing user for this. See `Manage.py` for adding users


## Manage.py
manage.py is for managing the current installation. commands - 
* `add-user`: Add a new user who can add links.
   
  `Usage - python manage.py add-user username password`

## Refeed-Slack Command
Refeed now supports [Slash Commands](https://get.slack.help/hc/en-us/articles/201259356-Using-slash-commands) in Slack.
To configure slack and refeed follow these steps -
* Add `slack_user` in settings.py
* With the help of [this](https://get.slack.help/hc/en-us/articles/201259356-Using-slash-commands) link, get to the configuration page of the slack command. You can name the command as per your wish
* In the URL section, add `/slack` to the end of the url of your refeed installation. Eg. If the installation is @ `www.myrefeed.com`, the url would be `www.myrefeed.com/slack`.
* In the method section, select `POST`
* Copy the token and set it to `slack_token` of settings.py

The `Slash command` supports 2 actions - 
* `add`: Add a new article. 
  Syntax
  `/mycommand add www.mylink.com` where `mycommand` is the name you set in step 2 above.

   ![Add command](http://i.imgur.com/nHFRjj8.png)
* `random` : Get a random article to read
  Syntax
  `/mycommand random` where `mycommand` is the name you set in step 2 above.
   ![Get an article to read](http://i.imgur.com/DOh8EnI.png)

# Run
python main.py
localhost:5000
