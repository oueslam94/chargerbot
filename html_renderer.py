
from prettytable import PrettyTable
import juicenet_helper
import database_helper
import qrcode
import base64



def tabulate_chargers_state(chargers, location):
  t = PrettyTable(['','Name', 'Status', 'Last Seen Online (PST)', 'User'], tablefmt="fancy_grid")
  for charger in chargers:
    if charger['status'] == 'disconnect':
      symbol = '\U0001F6E0' #hammer and wrench   
    elif charger['status'] == 'charging':
      symbol = '\U000026A1' #bolt
    elif charger['status'] == 'standby':
      symbol = '\U00002705' # green circle
    elif charger['status'] == 'plugged':
      symbol = '\U0001F50C' # plug
    else:
      symbol = '❓'
    t.add_row([symbol, charger['name'], charger['status'], charger['last_seen_online_pst'], charger['user_slack_id']])
  return t

def tabulate_chargers_state_html(chargers, location):
  t = tabulate_chargers_state(chargers, location)
  return f'<h1>{location}</h1>' + t.get_html_string() + "\n\n"

def create_charger_groups(database):
  location_to_chargers_map = {}
  for charger_id, charger_info in database.items():
    location = charger_info['location']
    if location_to_chargers_map.get(location):
      location_to_chargers_map[location].append(charger_info)
    else:
      location_to_chargers_map[location] = []
      location_to_chargers_map[location].append(charger_info)
  return location_to_chargers_map

def get_location(str):
  end_of_location_index = str.find(' - ')
  return str[0:end_of_location_index]

def print_chargers(keywords = None):
    yml = database_helper.load_database()
    location_to_chargers_map = create_charger_groups(yml)
    html = ""
    if keywords:
      for keyword in keywords:
        html += tabulate_chargers_state_html(location_to_chargers_map[keyword], keyword)
    else:
      for location in location_to_chargers_map:
        html += tabulate_chargers_state_html(location_to_chargers_map[location], location)
    return html

def generate_assign_charger_text(charger_id):
  yml = database_helper.load_database()
  html = ""
  if yml:
    charger = yml.get(charger_id)
    if charger:
      # Add the html components
      html +=f"""
      <div>
           <h1>To get assigned {charger['name']}, please follow these steps:</h1>
           <h2> 1) Copy this command:</h2>
           <input type="text" value="/assign-charger {charger_id}" id="copyMe">
           <button onclick="copyMyText()">Copy To Clipboard</button>
           <h2> 2) Now go to Slack and paste it in any DM/Channel:</h2>
           <form action="slack://open">
           <input type="submit" value="Open Slack App" />
           </form>

      </div>"""
      # Add the script to copy to clipboard
      html +="""
      <script>
      function copyMyText() {
           //select the element with the id "copyMe", must be a text box
           var textToCopy = document.getElementById("copyMe");
           //select the text in the text box
           textToCopy.select();
           //copy the text to the clipboard
           document.execCommand("copy");
      }
      </script>
      """
    else:
      html += f"Hmm, we could not find a charger with the ID: {charger_id} :("
  return html

def generate_and_save_qr_code(root_url):
  endpoint = root_url + 'get-assign-charger-command/'
  yml = database_helper.load_database()
  if yml:
    for charger_id, charger_info in yml.items():
      #Creating an instance of qrcode
      qr = qrcode.QRCode(
              version=1,
              box_size=10,
              border=5)
      link_to_encode = endpoint + charger_id
      qr.add_data(link_to_encode)
      qr.make(fit=True)
      img = qr.make_image(fill='black', back_color='white')
      img.save(f"qr/{charger_id}.png")

def qr_codes_to_html():
    yml = database_helper.load_database()
    html = ""
    if yml:
      for charger_id, charger_info in yml.items():
        name = charger_info['name']
        html += f'\n <h1>Name: {name}, ID: {charger_id}</h1> \n'
        data_uri = base64.b64encode(open(f'qr/{charger_id}.png', 'rb').read()).decode('utf-8')
        img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
        html += img_tag
    return html

