from keep_alive import keep_alive
from bs4 import BeautifulSoup
import datetime
import pytz
import time
import requests
import random

def today_now():
  #Creates a file name with local india time
  India_local_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
  time_now = India_local_time.strftime("%Y-%m-%d %H:%M:%S")
  return [time_now, India_local_time]


def send_msg(text):
  TOKEN = "6165499133:AAEvdzvgwhTi13lfDEMSIXjmiaJTp5fC3uI"
  chat_id = "5752392578"
  chat_id2 = "865024459"
  message = text
  url1 = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
  requests.get(url1)
  url2 = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id2}&text={message}"
  requests.get(url2)
  return


def get_mmi():
  url = "https://www.tickertape.in/market-mood-index"
  content = requests.get(url).text
  soup = BeautifulSoup(content, 'html.parser')
  mmi = soup.find("span" , class_="jsx-1637443598 jsx-1556920289 number").get_text()
  return float(mmi)

def weekend_sleep():
  date_format_str = '%Y-%m-%d %H:%M:%S'
  now_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
  coming_monday = str((now_time + datetime.timedelta(days = (7-now_time.weekday()))).date())
  target_time = datetime.datetime.strptime(f"{coming_monday}"+" 09:00:00", date_format_str)
  naive = now_time.strftime(date_format_str)
  start = datetime.datetime.strptime(naive, date_format_str)
  end_date =   target_time
  diff = end_date - start
  tot_secs = diff.total_seconds()
  return (str(tot_secs),end_date.strftime(date_format_str))

def weekday_sleep():
  date_format_str = '%Y-%m-%d %H:%M:%S'
  now_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
  if(now_time.hour > 16):
    next_day = str((now_time + datetime.timedelta(days = 1)).date())
  else:
    next_day = str((now_time + datetime.timedelta(days = 0)).date())
  target_time = datetime.datetime.strptime(f"{next_day}"+" 09:00:00", date_format_str)
  naive = now_time.strftime(date_format_str)
  start = datetime.datetime.strptime(naive, date_format_str)
  end_date =   target_time
  diff = end_date - start
  tot_secs = diff.total_seconds()
  return (str(tot_secs),end_date.strftime(date_format_str))

def main():
  run_no = 0
  new_mmi = get_mmi()
  old_mmi = new_mmi
  in_id = 0
  out_id = 0
  while True:
    while today_now()[1].hour < 16 and today_now()[1].hour >= 9:
      print(f"run_no  {run_no}")
      print(f"new mmi is {new_mmi}")
      print(f"old mmi is {old_mmi}")
      lower_bound = old_mmi - delta_change
      print(f"Range lower bound is {lower_bound}")
      upper_bound = old_mmi + delta_change
      print(f"Range upper bound is {upper_bound}")

      if (new_mmi <= target_value):
        if (new_mmi <= lower_bound):
          send_msg(u"\u2705"+f"mmi reduced more than {delta_change} and value is {new_mmi}")
          old_mmi = new_mmi
        elif (new_mmi >= upper_bound):
          send_msg(u"\u274C"+f"&#10060 mmi increased more than {delta_change} and value is {new_mmi}")
          old_mmi = new_mmi
        elif (in_id == 0):
          send_msg(u"\u2705"+f"mmi is lower than {target_value} and value is {new_mmi}")
        in_id = 1
        out_id = 0
      elif (out_id == 0):
        send_msg(u"\u274C"+f"mmi is more than {target_value} and value is {new_mmi}")
        in_id = 0
        out_id = 1
        old_mmi = new_mmi

      time.sleep(refresh_time * 60)
      new_mmi = get_mmi()  #assigns the refreshed value
      run_no = run_no + 1
    if ( (today_now()[1].weekday()== 4 and today_now()[1].hour>=16) or (today_now()[1].weekday() > 4 ) ):
      send_msg(f"sleeping for {weekend_sleep()[0]} seconds now is weekend and starts at {weekend_sleep()[1]}")
      time.sleep(float(weekend_sleep()[0]))
      send_msg(f"bot started at {today_now()[0]}")
    else:
      send_msg(f"sleeping for {weekday_sleep()[0]} seconds now is weekday and starts at {weekday_sleep()[1]}")
      time.sleep(float(weekday_sleep()[0]))
      send_msg(f"bot started at {today_now()[0]}")
  return


keep_alive()
delta_change = 5.0
refresh_time = 3.0  # in minutes
target_value = 30.0
main()
