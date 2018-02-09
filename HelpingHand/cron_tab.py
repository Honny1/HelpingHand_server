from crontab import CronTab

cron = CronTab(tabfile='filename.tab')
job = cron.new(command='echo "123"')
job.minute.every(1)
cron.write()
