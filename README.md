# tgtg
Notifications for TooGoodToGo
Sends notifications through email for when a store on TooGoodToGo restocks based on the stores that a user has favourited

- notify.py: the script that should be constantly running
- changeUsers.py: can be run to add or remove users (it sends the email that a new user would need to click on)
- info.py: has some constants, like the time between pinging the api (refresh_seconds) and the email and password to send emails
- users.json: stores the info about the users and is automatically updated when changeUsers.py is run
