#!/bin/bash

echo "0 6 * * 1 root docker restart nginx-gunicorn-webserver" >> /etc/crontab
