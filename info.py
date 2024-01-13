import pytz

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "" # Email address to send notifications from
password = "" # Email password

pacific_timezone = pytz.timezone('America/Los_Angeles') # change for different timezones

# email template
html_template = """\
    <html>
    <body>
        <p><a href = "http://share.toogoodtogo.com/item/{item_id}" > {store_name}: </a> <br> 
        {items_available} {bag} for ${price} <br>
        Pickup from {pickup_start} to {pickup_end} at <a href = "https://google.com/maps/search/{location}">{location}</a>
        </p>
    </body>
    </html>
    """

refresh_seconds = 60

clients = []
all_items = []
last_email_time = {}
users = {}