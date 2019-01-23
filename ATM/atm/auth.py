#Author:ZJF
from .db_handler import load_account_data
from .utils import print_error

def authenticate(account,password):
    """对用户信息进行验证"""
    account_data = load_account_data(account)
    if account_data["status"] == 0: #账户文件加载成功
        account_data = account_data["data"]
        if password == account_data["password"]:
            return account_data
        else:
            return None
    else:
        print_error(account_data["error"])
        return None

