#!/usr/bin/env bash
ps aux|grep uwsgi | awk '{print $2}'|xargs kill -9 || echo -n
source venv/bin/activate
mkdir -p Logs
uwsgi viewOJ_uwsgi.ini &
deactivate