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
  message = text
  url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
  requests.get(url)
  return


def get_mmi():
  url = "https://www.tickertape.in/market-mood-index"
  content = requests.get(url).text
  soup = BeautifulSoup(content, 'html.parser')
  mmi = soup.find("span" , class_="jsx-1637443598 jsx-1556920289 number").get_text()
  return float(mmi)


def main():
  run_no = 0
  new_mmi = get_mmi()
  old_mmi = new_mmi
  in_id = 0
  out_id = 0
  while True:
    while today_now()[1].hour < 24 and today_now()[1].hour >= 9:
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
    if (today_now()[1].weekday() < 5):
      print("sleeping for 17 hrs")
      time.sleep(61200)
    else:
      print("sleeping for weekend")
      time.sleep(838800)
  return


keep_alive()
delta_change = 5.0
refresh_time = 3.0  # in minutes
target_value = 30.0
main()
