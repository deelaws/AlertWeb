#!/usr/bin/env python
"""
This script runs the AlertWeb application using a development server.
"""

from os import environ
from AlertWeb import create_app

if __name__ == '__main__':
    app = create_app(environ.get('CONFIG_TYPE', 'production'))
    app.run()