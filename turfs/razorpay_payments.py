import razorpay
from razorpay_datas.models import *



def credentials(modelname):
    if modelname == "TEST":
        cred = Test_credentials.objects.values('key_id','secret').get(active_status = "YES")
        print("cred :: ",cred)
        if cred:
            return {
                "key_id":cred["key_id"],
                "secret":cred["secret"],
                "stat":"Ok"
            }
        else:
            return {
                "key_id":"",
                "secret":"",
                "stat":"Not Ok"
            }

def create_client_session(KEY_ID,KEY_SECRET):
    print("KEY_ID :: ",KEY_ID)
    print("KEY_SECRET :: ",KEY_SECRET)
    client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
    return client


def get_customer_by_email(email,client):
    try:
        customers = client.customer.all({'email': email})
        if customers['count'] > 0:
            customer = customers['items'][0]
            return {"customer":customer,"stat":"Ok"}
        else:
            return {"customer":"","stat":"Not OK"}
    except Exception as e:
        print(f"Error retrieving customer: {e}")
        return {
            "error":str(e),
            "stat":"Not OK"
        }


def create_customer(name, email, contact,client):
    try:
        customer_data = {"name": name, "email": email, "contact": contact}
        customer = client.customer.create(customer_data)
        return {
            "customer":customer,
            "stat":"Ok"
        }
    except Exception as e:
        print(f"Error creating customer: {e}")
        return {
            "stat":"Not Ok",
            "error":str(e)
        }

def create_fund_account(customer_id, account_holder_name, ifsc, account_number,client):
    try:
        fund_account_data = {
            "customer_id": customer_id,
            "account_type": "bank_account",
            "bank_account": {
                "name": account_holder_name,
                "ifsc": ifsc,
                "account_number": account_number
            }
        }
        fund_account = client.fund_account.create(fund_account_data)
        print(f"Fund Account created with ID: {fund_account['id']}")
        return {"fund_account":fund_account,"stat":"Ok"}
    except Exception as e:
        print(f"Error creating Fund Account: {e}")
        return {
            "error":str(e),
            "stat":"Not Ok"
        }

# def list_fund_accounts(customer_id,client):
#     try:
#         fund_accounts = client.fund_account.all({'customer_id': customer_id})
#         if fund_accounts['count'] > 0:
#             print(f"Found {fund_accounts['count']} Fund Account(s) for customer ID {customer_id}:")
#             for fa in fund_accounts['items']:
#                 print(f" - ID: {fa['id']}, Account Holder: {fa['bank_account']['name']}")
#             return {"fund_accounts":fund_accounts['items'],"stat":"Ok"}
#         else:
#             return {"fund_accounts":[],"stat":"Ok"}
#     except Exception as e:
#         return {"fund_accounts":[],"stat":"Not Ok","error":str(e)}


def initiate_penny_drop(fund_account_id,client, amount=100, currency="INR", mode="IMPS"):
    try:
        payout_data = {
            "fund_account_id": fund_account_id,
            "amount": amount,
            "currency": currency,
            "mode": mode,
            "purpose": "payout",
            "queue_if_low_balance": True
        }
        payout = client.payout.create(payout_data)
        print(f"Payout initiated with ID: {payout['id']}")
        return {
            "stat":"Ok",
            "payout":payout
        }
    except Exception as e:
        print(f"Error initiating payout: {e}")
        return {
            "stat":"Not Ok",
            "error":str(e)
        }

def get_payout_status(payout_id,client):
    try:
        payout = client.payout.fetch(payout_id)
        status = payout['status']
        print(f"Payout Status for {payout_id}: {status}")
        return {
            "stat":"Ok",
            "payout":payout
        }
    except Exception as e:
        print(f"Error fetching payout status: {e}")
        return {
            "stat":"Not Ok",
            "error":str(e)
        }




def main_func(using_cred:str,clientname:str,clientemail:str,contact:str,ifsc:str,account_number:str):
    try:
        get_cred = credentials(using_cred)
        print("get_cred :: ",get_cred)
        session = create_client_session(get_cred["key_id"],get_cred["secret"])
        check_customer = get_customer_by_email(clientemail,session)
        if "error" not in check_customer and check_customer["stat"] == "Ok":
            return {
                "data":check_customer["customer"]
            }
        elif "error" not in check_customer and check_customer["stat"] != "Ok":
            
        # if get_cred["stat"] == "Ok":
            create_user = create_customer(clientname,clientemail,contact,session)
            if create_user["stat"] == "Ok":
                fund_acc = create_fund_account(create_user["customer_id"],clientname,ifsc,account_number,session)
                if fund_acc["stat"] == "Ok":
                    initi_penny_drop = initiate_penny_drop(fund_acc["fund_account"]["id"],session)
                    if initi_penny_drop["stat"] == "Ok":
                        payout_status = get_payout_status(initi_penny_drop["payout"]["id"],session)
                        if payout_status["stat"] == "Ok":
                            return payout_status
                        else:
                            return "Payout status error"
                    else:
                        return "Initiate penny drop error"
                else:
                    return "Fund account creation error"
            else:
                return "create user error"
                
        # else:
        #     return {
        #         "error":"getting credentials error",
        #         "stat":"Not Ok"
        #     }
    except Exception as e:
        return {
            "stat":"Not Ok",
            "error":str(e),
            "msg":"syntax error 1"
        }

