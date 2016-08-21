#!/usr/bin/env python
"""
This script runs the AlertWeb application using a development server.
"""

import os, sys, inspect

# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"AlertWeb")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from AlertWeb import create_app

if __name__ == '__main__':
    app = create_app(environ.get('CONFIG_TYPE', 'production'))
    app.run()