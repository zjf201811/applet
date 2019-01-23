#Author:ZJF
import sys,os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from conf import settings
from atm.db_handler import save_db

def make_transaction(logger,user_obj,tran_type,amount,**kwargs):
    amount = float(amount)
    if tran_type in settings.TRANSACTION_TYPE:

        interest = amount*settings.TRANSACTION_TYPE[tran_type]["interest"]
        old_balance = user_obj["data"]["balance"]
        if settings.TRANSACTION_TYPE[tran_type]["action"] == "plus":
            new_balance = old_balance + amount + interest
        elif settings.TRANSACTION_TYPE[tran_type]["action"] == "minus":
            new_balance = old_balance - amount - interest
            if new_balance < 0:
                print("""\033[31;1mYour credit [%s] is not enough for this transaction [-%s],your current
                [%s]"""%(user_obj["data"]["credit"],(amount + interest),old_balance))
                return{"status": 1, "error": "交易失败，余额不足"}

        user_obj["data"]["balance"] = new_balance
        save_db(user_obj["data"])

        logger.info("account:%s   action:%s   amount:%s    interest:%s  balance:%s"%
                    (user_obj["data"]["id"],tran_type,amount,interest,new_balance))
        return{"status":0,"msg":"交易操作成功"}
    else:
        print("\033[31;1mTransaction type [%s] is not exist!\033[0m"%tran_type)
        return{"status":1,"error": "交易失败,Transaction type [%s] is not exist!" %tran_type}