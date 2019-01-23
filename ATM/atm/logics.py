#Author:ZJF
from .transaction import make_transaction
from atm import utils

def view_account_info(account_data,*args,**kwargs):
    """查看账户状态"""
    print("ACCOUNT INFO".center(50,"-"))
    for k,v in account_data["data"].items():
        if k not in ("password",):
            print("%15s:%s"%(k,v))
    print("END".center(50,"-"))

def with_draw(account_data,*args,**kwargs):
    """取现"""
    trans_logger = kwargs.get("transaction_logger")
    current_balance = """--------- BALANCE INFO ---------
        Credit :    %s
        Balance:    %s"""%(account_data["data"]["credit"],account_data["data"]["balance"])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input("\033[33;1m请输入金额:\033[0m").strip()
        if len(withdraw_amount) > 0 and withdraw_amount.isdigit():
            withdraw_amount = int(withdraw_amount)
            if (account_data["data"]["balance"]/2) >= withdraw_amount:
                transaction_result = make_transaction(trans_logger,account_data,"withdraw",withdraw_amount)
                if transaction_result["status"] == 0:
                    print("""\033[42;1mNew Balance:%s\033[0m"""%(account_data["data"]["balance"]))
                else:
                    print(transaction_result)
            else:
                utils.print_warning("可取月不足，可提现%s"%(int(account_data["data"]["balance"]/2)))

            back_flag = True

        if withdraw_amount == "b":
            back_flag = True

def pay_back(account_data,*args,**kwargs):
    trans_logger = kwargs.get("transaction_logger")
    current_balance = '''--------BALANCE INFO--------
        Credit : %s
        Balance: %s'''%(account_data['data']['credit'],account_data['data']['balance'])
    print(current_balance)
    pay_amount = input("\033[33;1m请输入要还款金额:\033[0m").strip()
    if len(pay_amount)>0 and pay_amount.isdigit():
        pay_amount = int(pay_amount)
        transaction_result=make_transaction(trans_logger,account_data,"repay",pay_amount)
        if transaction_result['status']==0:
            print('''\033[42;1mNew Balance:%s\033[0m'''%(account_data["data"]["balance"]))
        else:
            print(transaction_result)