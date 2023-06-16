from os import stat
from xml.etree.ElementTree import Comment
from click import command
from flask import jsonify, request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import true
from models.user import UserModel
from models.transaction import TransactionModel

from utils.coinbase_wrapper import CoinbaseWrapper

Coinbase = CoinbaseWrapper("8bad8804-8d29-4823-a6af-dc3dd4f243e1")


class CoinbaseResource(Resource):

    # This endpoint should create a new coinbase charge
    @jwt_required()
    def post(self):
        amount = request.json["amount"]
        user_id = get_jwt_identity()
        resp = Coinbase.API_create_charge(user_id, UserModel.find_by_id(user_id).email, amount)
        print("coinbase API:", Coinbase.api_key)
        transaction = TransactionModel(resp["data"]["id"], user_id, "coinbase", amount)
        transaction.save_to_db()
        print(resp)
        return {"message": "Created", "id": resp["data"]["id"], "hosted_url": resp["data"]["hosted_url"]}, 200

    @jwt_required()
    def get(self):
        id = request.json["transaction_id"]
        return Coinbase.API_get_charge(id)
