from faker import Faker
import random
import uuid
import json
from datetime import datetime, timedelta
        
fake = Faker()

def generate_transaction():
    transaction_id = "TXN" + str(uuid.uuid4())[:8].upper()
    user_id = "USR" + str(random.randint(1000, 9999))
    merchant = random.choice(["Amazon", "Flipkart", "eBay", "Apple", "Netflix"])
    amount = round(random.uniform(10, 500), 2)
    currency = random.choice(["USD", "EUR", "INR", "GBP"])
    payment_method = random.choice(["CreditCard", "DebitCard", "UPI", "PayPal"])
    payment_gateway = random.choice(["Stripe", "Razorpay", "PayPal", "Square"])
    transaction_date = fake.date_time_between(start_date="-90d", end_date="now").isoformat()
    status = random.choice(["Completed", "Failed", "Refunded"])
    refund_status = random.choice(["None", "Pending", "Approved", "Denied"])
    dispute_status = random.choice(["None", "Open", "Resolved"])
    order_id = "ORD" + str(uuid.uuid4())[:8].upper()
    product_description = random.choice([
        "AI Ebook", "Bluetooth Speaker", "Mobile App Subscription", "Online Course", "Cloud Storage Plan"
    ])
    delivery_status = random.choice(["Delivered", "Not Delivered"])
    
    refund_reason = (
        fake.sentence(nb_words=6) if refund_status in ["Pending", "Approved", "Denied"] else ""
    )
    policy_matched = random.choice([True, False]) if refund_status != "None" else None
    support_notes = fake.sentence(nb_words=12) if random.random() < 0.3 else ""

    return {
        "transaction_id": transaction_id,
        "user_id": user_id,
        "merchant": merchant,
        "amount": amount,
        "currency": currency,
        "payment_method": payment_method,
        "payment_gateway": payment_gateway,
        "transaction_date": transaction_date,
        "status": status,
        "refund_status": refund_status,
        "dispute_status": dispute_status,
        "order_id": order_id,
        "product_description": product_description,
        "delivery_status": delivery_status,
        "refund_reason": refund_reason,
        "policy_matched": policy_matched,
        "support_notes": support_notes
    }

# Generate dataset
def generate_dataset(n=1000, output_file="mock_transactions.json"):
    data = [generate_transaction() for _ in range(n)]
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

# Run generator
generate_dataset(10000)  # change number as needed


