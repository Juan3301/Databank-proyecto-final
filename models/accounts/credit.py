from models.accounts.client import Client

class Credit:
    def __init__(self, amount: float, interest_rate: float, months: int, client: Client):
        self.amount = amount
        self.interest_rate = interest_rate
        self.months = months
        self.client = client
        self.approved = False
        self.remaining_balance = amount
        self.status = "Pendiente"
        client.add_credit(self)

    def __str__(self) -> str:
        return (f"Credito de {self.amount} para {self.client.name}")
    
    def to_dict(self):
        return {
            "amount": self.amount,
            "interest_rate": self.interest_rate,
            "months": self.months,
            "approved": self.approved,
            "remaining_balance": self.remaining_balance,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data, client):
        credit = cls(
            amount=data["amount"],
            interest_rate=data["interest_rate"],
            months=data["months"],
            client=client
        )

        credit.approved = data["approved"]
        credit.remaining_balance = data["remaining_balance"]
        credit.status = data["status"]

        return credit
