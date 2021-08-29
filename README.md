[/]: https://joby-ev-chargers.glitch.me
[/sql]: https://joby-ev-chargers.glitch.me/sql
[/qry]: https://joby-ev-chargers.glitch.me/qry
[/render-qr-codes]: https://joby-ev-chargers.glitch.me/render-qr-codes
[/get-assign-charger-command/<charger_id>]: https://joby-ev-chargers.glitch.me/get-assign-charger-command/<charger_id>
[/slack/assign-charger]: https://joby-ev-chargers.glitch.me/slack/assign-charger

# Documentation

## Usage:

### Monitoring chargers:

- Using [/], [/qry], [/sql]: Users can monitor the states of all chargers at Joby.

### Assigning a Charger to Yourself:

If you are about to charge at a Joby EV charger, please follow these steps to let other Jobians know who to reach out to in case they need to get a hold of you.

1. Once parked next to a charger and plugged in, use your smartphone to scan the QR code next to charger name:
   ![alt text](https://cdn.glitch.com/b81dd1a0-835d-48d2-bf45-82e71d46b316%2Fqr-example.png?v=1629912254642)
2. Once Scanned the landing page should look like this:
   ![alt text](https://cdn.glitch.com/b81dd1a0-835d-48d2-bf45-82e71d46b316%2Fqr_landing_page.jpeg?v=1629667553686?raw=true)
3. Follow the instructions on the landing page by copying the command to your clipboard, then pasting in on any channel in slack (Don't worry, nothing will be actually posted to that channel).
4. If successful, you should see a message like this:
   ![alt text](https://cdn.glitch.com/b81dd1a0-835d-48d2-bf45-82e71d46b316%2FScreen%20Shot%202021-08-22%20at%202.38.18%20PM.png?v=1629668311016raw=true)
5. Your slack handle should now appear on the main landing page!
   ![alt text](https://cdn.glitch.com/b81dd1a0-835d-48d2-bf45-82e71d46b316%2FScreen%20Shot%202021-08-22%20at%202.39.29%20PM.png?v=1629668472844raw=true)

Slack handles will be automatically removed from the main landing page everyday at midnight.

## System architecture

![alt text](https://cdn.glitch.com/b81dd1a0-835d-48d2-bf45-82e71d46b316%2Fevchargerbot.png?v=1629665285656?raw=true)

## Available endpoints:

- [/]: Main landing page. Shows all charger states at Joby.
- [/sql]: Shows all charger states at the 980 office.
- [/qry]: Shows all charger states at the Santa Cruz offices.
- [/render-qr-codes]: Generate QR codes for all chargers at Joby. Each QR code, will lead to a page holding a slack command to use on slack in order to assign a specific charger to a user.
- [/get-assign-charger-command/<charger_id>]: Given a <charger_id>, this will return a page holding a slack command to use on slack in order to assign a specific charger to a user.
- [/slack/assign-charger]: Endpoint only accessible from slack and used assign a given charger to the user sending the assign-charger slack command.
