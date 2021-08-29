from flask import abort, Flask, jsonify, request
import os
import asyncio
import pyjuicenet
import aiohttp
from prettytable import PrettyTable
from pytz import timezone
import datetime
import requests
import database_helper
import html_renderer

  
app = Flask(__name__)

@app.route("/")
def show_all_chargers():
  database_helper.update_chargers()
  return html_renderer.print_chargers()
 
@app.route("/sql")
def show_sql_chargers():
  database_helper.update_chargers()
  return html_renderer.print_chargers(['980'])

@app.route("/qry")
def show_qry_chargers():
  database_helper.update_chargers()
  return html_renderer.print_chargers(['Penta-Taj', 'Joby Heights'])

@app.route("/render-qr-codes")
def render_qr_codes():
  # will produce a QR code for all chargers in the database
  html_renderer.generate_and_save_qr_code(request.url_root)
  return html_renderer.qr_codes_to_html()

@app.route("/get-assign-charger-command/<charger_id>")
def get_assign_charger_command(charger_id):
  # will return the command to type into slack. 
  # we should get here after scanning a QR code
  return html_renderer.generate_assign_charger_text(charger_id)

# Slack handler
@app.route("/slack/assign-charger", methods=['POST'])
def assign_charger():
    team_id, token = request.form.get("team_id"), request.form.get("token")
    request_is_valid = validate_request(team_id, token)
    response = "Hmm...something went wrong."

    if request_is_valid:
      user = request.form.get("user_name")
      charger_id = request.form.get("text")

      if (user and charger_id):
        success, charger_name = database_helper.assign_driver(user, charger_id)
        if success:
          response = f"@{user}, you have been assigned {charger_name}. Find more information about other Joby chargers here: {request.url_root}!"
    return jsonify(
      response_type='ephemeral',
      text=response)

def validate_request(team_id, token):
  request_valid = False
  if team_id == os.environ['TEAM_ID'] and token == os.environ['SLACK_VERIFICATION_TOKEN']:
    request_valid = True
  else:
    print(f"Request with Team ID: {team_id} and token {token} is not valid.")
  return request_valid

app.run()

