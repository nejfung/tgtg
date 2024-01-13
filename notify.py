from tgtg import TgtgClient
from tgtg.exceptions import TgtgAPIError

import schedule
import time
from datetime import datetime
from datetime import timedelta

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from info import *
import json

# set up users
try:
    with open("users.json", "r") as file:
        users = json.load(file)
except FileNotFoundError:
    pass  # File not found

for i in range (len(users)):
    client = TgtgClient(access_token=users[i]['access_token'], refresh_token=users[i]['refresh_token'], user_id=users[i]['user_id'], cookie=users[i]['cookie'])
    clients.append(client)
    items = client.get_items()
    try:
        items = clients[i].get_items()
    except TgtgAPIError as e:
        print(f"Received error {users[i]['name']}. Retrying...")
        continue  # Skip to the next user
    all_items.append(items)

def job():
    global all_items, last_email_time

    # store old items and get new items
    for j in range(len(users)):
        old_items = all_items[j]
        try:
            items = clients[j].get_items()
        except TgtgAPIError as e:
            print(f"Received error {users[j]['name']}. Retrying...")
            continue  # Skip to the next user

        all_items[j]=items

        if(len(items) != len(old_items)):
            break

        for i in range(len(items)):
            # if the number of bags used to be 0 and is not 0 anymore
            if(old_items[i]['items_available'] == 0 and items[i]['items_available'] != 0 and old_items[i]['store']['store_id'] == items[i]['store']['store_id']):

                # get info about the store/bag
                store_name = items[i]['store']['store_name']
                items_available = items[i]['items_available']
                price = items[i]['item']['price_excluding_taxes']['minor_units'] / (pow(10,items[i]['item']['price_excluding_taxes']['decimals']))
                item_id = items[i]['item']['item_id']

                pickup_start = datetime.strptime(items[i]['pickup_interval']['start'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC).astimezone(pacific_timezone).strftime("%I:%M %p")
                pickup_end = datetime.strptime(items[i]['pickup_interval']['end'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC).astimezone(pacific_timezone).strftime("%I:%M %p")
                location = items[i]['pickup_location']['address']['address_line']

                bag = "bags" if items_available != 1 else "bag"
                
                # set up the message to send
                message = MIMEMultipart()
                message["To"] = users[j]["email"]
                message["From"] = sender_email
                subject_line = "TooGoodToGo - " + store_name
                message["Subject"] = subject_line

                # attatch message
                html = html_template.format(store_name=store_name, item_id=item_id, items_available=items_available, price=price, pickup_start=pickup_start, pickup_end=pickup_end, location=location, bag=bag)
                message.attach(MIMEText(html, "html"))

                # send the email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, users[j]["email"], message.as_string())

                # print to console
                print("[",datetime.now(),"][",users[j]["name"],"]",store_name,": ",items_available," ",bag," at ",price)

schedule.every(refresh_seconds).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)