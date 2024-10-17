import razorpay_datas


KEY_ID = "YOUR_KEY_ID"
KEY_SECRET = "YOUR_KEY_SECRET"
client = razorpay_datas.Client(auth=(KEY_ID, KEY_SECRET))

def create_customer(name, email, contact):
    try:
        customer_data = {"name": name, "email": email, "contact": contact}
        customer = client.customer.create(customer_data)
        print(f"Customer created with ID: {customer['id']}")
        return customer
    except Exception as e:
        print(f"Error creating customer: {e}")
        return None

def get_customer_by_email(email):
    try:
        customers = client.customer.all({'email': email})
        if customers['count'] > 0:
            customer = customers['items'][0]
            print(f"Customer found with ID: {customer['id']}")
            return customer
        else:
            print("No customer found with the provided email.")
            return None
    except Exception as e:
        print(f"Error retrieving customer: {e}")
        return None

def create_fund_account(customer_id, account_holder_name, ifsc, account_number):
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
        return fund_account
    except Exception as e:
        print(f"Error creating Fund Account: {e}")
        return None

def list_fund_accounts(customer_id):
    try:
        fund_accounts = client.fund_account.all({'customer_id': customer_id})
        if fund_accounts['count'] > 0:
            print(f"Found {fund_accounts['count']} Fund Account(s) for customer ID {customer_id}:")
            for fa in fund_accounts['items']:
                print(f" - ID: {fa['id']}, Account Holder: {fa['bank_account']['name']}")
            return fund_accounts['items']
        else:
            print("No Fund Accounts found for this customer.")
            return []
    except Exception as e:
        print(f"Error listing Fund Accounts: {e}")
        return []

def initiate_penny_drop(fund_account_id, amount=100, currency="INR", mode="IMPS"):
    """
    Initiates a penny drop by sending a small amount to the specified fund account.
    
    Parameters:
    - fund_account_id (str): The ID of the fund account to send the penny drop to.
    - amount (int): The amount to send in paise. Default is 100 paise (₹1).
    - currency (str): Currency code. Default is INR.
    - mode (str): Transfer mode. Default is IMPS. Alternatives include NEFT, RTGS, etc.
    
    Returns:
    - dict: Response from Razorpay API.
    """
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
        return payout
    except Exception as e:
        print(f"Error initiating payout: {e}")
        return None

def get_payout_status(payout_id):
    """
    Retrieves the status of a payout.
    
    Parameters:
    - payout_id (str): The ID of the payout to check.
    
    Returns:
    - dict: Payout details including status.
    """
    try:
        payout = client.payout.fetch(payout_id)
        status = payout['status']
        print(f"Payout Status for {payout_id}: {status}")
        return payout
    except Exception as e:
        print(f"Error fetching payout status: {e}")
        return None

# Example Workflow
def main():
    # Step 1: Create or Retrieve Customer
    customer_email = "john.doe@example.com"
    customer = get_customer_by_email(customer_email)
    if not customer:
        customer = create_customer(
            name="John Doe",
            email=customer_email,
            contact="9123456789"
        )
    customer_id = customer['id'] if customer else None

    if not customer_id:
        print("Cannot proceed without a valid customer ID.")
        return

    # Step 2: Create Fund Account
    fund_account = create_fund_account(
        customer_id=customer_id,
        account_holder_name="John Doe",
        ifsc="HDFC0001234",
        account_number="1234567890"
    )
    fund_account_id = fund_account['id'] if fund_account else None

    if not fund_account_id:
        print("Cannot proceed without a valid Fund Account ID.")
        return

    # Step 3: Initiate Penny Drop
    payout = initiate_penny_drop(fund_account_id)
    if payout:
        print(f"Penny Drop initiated successfully. Payout ID: {payout['id']}")
        # Optionally, check payout status
        get_payout_status(payout['id'])
    else:
        print("Failed to initiate Penny Drop.")

    # Optional: List all Fund Accounts for the customer
    existing_fund_accounts = list_fund_accounts(customer_id)

if __name__ == "__main__":
    main()
