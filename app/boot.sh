#!/bin/bash
exec gunicorn -b 0.0.0.0:5050 --access-logfile - --error-logfile - wsgi:app
