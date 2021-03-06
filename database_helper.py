import yaml
import os
import datetime
from pytz import timezone
import juicenet_helper
import asyncio
import pytz

def load_database():
  yml = {}
  try:
    with open(os.environ['DATABASE'], 'r') as file:
      yml = yaml.safe_load(file)
      if not yml:
        # in case the yaml is empty
        yml = dict()
  except Exception as e:
    print(e)
  return yml

def write_database(yml):
  write_success = True;
  try:
    if yml:
      with open(os.environ['DATABASE'], 'w') as file:
        yaml.dump(yml, file)
    else:
      # attemped to write an empty yaml
      write_success = false
  except Exception as e:
    write_success = False
    print(e)
  return write_success
  
def assign_driver(slack_user, charger_id):
  success = False
  charger_name = None
  yml = load_database()
  if yml:
    charger_info = yml.get(charger_id)
    if charger_info:
      charger_info['user_slack_id'] = slack_user
      last_assigned_time_stamp_pst_string = get_current_time_in_pst_string()
      charger_info['last_assigned_time_stamp_pst'] = last_assigned_time_stamp_pst_string
      charger_name = charger_info['name']
      yml.update({charger_id: charger_info})
      write_database(yml)
      success = True
    else:
      print(f"Charger {charger_id} not found")
  else:
    print("Unable to load yaml.")
  return success, charger_name

def update_chargers():
    #load database
    yml = load_database()
    chargers =  asyncio.run(juicenet_helper.get_chargers())
    for charger in chargers:
      # cleanup the time
      last_time_ping = datetime.datetime.utcfromtimestamp(charger.json_state['time_last_ping'])
      last_time_ping_pst = last_time_ping.astimezone(timezone('US/Pacific'))
      if (yml.get(charger.id)):
        #charger already exists, update the charger fields
        charger_info = yml.get(charger.id)
        charger_info['last_seen_online_pst'] = last_time_ping_pst.strftime("%Y-%m-%d %H:%M:%S")
        charger_info['name'] = charger.name
        charger_info["location"] = get_location(charger.name)
        charger_info["status"] = charger.status
        if should_reset_assigned_user(datetime.datetime.strptime(charger_info['last_assigned_time_stamp_pst'], "%Y-%m-%d %H:%M:%S")):
          charger_info['user_slack_id'] = ''

                
      else:
        # create new charger entry
        charger_info = {
            'last_seen_online_pst': last_time_ping_pst.strftime("%Y-%m-%d %H:%M:%S"),
            'last_assigned_time_stamp_pst': last_time_ping_pst.strftime("%Y-%m-%d %H:%M:%S"),
            'name': charger.name,
            'location': get_location(charger.name),
            'status': charger.status,
            'user_slack_id': ''
        }
        
      # update yaml
      yml.update({charger.id: charger_info})

    write_database(yml)

def get_location(str):
  end_of_location_index = str.find(' - ')
  return str[0:end_of_location_index]

def should_reset_assigned_user(last_assigned_time_stamp_pst_datetime):
  # Will reset the assigned user when a new day starts
  threshold = last_assigned_time_stamp_pst_datetime.astimezone(timezone('US/Pacific')).replace(hour=23, minute=59, second=59)
  reset = get_current_time_in_pst_datetime() > threshold
  return reset

def get_current_time_in_pst_datetime():
  return datetime.datetime.utcnow().astimezone(timezone('US/Pacific'))

def get_current_time_in_pst_string():
  return get_current_time_in_pst_datetime().strftime("%Y-%m-%d %H:%M:%S")



