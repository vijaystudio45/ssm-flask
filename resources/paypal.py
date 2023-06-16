import os

from flask import jsonify, request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

import paypalrestsdk as pp
from models.user import UserModel

from models.wallet import WalletModel


pp.configure(
    {
        "mode": "live",
        "client_id": "ASqoRGnJPvk4ne011_uAs-_Oa1s7fg5gxB4L2VHI-8rhVtFW-aHYci5HGbn13OsQpHh_HXvrnyvoi7XL",
        "client_secret": "EOX-zZMqlJzL0Xy-pCoVvsJUKY5WAQ-AxZCKSzks741vLaO1up5XAfbhKo21vFxCkf51sSm2trU9rndr",
    }
)


class PaypalCreatePayment(Resource):
    def post(self, amount):
        amount = float(amount)
        payment = pp.Payment(
            {
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {"return_url": "http://146.190.22.4/payment/execute", "cancel_url": "http://146.190.22.4/add_funds"},
                "transactions": [
                    {
                        "item_list": {
                            "items": [{"name": "test balance", "sku": "12345", "price": amount, "currency": "USD", "quantity": 1}]
                        },
                        "amount": {"total": amount, "currency": "USD"},
                        "description": "This is the payment transaction description.",
                    }
                ],
            }
        )

        if payment.create():
            print("payment created!")
        else:
            print(payment.error)

        return jsonify({"paymentID": payment.id})


class PaypalExecutePayment(Resource):
    # @jwt_required() not working
    def post(self):
        print("payment")
        payment = pp.Payment.find(request.form["paymentID"])
        amount = float(payment["transactions"][0]["amount"]["total"])
        if payment.execute({"payer_id": request.form["payerID"]}):
            # Topping up the user's balance
            UserModel.create_wallet_if_not_exists(int(request.form["_user_id"]))
            WalletModel.topup(int(request.form["_user_id"]), amount)
            print("payment executed successfully!")
            return jsonify({"success": True})
        else:
            print(payment.error)
        return jsonify({"success": False})
