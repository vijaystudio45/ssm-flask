from datetime import date, datetime
from xml.etree.ElementTree import Comment
from click import command
from flask import jsonify, request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
from sqlalchemy import true
from models.service import ServiceModel

from models.user import UserModel
from models.wallet import WalletModel
from models.orderhistory import OrderHistory
from resources.wallet import Wallet
from views import ADMINLIST, order_history

KEY = "0ff95bb78fd927a8750f6c2cda1442dd"

MAINTENANCE = False

class ServiceHandler(Resource):

    # This should render the prices of

    @jwt_required()
    def post(self):
        print("getting...")
        if(MAINTENANCE):
            return {"message": "Oough! We're having a maintenance break. We'll be back in 2-3 minutes."}, 503
        task_id = 0
        user_id = get_jwt_identity()

        body = request.get_json()
        print(body)
        # Required params!
        service_id = body.get("service_id")
        link = body.get("link")

        # Optional params!
        quantity = body.get("quantity")
        comments = body.get("comments", "")
        username = body.get("username", "")
        answer_number = body.get("answer_number", "")

        service = ServiceModel.find_by_id(service_id)
        charge_amount = 0
        status = 0

        user_wallet = WalletModel.find_by_user(user_id)
        if user_wallet == None:
            return {"message": "No wallet for this user, please deposit funds to your account"}, 402  # Payment required
        
        charge_amount = (float(quantity) / 1000) * service.rate
        if user_wallet.check_bal() < charge_amount:
            return {"message": "Not enough funds on the account, please add more funds using 'Add funds' option "}
        
        if service.type == "Custom Comments":
            quantity = len(comments.split('\n'))
        
        print("rate", service.rate, "quantity", quantity)
        
        try:
            status = WalletModel.charge(user_id, charge_amount)
        except:
            return {"Error": "Please fill in the correct information!"}
        
        if not status[0]:
            print(f"status {status}, to charge {charge_amount}")
            return status

        task = Tasks(service.type, service_id, link, quantity, comments, username, answer_number)

        task_status = task.submit()

        if "task_id" in task_status.keys():
            order_log = OrderHistory(
                user_id,
                task_status["task_id"],
                service.name,
                link,
                service.base_rate,
                service.rate,
                datetime.utcnow(),
                False,
                quantity,
                "",
            )
            order_log.save_to_db()
            return "You've successfully made an order, check the order history page!"
        
        return task_status


class ServiceUpdate(Resource):
    @jwt_required()
    def put(self, service_id, new_name, new_rate):
        identity = get_jwt_identity()
        if identity in ADMINLIST:  # or whatever admin's id is... should be loaded from somewhere
            ServiceModel.update_price(service_id, new_rate)
            ServiceModel.update_name(service_id, new_name)
            return {"message": "updated successfully"}, 200
        return {"message": "unauthorized"}, 401



class ServiceEnabler(Resource):
    @jwt_required()
    def post(self, service_id, status):
        identity = get_jwt_identity()
        if identity in ADMINLIST:  # or whatever admin's id is... should be loaded from somewhere
            if status == "True":
                ServiceModel.enable_service(service_id)
            else:
                ServiceModel.disable_service(service_id)
            return {"message": "updated successfully"}, 200

        return {"message": "unauthorized"}, 401


class Tasks:
    def __init__(self, _type, service, link, quantity, comments, username, answer_number):
        self.URL = "https://spiderpanel.com/api/v2"
        self._init_params(_type, service, link, quantity, comments, username, answer_number)

    def _init_params(self, _type, service, link, quantity=1, comments="", username="", answer_number=""):
        self.parameters = {"key": KEY, "action": "add", "service": service, "link": link}
        _type = _type.lower()

        if _type == "default":
            self.parameters["quantity"] = int(quantity)

        elif _type == "custom comments":
            self.parameters["comments"] = comments

        elif _type == "mentions user followers":
            self.parameters["quantity"] = quantity
            self.parameters["username"] = username

        elif _type == "comment likes":
            self.parameters["quantity"] = quantity
            self.parameters["username"] = username

        elif _type == "poll":
            self.parameters["quantity"] = quantity
            self.parameters["answer_number"] = answer_number

    def submit(self):

        # Custom (ours) tasks handler:
        print("aa"+self.parameters['service'])
        if self.parameters['service'] == '8413': # or check if it's in a list of custom services (future)
            return self.custom_handler()

        print("Submitting a task...")
        print(self.parameters)

        url = "https://spiderpanel.com/api/v2"

        payload = ""
        response = requests.request("GET", url, data=payload, params=self.parameters)

        print(response.text)
        res = response.json()
        if "error" in res:
            return {"An error has occured:": res["error"]}

        return {"task_id": res["order"]}


    def custom_handler(self):
        if self.parameters['service'] == '8413':
            url = "https://993ibru2ff.execute-api.ap-south-1.amazonaws.com/api/client_request"
            payload = {
                "category": 1,
                "target_url": self.parameters['link'],
                "action": "join",
                "max_user": self.parameters['quantity'],
                "proxy": False
            }
            headers = {
                "Content-Type": "application/json",
                "X-Api-Key": "ZsipAjyO4l9rw8QED4XqH68MuXRL8GmG8SFKtxrd"
            }
            print(payload)
            response = requests.request("POST", url, verify=False, timeout=10, json=payload, headers=headers)
            print(response.text)
            
            if "30" in response.text:
                return (True,{"message": "Because of heavy load, we've successfully scheduled the request for 30 minutes! :)"})
            return (False, response.json())
            