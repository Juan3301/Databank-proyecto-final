from models.accounts.bank_account import BankAccount
from models.exceptions.impossible_operation_exception import ImpossibleOperationException
from models.accounts.client import Client

class SavingsAccount(BankAccount):
    def __init__(self, bank_number: int, client: Client, account_number: str | None = None):
        super().__init__(bank_number, client, account_number)
        self.interest_rate = 0.5
        self.daily_withdrawal_limit = 6
        self.transfer_limit = 5000000
        
    def apply_interest_rate(self):
        self._balance += self._balance * self.interest_rate

    def withdraw(self, amount: float) -> bool:
        if amount <=0:
            raise ImpossibleOperationException("Monto Inválido")
        
        if amount > self.get_balance():
            raise ImpossibleOperationException("La cuenta de ahorros no permite saldo negativo")
        
        return super().withdraw(amount)
    
    def get_max_transactions_per_minute(self):
        return 2
    
    def can_withdraw(self, amount):
        return (
            len(self.daily_withdraws()) < self.daily_withdrawal_limit # type: ignore
            and self._balance - amount >= 0
        )    

    def to_dict(self):
        data = super().to_dict()
        data["daily_withdrawal_limit"] = self.daily_withdrawal_limit
        return data
