from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.accounts.bank_account import BankAccount
    
import uuid
from datetime import datetime
class Transaction:
    def __init__(self, type: str, amount: float, origin_acc: "BankAccount", destination_acc, description: str, transaction_id: str | None = None, date: datetime | None = None):
        self.id = transaction_id if transaction_id is not None else uuid.uuid4().hex[:8]
        self.date = date if date is not None else datetime.now()
        self.type = type
        self.amount = amount
        self.origin_account = origin_acc
        self.destination_account = destination_acc
        self.description = description

    def __str__(self) -> str:
        return (
            f"Id transacción: {self.id}\n"
            f"Fecha de la transacción: {self.date}\n"
            f"Tipo de la transacción: {self.type}\n"
            f"Monto de dinero: {self.amount}\n"
            f"Cuenta de origen: {self.origin_account.account_number}\n"
            f"Cuenta de destino:"
            f"{self.destination_account.account_number if self.destination_account else 'N/A'}\n"
            f"Detalles y descripción: {self.description}\n"
            )
    
    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "type": self.type,
            "amount": self.amount,
            "origin_account": self.origin_account.account_number,
            "destination_account": (self.destination_account.account_number if self.destination_account else None),
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data, accounts):

        origin = accounts[data["origin_account"]]

        destination = (
            accounts[data["destination_account"]]
            if data["destination_account"] is not None
            else None
        )

        return cls(
            type=data["type"],
            amount=data["amount"],
            origin_acc=origin,
            destination_acc=destination,
            description=data["description"],
            transaction_id=data["id"],
            date=datetime.fromisoformat(data["date"])
        )