#Author:ZJF

from .auth import authenticate
from .utils import print_error
from .logger import logger
from atm import logics

transaction_logger = logger("transaction")  # 日记
access_logger = logger("access")            # 存取日记  数据库
features = [
    ("账户信息",logics.view_account_info),
    ("取现",logics.with_draw),
    ("还款",logics.pay_back)
    ]                                            # 特性

def controller(user_obj):
    """功能分配"""
    while True:
        for index,feature in enumerate(features):
            print(index,feature[0])
        choice = input("ATM>>:").strip()
        if not choice:continue
        if choice.isdigit():
            choice = int(choice)
            if choice < len(features) and choice >= 0:
                features[choice][1](user_obj,transaction_logger=transaction_logger,access_logger=access_logger)
        if choice == "exit":
            exit("Bye.")
def entrance():
    """ATM交互程序入口"""

    user_obj = {
        "is_authenticated":False,
        "data":None
    }

    retry_count = 0
    while user_obj["is_authenticated"] is not True:
        account = input("\033[32;1maccount:\033[0m").strip()
        password = input("\033[32;1mpassword:\033[0m").strip()
        auth_data = authenticate(account,password)#验证
        if auth_data:
            user_obj["is_authenticated"] = True
            user_obj["data"] = auth_data
            print("welcome")
            access_logger.info("user %s just loggged in" % user_obj["data"]["id"])

            controller(user_obj)
        else:
            print_error("Wrong username or password!")
        retry_count += 1

        if retry_count == 3:
            msg = "user %s tired wrong password reached 3 times" % account
            print_error(msg)
            access_logger.info(msg)
            break
