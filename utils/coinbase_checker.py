import sqlalchemy as db
from sqlalchemy import update
from coinbase_wrapper import CoinbaseWrapper
import time
from datetime import datetime


Coinbase = CoinbaseWrapper("8bad8804-8d29-4823-a6af-dc3dd4f243e1")
engine = db.create_engine("sqlite:////var/www/html/ssm/data.db")
connection = engine.connect()
metadata = db.MetaData()
transactions = db.Table("transactions", metadata, autoload_with=engine)
wallets = db.Table("wallets", metadata, autoload_with=engine)
print("starting coinbase_checker!")
def get_pending_transactions_from_db():
    query = db.select([transactions]).where(transactions.columns.type == "coinbase").where(transactions.columns.status == "pending")
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    return ResultSet

def set_as_expired(transaction_id):
    result = connection.execute(
        update(transactions).where(transactions.c.transaction_id == transaction_id).
        values(status='expired')
    )
    print(result)

def set_as_resolved(transaction_id):
    result = connection.execute(
        update(transactions).where(transactions.c.transaction_id == transaction_id).
        values(status='resolved')
    )

def topup_user_balance(transaction, info):
    tranasction_owner_id = transaction[7]
    topup_amount = info['payments'][-1]['value']['local']['amount']
    connection.execute(
        update(wallets).where(wallets.c.user_id == tranasction_owner_id).
        values(funds = wallets.c.funds + topup_amount)
    )
    print(f"Account with id {transaction[7]} topped up with ${topup_amount}")

def get_from_coinbase(transaction_id):
    charge = Coinbase.API_get_charge(transaction_id)
    return charge["data"]


# Only checks the charges with status "Pending"
def get_all_charges():
    while True:
        print(f" {datetime.now()} Checking...")
        pending_transactions = get_pending_transactions_from_db()
        for transaction in pending_transactions:
            info = get_from_coinbase(transaction[1])
            most_recent_status = info['timeline'][-1]['status']
            # Update the transactions with the new information
            
            print(f"{most_recent_status=}, {info['id']=}")
            if most_recent_status in ["EXPIRED", "CANCELED"]:
                set_as_expired(info['id'])
                
            elif most_recent_status in ["COMPLETED","UNRESOLVED"]:
                topup_user_balance(transaction, info)
                set_as_resolved(info['id'])

        time.sleep(600)

get_all_charges()

# for result in get_pending_transactions_from_db():
#     coinbase_transaction = get_from_coinbase(result["transaction_id"])
#     # print(coinbase_transaction["timeline"])
#     for event in coinbase_transaction["timeline"]:
#         status = event["status"]
#         if status == "EXPIRED":
#             print("EXPIRED")
            

#     print(result)
