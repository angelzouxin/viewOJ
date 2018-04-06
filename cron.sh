cd `dirname $0`
source venv/bin/activate
mkdir -p Logs
(python3 cron_job.py || echo fail >> Logs/crawler.log) && date >> Logs/crawler.log
