mkdir -p Logs
source venv/bin/activate
(python3 cron_job.py || echo fail >> Logs/crawel.log) && date >> Logs/crawel.log
