'''
 Users online will be always random number between 100-300
And once new user is online it will count +1 to the counter 

New orders (per 24h)
Will be always counter between 10-80 random number 
Any new order will count +1 to the counter

Total orders, the base will start from 1000 and each 24h will join more orders between 10-80 by the section "new orders" Any new order will count +1 to the counter
'''
import random
import json
import threading
import datetime
from datetime import timezone

WAIT_SECONDS = 300 # loop every 5 minutes

def update():
    with open("/var/www/html/ssm/numbers.json", "r") as read_file:
        data = json.load(read_file)

    from datetime import date

    today = date.today()
    day = today.strftime("%d")

    if data['day'] != day: # day change happened
        data['day'] = day
        data['new_orders'] = 0

    increment = random.randint(1, 3)
    data['total_orders'] += increment
    data['new_orders'] += increment

    data['users_online'] = random.randint(100,300)

    with open("/var/www/html/ssm/numbers.json", "w") as write_file:
        json.dump(data, write_file)

    threading.Timer(WAIT_SECONDS, update).start()
    
update()
