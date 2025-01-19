from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import random


# Define the UPI transaction model
class UPITransaction(BaseModel):
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    timestamp: datetime = Field(..., description="Date and time of the transaction")
    sender_vpa: str = Field(..., description="Sender's Virtual Payment Address")
    receiver_vpa: str = Field(..., description="Receiver's Virtual Payment Address")
    transaction_type: str = Field(..., description="Type of transaction, e.g., 'credit' or 'debit'")
    amount: float = Field(..., description="Amount transferred")
    status: str = Field(..., description="Status of the transaction, e.g., 'success', 'pending', 'failed'")
    remarks: str = Field(..., description="Optional remarks or note attached to the transaction")


# Generate synthetic UPI transactions
def generate_upi_transactions(count: int) -> List[UPITransaction]:
    statuses = ["success", "pending", "failed"]
    transaction_types = ["credit", "debit"]
    vp_domains = ["@upi", "@ybl", "@okicici", "@okhdfcbank", "@oksbi"]

    transactions = []
    for _ in range(count):
        transaction = UPITransaction(
            transaction_id=f"TXN{random.randint(10000000, 99999999)}",
            timestamp=datetime.now().replace(microsecond=0),
            sender_vpa=f"user{random.randint(1, 100)}{random.choice(vp_domains)}",
            receiver_vpa=f"user{random.randint(101, 200)}{random.choice(vp_domains)}",
            transaction_type=random.choice(transaction_types),
            amount=round(random.uniform(10.0, 10000.0), 2),
            status=random.choice(statuses),
            remarks=random.choice(
                ["Payment for services", "Refund", "Bill Payment", "Gift", "Lunch", "Groceries"]
            ),
        )
        transactions.append(transaction)

    return transactions


# Generate 20-25 transactions
transactions = generate_upi_transactions(25)

# Print sample transactions
for txn in transactions:
    print(txn.dict())
