from flask import Flask
import os
import asyncio
import pyjuicenet
import aiohttp
from prettytable import PrettyTable
from pytz import timezone
import datetime

def tabulate_chargers_state(chargers, location):
  t = PrettyTable(['','Name', 'Status', 'Last Seen Online (PST)'])
  for charger in chargers:
    if charger.status == 'disconnect':
      symbol = '\U0001F6E0' #hammer and wrench   
    elif charger.status == 'charging':
      symbol = '\U000026A1' #bolt
    elif charger.status == 'standby':
      symbol = '\U00002705' # green circle
    elif charger.status == 'plugged':
      symbol = '\U0001F50C' # plug
    else:
      symbol = '❓'    
    date = datetime.datetime.utcfromtimestamp(charger.json_state['time_last_ping'])
    date_pst = date.astimezone(timezone('US/Pacific'))
    t.add_row([symbol, charger.name, charger.status, date_pst.strftime("%Y-%m-%d %H:%M:%S")])
  return f'<h1>{location}</h1>' + t.get_html_string() + "\n\n"

def create_charger_groups(chargers):
  location_to_chargers_map = {}
  for charger in chargers:
    location = get_location(charger.name)
    if location_to_chargers_map.get(location):
      location_to_chargers_map[location].append(charger)
    else:
      location_to_chargers_map[location] = []
      location_to_chargers_map[location].append(charger)
  return location_to_chargers_map

def get_location(str):
  end_of_location_index = str.find(' - ')
  return str[0:end_of_location_index]

async def get_chargers():
  async with aiohttp.ClientSession() as session:
    api = pyjuicenet.Api(os.environ['JUICENET_API_KEY'], session)
    devices = await api.get_devices()
    return devices

  
def print_chargers(keywords = None):
    charger_list = asyncio.run(get_chargers())
    location_to_chargers_map = create_charger_groups(charger_list)
    html = ""
    if keywords:
      for keyword in keywords:
        html += tabulate_chargers_state(location_to_chargers_map[keyword], keyword)
    else:
      for location in location_to_chargers_map:
        html += tabulate_chargers_state(location_to_chargers_map[location], location)
    return html
  
app = Flask(__name__)
 
@app.route("/")
def show_all_chargers():
  return print_chargers()
 
@app.route("/sql")
def show_sql_chargers():
  return print_chargers(['980'])

@app.route("/qry")
def show_qry_chargers():
  return print_chargers(['Penta-Taj', 'Joby Heights'])

app.run()