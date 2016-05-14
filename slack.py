from flask import jsonify
from urllib.parse import urlparse
import rss


def get_response(text):
    return jsonify({'text': text})


def split(command):
    return str(command).split(" ")


def get_help():
    text = "Your Re-Feed command was incomplete. Use `add <url> <title (optional)>` to add a url or `latest` to get the newest article or `list` to get a list of 10 recent articles"
    return get_response(text)


def get_from_array(array, index):
    if index < len(array):
        return array[index]
    return None


def check_url(url):
    parsed = urlparse(url)
    if parsed.scheme is None or parsed.scheme != "http:":
        return False
    return True


def add_item(components, user):
    url = get_from_array(components, 2)
    title = get_from_array(components, 3)
    if url is None:
        return get_response("Error: No URL Found")
    else:
        if check_url(url):
            try:
                result = rss.add_artcle(url, title, "", user)
                if result == rss.STATUS_OK:
                    return get_response('Successfully added Article @ ' + url)
                elif result == rss.STATUS_EXISTS:
                    return get_response("Error: Article was added less than 7 days ago")
            except:
                return get_response('Error: Could not save URL.')
        else:
            return get_response("Error: Invalid URL")


def execute_command(command, user):
    components = split(command)
    if len(components) == 0:
        return get_help()
    function = get_from_array(components, 1)
    if function is None:
        return get_help()
    elif function == "add":
        return add_item(components, user)
