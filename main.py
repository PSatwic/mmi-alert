from keep_alive import keep_alive
from selenium import webdriver
import datetime
import pytz
import time
import requests

def start_driver():
  options = webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_argument("disable-blink-features=AutomationControlled")
  #Starting driver
  driver = webdriver.Chrome(options=options)
  driver.get("https://www.tickertape.in/market-mood-index")
  return driver

def today_now():
  #Creates a file name with local india time
  India_local_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
  time_now = India_local_time.strftime("%Y-%m-%d %H:%M:%S")
  return [time_now,India_local_time]

def send_msg(text):
  TOKEN = "6165499133:AAEvdzvgwhTi13lfDEMSIXjmiaJTp5fC3uI"
  chat_id = "5752392578"
  message = text
  url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
  requests.get(url)
  return

def get_mmi(driver):
  time.sleep(2) #wait to load the data
  element = driver.find_element(by="xpath",value="/html/body/div/div[3]/div/div[1]/div[1]/div/div[2]/span")
  return float(element.text)


def main():
  driver = start_driver()
  run_no = 0
  new_mmi = get_mmi(driver)
  old_mmi = new_mmi
  in_id = 0
  out_id = 0
  while True:
    while today_now()[1].hour < 16 and today_now()[1].hour >= 9:
      print(f"run_no  {run_no}")
      print(f"new mmi is {new_mmi}")
      print(f"old mmi is {old_mmi}")
      lower_bound = old_mmi-delta_change
      print(f"Range lower bound is {lower_bound}")
      upper_bound = old_mmi+delta_change
      print(f"Range upper bound is {upper_bound}")
  
      if(new_mmi <= target_value):
        if(new_mmi<=lower_bound):
          send_msg(f"mmi reduced more than {delta_change} and value is {new_mmi}")
        elif (new_mmi>=upper_bound):
          send_msg(f"mmi increased more than {delta_change} and value is {new_mmi}")
        elif(in_id == 0):
          send_msg(f"mmi is lower than {target_value} and value is {new_mmi}")
        old_mmi = new_mmi
        in_id = 1
        out_id = 0
      elif (out_id == 0):
        send_msg(f"mmi is more than {target_value} and value is {new_mmi}")
        in_id = 0
        out_id = 1
        old_mmi = new_mmi
        
      time.sleep(refresh_time*60)
      driver.get(driver.current_url)  # refreshes the page
      new_mmi = get_mmi(driver) #assigns the refreshed value
      run_no = run_no+1
  if(today_now()[1].weekday() < 5 ):
    time.sleep(61200)
  else:
    time.sleep(838800)
  return

keep_alive()
delta_change = 0.1
refresh_time = 3.0 # in minutes
target_value = 30.0
main()

