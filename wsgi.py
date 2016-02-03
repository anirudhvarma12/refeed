#!/usr/bin/env python
from main import app as application
import os
import sys

try:
    virtenv = os.path.join(
        os.environ.get('OPENSHIFT_PYTHON_DIR', '.'), 'virtenv')
    python_version = "python" + \
        str(sys.version_info[0]) + "." + str(sys.version_info[1])
    os.environ['PYTHON_EGG_CACHE'] = os.path.join(
        virtenv, 'lib', python_version, 'site-packages')
    virtualenv = os.path.join(virtenv, 'bin', 'activate_this.py')
    if(sys.version_info[0] < 3):
        exec(virtualenv, dict(__file__=virtualenv))
    else:
        exec(open(virtualenv).read(), dict(__file__=virtualenv))

except IOError:
    pass

# Below for testing locally only
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('0.0.0.0', 8080, application)
    httpd.serve_forever()
