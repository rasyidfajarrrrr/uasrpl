# group_monitor
Simple web app to manage groups and show participants on monitors.

A nice explanation how to use a Raspberry Pi for Digital Signage can be found here: https://www.heise.de/select/ct/2022/12/2204109513141146830.

## Usage
Install all requirements before first use:

    pip install flask faker Flask-HTTPAuth

To start the web app with the internal web server of Flask:

    FLASK_ENV=development flask run

Or run the Python script directly:

    python gm.py

## Requirements
* flask
* Flask-HTTPAuth
* faker
