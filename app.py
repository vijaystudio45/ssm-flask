from datetime import datetime
from datetime import timezone
from datetime import timedelta
import os
import time

from dotenv import load_dotenv
from utils.coinbase_wrapper import CoinbaseWrapper

import views
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_restx import Api
from flask_jwt_extended import (
    get_jwt_identity,
    get_jwt,
    create_access_token,
    jwt_required,
    JWTManager,
    set_access_cookies,
    unset_jwt_cookies,
)
from flask_cors import CORS

from db import db

load_dotenv()

from models.user import UserModel
from models.wallet import WalletModel
from models.service import ServiceModel
from models.transaction import TransactionModel

from resources.user import UserActivator, UserRegister, UserLogin, UserLogout, UserAddFunds
from resources.wallet import Wallet
from resources.paypal import PaypalCreatePayment, PaypalExecutePayment
from resources.servicehandler import ServiceHandler, ServiceUpdate, ServiceEnabler
from resources.coinbase import CoinbaseResource, Coinbase


from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing import Pool


app = Flask(__name__)

# will be if the app is being run on Heroku
ON_HEROKU = os.environ.get("ON_HEROKU")

# Here you can globally configure all the ways you want to allow JWTs to
# be sent to your web application. By default, this will be only headers.
# app.config["BASE_URL"] = "http://boostgram.net/"
app.config["BASE_URL"] = "http://127.0.0.1:5000/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SECRET_KEY"] = "7hol100vGE8y1gk2y3b4ASDkj768VinAc7y1823b4jDA"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["JWT_CSRF_CHECK_FORM"] = False
app.config["JWT_COOKIE_SECURE"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config.SWAGGER_SUPPORTED_SUBMIT_METHODS = []

# maintenance will be set to true by mass_update in order to prevent
# anyone from placing an order in a changing database 
MAINTENANCE = True



api = Api(app, doc=False)
jwt = JWTManager(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserActivator, "/activateMail/<string:code>")

api.add_resource(PaypalCreatePayment, "/payment/paypal/create/<amount>")
api.add_resource(PaypalExecutePayment, "/payment/paypal/execute")
api.add_resource(CoinbaseResource, "/payment/coinbase")
api.add_resource(UserAddFunds, "/adminAddFunds/<user_id>/<amount>")

api.add_resource(ServiceHandler, "/submitTask")
api.add_resource(ServiceUpdate, "/updateService/<int:service_id>/<string:new_name>/<float:new_rate>")
api.add_resource(ServiceEnabler, "/updateServiceStatus/<int:service_id>/<status>")


# app.add_url_rule("/login", view_func=views.login)
# app.add_url_rule("/signup", view_func=views.signup)
# app.add_url_rule("/home", view_func=views.home)
# app.add_url_rule("/index", view_func=views.index)
# app.add_url_rule("/wallet", view_func=views.wallet)
# app.add_url_rule("/newhome", view_func=views.newHome)
# app.add_url_rule("/newhome2", view_func=views.newHome2)

app.add_url_rule("/admin_panel", view_func=views.admin_panel)
app.add_url_rule("/mass_update/<string:site>", methods=["POST"], view_func=views.mass_update)
app.add_url_rule("/home", view_func=views.new_home)
app.add_url_rule("/", view_func=views.new_home)
app.add_url_rule("/order_history", view_func=views.order_history)
app.add_url_rule("/add_funds", view_func=views.add_funds)
app.add_url_rule("/signup", view_func=views.signup)

app.add_url_rule("/add_order", view_func=views.add_order)
#app.add_url_rule("/add_order/<string:service_name>", view_func=views.add_order_service)
app.add_url_rule("/add_order_advanced", view_func=views.new_order_advanced)
app.add_url_rule("/add_order/<string:service_name>/<string:category>/details", view_func=views.service_details)
app.add_url_rule("/add_order/search/<string:term>", view_func=views.search)
app.add_url_rule("/add_order/<string:service_name>", view_func=views._test)

app.add_url_rule("/check_status/<int:order_id>", view_func=views.check_status)

app.add_url_rule("/home/google756ae359b1032929.html", view_func=views.google_verify)

# Check for test views:
# path = "/var/www/html/ssm/templates"
# path = "D:\Flask_Project\SSM-main\templates"
path = "D:\\Flask_Project\\SSM-main\\templates"
dir_list = os.listdir(path)
for file in dir_list:
    if "_test_" in file:
        print("222222222222222")
        print(file) 
        a = lambda file: render_template(file)
        app.add_url_rule(f"/test/<string:file>", view_func=a)

@jwt.unauthorized_loader
def failed_loader(_err):
    print(_err)
    try:
        if get_jwt():
            users_online, new_orders, total_orders = views.get_stats_numbers()

            resp = make_response(render_template("new_home.html",users_online=users_online, new_orders=new_orders, total_orders=total_orders, alert="relogin", timestamp=time.time(), port=os.environ.get("PORT", 5000)))
            return resp
    except:
        # return redirect('http://boostgram.net/home')
        return redirect('http://127.0.0.1:5000/home')
    


@jwt.expired_token_loader
def expired(header, payload):
    users_online, new_orders, total_orders = views.get_stats_numbers()
    return render_template("new_home.html", users_online=users_online, new_orders=new_orders, total_orders=total_orders,alert="relogin", timestamp=time.time(), port=os.environ.get("PORT", 5000))


@app.after_request
def refresh_expiring_jwts(response):
    if request.endpoint == "user_logout":
        return response
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


def start():
    from create_app import create_app

    app = create_app()

    port = None
    if ON_HEROKU:
        # get the heroku port
        port = int(os.environ.get("PORT", 17995))  # as per OP comments default is 17995
    else:
        port = 5000

    # app.run(debug=os.environ.get("Debug", True), host="0.0.0.0", port=port)
    app.run(debug=os.environ.get("Debug", True), host="0.0.0.0", port=port)


if __name__ == "__main__":
    start()
