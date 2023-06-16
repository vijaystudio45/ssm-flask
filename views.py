import time
import requests
import json

from unicodedata import category
from bcrypt import os
from pytz_deprecation_shim import UTC

from flask import render_template
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt, get_jwt_identity
from models.service import ServiceModel
from models.user import UserModel
from models.wallet import WalletModel
from models.orderhistory import OrderHistory

from services_source_update import i_fix_lookup
print(i_fix_lookup)

def normalize_text(text):
    # Normalizes the text (removes utf8 trash)
    with open('/var/www/html/ssm/normalized.json') as json_file:
        normalized = json.load(json_file)
        
        r = ""
        for c in text:  
            f = False
            for key, value in normalized.items():
                if c in value:
                    r += key
                    f = True
                    break
            if not f:
                r += c
    return r

ADMINLIST = [1] # CANT IMPORT FROM APP (should find a solution for that)

def get_stats_numbers():
    users_online=0
    new_orders=0
    total_orders=0

    with open('numbers.json', 'r') as read_file:
        data = json.load(read_file)
        users_online=data['users_online']
        new_orders=data['new_orders']
        total_orders=data['total_orders']

    return users_online,new_orders,total_orders

def index():
    return render_template("index.html")


def signup():
    return render_template("register.html")


@jwt_required()
def new_order_advanced():

    all_services = ServiceModel.find_all()
    user = UserModel.find_by_id(get_jwt_identity())
    wallet = WalletModel.find_by_user(get_jwt_identity())
    funds = 0
    if wallet != None:
        funds = round(wallet.funds, 3)

    categories = {}
    for service in all_services:
        if service.category not in categories:
            categories[service.category] = []
        else:
            categories[service.category].append(service)
    print(categories)
    admin = False
    if get_jwt_identity() in ADMINLIST:
        admin = True

    search_terms = ServiceModel.execute_query(
        f"SELECT DISTINCT category FROM services"
    )

    print(categories)
    return render_template(
        "new_order_advanced.html",
        categories=categories,
        search_terms=search_terms,
        logged_in=True,
        username=user.username,
        funds=funds,
        timestamp=time.time(),
        admin=admin,
    )



@jwt_required(optional=True)
def _test(service_name):
    all_services = ServiceModel.find_all()
    user = None
    wallet = None
    try:
        user = UserModel.find_by_id(get_jwt_identity())
        wallet = WalletModel.find_by_user(get_jwt_identity())
    except:
        pass
    funds = 0
    if wallet != None:
        funds = round(wallet.funds, 3)
    categories = {}
    for service in all_services:
        if service.category not in categories:
            categories[service.category] = []
        else:
            categories[service.category].append(service)

    admin = False
    logged_in = False
    user_identity = get_jwt_identity()
    if user_identity:
        logged_in = True
        if user_identity in ADMINLIST:  
            admin = True

    username = "Not logged in"
    if get_jwt() != {}:
        username = user.username


    search_terms = ServiceModel.execute_query(
        f"SELECT DISTINCT category FROM services"
    )

    media_services = ServiceModel.execute_query(
        f"SELECT category, rate FROM services WHERE category LIKE '%{service_name}%' GROUP BY category ORDER BY rate"
    )

    media_services = [(str(x[0]), x[1], str(x[0]).replace(service_name, "").replace("|", "")) for x in media_services]

    if "instagram" in service_name.lower():
        service_logo_path = "icon_instagram.webp"
        service_groups = [["Likes"], ["Followers"], ["Comments", "Comment"], ["Reels / Views / Engagement", "Reel", "View", "IGTV"], ["Other (Country Specific)", "Country"]]

    elif "facebook" in service_name.lower():
        service_logo_path = "icon_facebook.webp"
        service_groups = [["Likes"], ["Friend requests", "Friend Request"], ["Comments", "Comment"], ["Video views / Shares", "Video", "View", "Share"], ["Other (Country Specific)", "Country"]]


    elif "linkedin" in service_name.lower():
        service_logo_path = "icon_telegram.webp"
        service_groups = [["Likes"], ["Friend requests", "Friend Request"], ["Comments", "Comment"], ["Video views", "Video", "View"], ["Other (Country Specific)", "Country"]]

    elif "telegram" in service_name.lower():
        service_logo_path = "icon_telegram.webp"
        service_groups = [["Reactions"], ["Members"], ["Comments / Mass DM", "Comment", "DM"], ["Views / Shares", "View", "Share"], ["Other (Country Specific)", "Country"]]

    elif "twitter" in service_name.lower():
        service_logo_path = "icon_twitter.webp"
        service_groups = [["Likes", "Like", ], ["Members"], ["Comments / Mass DM", "Comment", "DM"], ["Views / Retweets", "View", "Retweet"], ["Other (Country Specific)", "Country"]]

    elif "tiktok" in service_name.lower():
        service_logo_path = "icon_tiktok.webp"
        service_groups = [["Likes", "Like"], ["Followers", "Follower"], ["Comments", "Comment"], ["Views / Shares / Saves", "View", "Share", "Save"], ["Other (Country Specific)", "Country"]]

    elif "youtube" in service_name.lower():
        service_logo_path = "icon_youtube.webp"
        service_groups = [["Likes", "Like"], ["Subscribers", "Subscribe"], ["Comments", "Comment"], ["Views / Watchtime", "View", "Watch"], ["Other (Country Specific)", "Country"]]

    return render_template(
        "new_order_service.html",
        service_name=service_name,
        categories=categories,
        search_terms=search_terms,
        service_groups=service_groups,
        media_services=media_services,
        service_logo_path=service_logo_path,
        logged_in=logged_in,
        username=username,
        funds=funds,
        timestamp=time.time(),
        admin=admin,
    )

@jwt_required(optional=True)
def add_order():
    all_services = ServiceModel.find_all()
    user = None
    wallet = None
    try:
        user = UserModel.find_by_id(get_jwt_identity())
        wallet = WalletModel.find_by_user(get_jwt_identity())
    except:
        pass
    funds = 0
    if wallet != None:
        funds = round(wallet.funds, 3)
    categories = {}
    for service in all_services:
        if service.category not in categories:
            categories[service.category] = []
        else:
            categories[service.category].append(service)

    admin = False
    logged_in = False
    user_identity = get_jwt_identity()
    if user_identity:
        logged_in = True
        if user_identity in ADMINLIST:  
            admin = True

    username = "Not logged in"
    if get_jwt() != {}:
        username = user.username


    search_terms = ServiceModel.execute_query(
        f"SELECT DISTINCT category FROM services"
    )

    return render_template(
        "new_order.html",
        categories=categories,
        search_terms=search_terms,
        logged_in=logged_in,
        username=username,
        funds=funds,
        timestamp=time.time(),
        admin=admin,
    )

@jwt_required()
def mass_update(site):
    print(" >>> MASS UPDATE has been requested. Setting on the maintenance mode")
    global MAINTENANCE
    # Enabling maintenance so noone can submit new tasks.
    MAINTENANCE = True

    url = "https://spiderpanel.com/api/v2"
    key = "0ff95bb78fd927a8750f6c2cda1442dd"  #TODO: SHOULD REMOVE FROM HERE

    params = {"key": key, "action": "services"}

    resp = requests.post(url, params=params)
    data = resp.json()

    ServiceModel.execute_query("DELETE FROM Services;")
    num = 0
    print(f"Found {len(data)} services. Looping...") 

    for i in data:
        num += 1 
        id = int(i["service"])
        name = normalize_text(i["name"])
        type = normalize_text(i["type"])
        rate = float(i["rate"])
        min = int(i["min"])
        max = int(i["max"])
        dripfeed = i["dripfeed"]
        refill = i["refill"]
        category = normalize_text(i["category"])
        enabled = True
        
        
        service = ServiceModel(id, name, type, rate, min, max, dripfeed, refill, category)
        print(service.type)
        if type in ["Subscriptions","Invites from Groups","Comment Replies",
            "Custom Comments Package","Mentions Hashtag","Mentions Custom List","Mentions Hashtag","Mentions with Hashtags", "Package"]:
            service.enabled = False
            print("Disabling")
        service.rate = service.base_rate * 1.2 # 20% price increase

        for wrong, correct in i_fix_lookup.items():
            if wrong in service.name:
                service.name = service.name.replace(wrong, correct)
                print(f"Found {wrong}, replacing with {correct} => {service.name}")
            if wrong in service.category:
                service.category = service.category.replace(wrong, correct)
                print(f"Found {wrong}, replacing with {correct} => {service.category}")

            
        service.save_to_db()

    ServiceModel.execute_query("UPDATE services SET category=replace(category,'/','')")
    print(f"Done adding services, updated (added): {num} services")

    MAINTENANCE = False
    return {"Message": f"Completed mass update, updated (added): {num} services"}, 200

@jwt_required(optional=True)
def add_order_service(service_name):
    user = None
    wallet = None
    try:
        user = UserModel.find_by_id(get_jwt_identity())
        wallet = WalletModel.find_by_user(get_jwt_identity())
    except:
        pass
    funds = 0
    if wallet != None:
        funds = round(wallet.funds, 3)
    service_logo_path = ""
    if ';' in service_name or '-' in service_name or '?' in service_name or '%' in service_name:
        return {"Message": "nice try"}

    print(service_name)
    if "instagram" in service_name.lower():
        service_logo_path = "Instagram-Logo.webp"

    elif "facebook" in service_name.lower():
        service_logo_path = "Facebook-Logo.webp"

    elif "linkedin" in service_name.lower():
        service_logo_path = "LinkedIn-Logo.webp"

    elif "telegram" in service_name.lower():
        service_logo_path = "Telegram.svg"
    
    elif "twitter" in service_name.lower():
        service_logo_path = "Twitter.webp"

    elif "tiktok" in service_name.lower():
        service_logo_path = "TikTok_Icon_Black_Square.webp"

    elif "youtube" in service_name.lower():
        service_logo_path = "YouTube-Logo.webp"

    media_services = ServiceModel.execute_query(
        f"SELECT category,rate FROM services WHERE category LIKE '%{service_name}%' GROUP BY category ORDER BY rate"
    )

    media_services = [(str(x[0]).replace(service_name, ""), x[1]) for x in media_services]

    admin = False
    if get_jwt_identity() in ADMINLIST:
        admin = True
    username = "Not logged in"
    if get_jwt() != {}:
        username = user.username

    
    search_terms = ServiceModel.execute_query(
        f"SELECT DISTINCT category FROM services"
    )

    return render_template(
        "new_order_service.html",
        service_logo_path=service_logo_path,
        search_terms=search_terms,
        media_services=media_services,
        service_name=service_name,
        logged_in=True,
        username=username,
        funds=funds,
        timestamp=time.time(),
        admin=admin,
    )


@jwt_required(optional= True)
def service_details(service_name, category):
    username= "Not logged in"
    logged = False
        
    user = None
    wallet = None
    try:
        user = UserModel.find_by_id(get_jwt_identity())
        wallet = WalletModel.find_by_user(get_jwt_identity())
    except:
        pass
    funds = 0

    if wallet != None:
        funds = round(wallet.funds, 3)

    if get_jwt() != {}:
        logged = True
        username = user.username

    service_logo_path = ""
    
    if ';' in category or '-' in category or '?' in category or '%' in category:
        return {"Message": "nice try"}    

    if ';' in service_name or '-' in service_name or '?' in service_name or '%' in service_name:
        return {"Message": "nice try"}
        
    if  "instagram" in service_name.lower():
        service_logo_path = "Instagram-Logo.webp"

    elif "facebook" in service_name.lower():
        service_logo_path = "Facebook-Logo.webp"

    elif "linkedin" in service_name.lower():
        service_logo_path = "LinkedIn-Logo.webp"

    elif "twitter" in service_name.lower():
        service_logo_path = "Twitter.webp"

    elif "telegram" in service_name.lower():
        service_logo_path = "Telegram.svg"

    elif "tiktok" in service_name.lower():
        service_logo_path = "TikTok_Icon_Black_Square.webp"

    elif "youtube" in service_name.lower():
        service_logo_path = "YouTube-Logo.webp"

    print(f"{category=}")
    services_raw = ServiceModel.execute_query(f"SELECT * FROM services WHERE category LIKE '%{category}%' and category LIKE '%{service_name}%' ")
    services_list = [a for a in services_raw]  # Has to be looped through

    admin = False
    logged_in = False
    user_identity = get_jwt_identity()
    print(f"USER IDENTIY: {user_identity=}")
    if user_identity:
        logged_in = True
        if user_identity in ADMINLIST:  
            admin = True

    search_terms = ServiceModel.execute_query(
        f"SELECT DISTINCT category FROM services"
    )

    return render_template(
        "service_details.html",
        username = username,
        search_terms=search_terms,
        funds=funds,
        logged_in=logged_in,
        service_name=service_name,
        services_list=services_list,
        service_logo_path=service_logo_path,
    )


@jwt_required(optional= True)
def search(term):
    username= "Not logged in"
    logged = False
        
    user = None
    wallet = None
    try:
        user = UserModel.find_by_id(get_jwt_identity())
        wallet = WalletModel.find_by_user(get_jwt_identity())
    except:
        pass
    funds = 0

    if wallet != None:
        funds = round(wallet.funds, 3)

    if get_jwt() != {}:
        logged = True
        username = user.username

    service_logo_path = ""

    if ';' in term or '-' in term or '%' in term:
        return {"Message": "Nice try"}

    if "instagram" in term.lower():
        service_logo_path = "Instagram-Logo.webp"

    elif "facebook" in term.lower():
        service_logo_path = "Facebook-Logo.webp"

    elif "linkedin" in term.lower():
        service_logo_path = "LinkedIn-Logo.webp"

    elif "telegram" in term.lower():
        service_logo_path = "Telegram.svg"
    
    elif "twitter" in term.lower():
        service_logo_path = "Twitter.webp"

    elif "tiktok" in term.lower():
        service_logo_path = "TikTok_Icon_Black_Square.webp"

    elif "youtube" in term.lower():
        service_logo_path = "YouTube-Logo.webp"

    services_raw = ServiceModel.execute_query(f"SELECT * FROM services WHERE category LIKE '%{ term }%'")
    services_list = [a for a in services_raw]  # Has to be looped through
    admin = False
    if get_jwt_identity() in ADMINLIST:
        admin = True

    
    search_terms = ServiceModel.execute_query(
        f"SELECT DISTINCT category FROM services"
    )

    return render_template(
        "service_details.html",
        service_logo_path=service_logo_path,
        username = username,
        search_terms=search_terms,
        funds=funds,
        logged=logged,
        services_list=services_list,
    )


@jwt_required(optional=True)
def new_home():
    print("uuuuuuuuuuuuuuuuuuuuu")
    users_online, new_orders, total_orders = get_stats_numbers()

    admin = False
    if get_jwt_identity() in ADMINLIST:
        admin = True

    
    # search_terms = ServiceModel.execute_query(
    #     f"SELECT DISTINCT category FROM services"
    # )
    search_terms =[]
    
    if get_jwt() == {}:
        return render_template(
            "new_home.html",
            logged_in=None,
            search_terms=search_terms,
            timestamp=time.time(),
            admin=admin,
            users_online=users_online,
            new_orders=new_orders,
            total_orders=total_orders
        )
    else:
        user = UserModel.find_by_id(get_jwt_identity())
        wallet = WalletModel.find_by_user(get_jwt_identity())
        funds = 0
        if wallet != None:
            funds = round(wallet.funds, 3)
        admin = False

        if get_jwt_identity() in ADMINLIST:
            admin = True

        username = "Not logged in"
        if get_jwt() != {}:
            username = user.username
        return render_template(
            "new_home.html",
            logged_in=True,
            username=username,
            funds=funds,
            timestamp=time.time(),
            admin=admin,
            users_online=users_online,
            new_orders=new_orders,
            total_orders=total_orders
        )


@jwt_required()
def order_history():
    print("++++++++++++++++++++")
    user = UserModel.find_by_id(get_jwt_identity())
    wallet = WalletModel.find_by_user(get_jwt_identity())
    funds = 0
    if wallet != None:
        funds = round(wallet.funds, 3)
    order_history = OrderHistory.find_all()
    for order in order_history:
        order.base_rate = 0  # Hide base rate
        date_time = str(order.issued_at).split(".")[0]
        order.issued_at = date_time.replace(" ", " at ")
        order.issued_at += " UTC"
        order.link = order.link.replace("https://www.", "")
        if len(order.link) < 50:
            order.link_short = order.link
        else:
            order.link_short = order.link[0:50]
            order.link_short += "..."

        if order.quantity == "":
            order.quantity = 0
        order.cost = float(order.quantity) * float(order.rate) / 1000
        order.cost = round(order.cost, 4)
    admin = False
    if get_jwt_identity() in ADMINLIST:
        admin = True

    
    search_terms = ServiceModel.execute_query(
        f"SELECT DISTINCT category FROM services"
    )
    print("---------------------------")
    return render_template(
        "order_history.html",
        logged_in=True,
        admin=admin,
        username=user.username,
        funds=funds,
        search_terms=search_terms,
        order_history=order_history,
        timestamp=time.time(),
    )


@jwt_required()
def add_funds():
    user = UserModel.find_by_id(get_jwt_identity())
    wallet = WalletModel.find_by_user(get_jwt_identity())
    funds = 0
    if wallet != None:
        funds = round(wallet.funds, 3)

    admin = False
    if get_jwt_identity() in ADMINLIST:
        admin = True
    
    search_terms = ServiceModel.execute_query(
        f"SELECT DISTINCT category FROM services"
    )

    return render_template(
        "add_funds.html", search_terms=search_terms, admin=admin, logged_in=True, username=user.username, funds=funds, timestamp=time.time()
    )


@jwt_required()
def admin_panel():
    admin = False
    if get_jwt_identity() in ADMINLIST:
        admin = True

    user = UserModel.find_by_id(get_jwt_identity())
    wallet = WalletModel.find_by_user(get_jwt_identity())
    funds = 0
    if wallet != None:
        funds = round(wallet.funds, 3)

    services = ServiceModel.find_all()
    services_dict = {}
    for service in services:
        if service.category not in services_dict.keys():
            services_dict[service.category] = []

        services_dict[service.category].append(service)

    users = UserModel.find_all()

    for us in users:
        us.num_orders = len(OrderHistory.find_by_user_id(us.id))
        us.total_spent = round(OrderHistory.user_spent(us.id),3)
        us.funds = -1 
        try:
            us.funds = round(WalletModel.find_by_id(us.id).funds,3)
        except:
            us.funds = "No wallet"
        


    
    search_terms = ServiceModel.execute_query(
        f"SELECT DISTINCT category FROM services"
    )

    return render_template(
        "admin_panel.html",
        admin=admin,
        services_dict=services_dict.items(),
        logged_in=True,
        users_list=users,
        username=user.username,
        funds=funds,
        timestamp=time.time(),
    )


@jwt_required()
def check_status(order_id):
    print("order_id"+str(order_id))
    user_id = get_jwt_identity()
    order = OrderHistory.find_by_order_id(order_id)
    if order:
        # Make sure the user had made the order
        if user_id == order.user_id:

            url = "https://spiderpanel.com/api/v2"

            querystring = {"key": "0ff95bb78fd927a8750f6c2cda1442dd", "action": "status", "order": order_id}

            payload = ""
            response = requests.request("GET", url, data=payload, params=querystring)

            print(response.json())
            return response.json()['status']


def google_verify():
    
    return render_template("google756ae359b1032929.html") 

