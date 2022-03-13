Import os
from apscheduler.schedulers.blocking import BlockingScheduler

TOKEN = os.environ.get("TOKEN")
#bot = telebot.TeleBot(TOKEN)
#bot.config['api_key'] = TOKEN
users = os.environ.get("Users") # allowed users.
allowed_chat_ids = users.split(",")
allowed_chat_ids = map(int, allowed_chat_ids)

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()
