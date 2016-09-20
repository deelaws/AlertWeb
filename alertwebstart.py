#!/usr/bin/env python
"""
This script runs the AlertWeb application using a development server.
"""

import os, sys, inspect

# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"AlertWeb")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

sys.path.insert(1, '.')

from AlertWeb import *

# performs migrations from current revision to head
#perform_migratons()

app = create_app(os.environ.get('CONFIG_TYPE', 'production'))

# Don't need this for Heroku
#app.run(debug=False, host='0.0.0.0', port=port)
