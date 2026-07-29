from .client import Client
from models.accounts.transaction import Transaction
from models.exceptions.insufficient_balance_exception import InsufficientBalanceException
from models.exceptions.impossible_operation_exception import ImpossibleOperationException
from models.accounts.card import Card
import uuid
from datetime import datetime
from datetime import timedelta

class BankAccount:
    account_count: int = 0

    def __init__(self, bank_number: int, client: Client, account_number: str | None = None):
        if bank_number is None or bank_number <= 0:
            raise ValueError("Es obligatorio un número de agencia válido")

        self.bank_number = bank_number
        self.account_number = (
            account_number if account_number is not None
            else str(uuid.uuid4().int)[:8]
        )
        self.client = client
        self._balance: float = 0.0
        self.interest_rate: float = 0.0
        self.overdraft_limit: float = 0.0
        self.account_active: bool = True
        self.commission_value: float = 0.0
        self.transfer_limit: float = 3000000
        self.__withdrawals_without_balance: int = 0
        self.__transfers_without_balance: int = 0
        self.transactions: list["Transaction"] = []
        self.max_transactions_per_minute = 100
        self.creation_date = datetime.now()
        self.cards: list["Card"] = []
        self.locked_until: datetime | None = None
        self.daily_withdrawal_limit: int | None = None


        BankAccount.account_count += 1

    def get_balance(self) -> float:
        return self._balance

    def get_withdrawals_without_balance(self) -> int:
        return self.__withdrawals_without_balance

    def get_transfers_without_balance(self) -> int:
        return self.__transfers_without_balance
    
    def get_min_balance(self)-> float:
        return 0

    def get_max_transactions_per_minute(self):
        return self.max_transactions_per_minute

    def has_blocked_card(self):
        if not self.cards:
            return False

        return any(card.is_blocked for card in self.cards)

    def can_withdraw(self, amount: float)-> bool:
        if self._balance - amount < self.get_min_balance():
            return False
        return True
    
    def daily_withdraws(self):
        today = datetime.now().date()
        return [
        t for t in self.transactions
        if t.type == "Retiro" and t.date.date() == today
        ]
    
    def check_transaction_limit(self):
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)

        recent = [
            t for t in self.transactions
            if t.date >= one_minute_ago
        ]

        if len(recent) >= self.get_max_transactions_per_minute():
            raise ImpossibleOperationException("Límite excedido")

    def withdraw(self, amount: float) -> bool:
        if not self.account_active:
            raise ImpossibleOperationException("La cuenta está inactiva.")
        
        if self.is_temporarily_locked():
            raise ImpossibleOperationException("La cuenta está bloqueada temporalmente.")

        if self.has_blocked_card():
            raise ImpossibleOperationException("La tarjeta está bloqueada, no se pueden realizar operaciones.")
        
        self.check_transaction_limit()
        
        if amount <= 0:
            raise ValueError("Monto inválido")

        if not self.can_withdraw(amount):
            self.__withdrawals_without_balance += 1
            raise InsufficientBalanceException("No puede superar el límite de la cuenta")

        self._balance -= amount

        withdraw = Transaction(type="Retiro", amount= amount, origin_acc=self, destination_acc= None, description=f"Retiro de: ${amount}")

        self.transactions.append(withdraw)

        return True

    def deposit(self, amount: float) -> None:
        if not self.account_active:
            raise ImpossibleOperationException("La cuenta está inactiva.")
    
        if self.is_temporarily_locked():
            raise ImpossibleOperationException("La cuenta está bloqueada temporalmente.")
  
        self.check_transaction_limit()

        if amount < 0:
            raise ValueError("Es imposible depositar un valor negativo.")
        
        self._balance += amount
        deposit = Transaction(type="Depósito", amount= amount, origin_acc=self, destination_acc= None, description=f"Depósito de: ${amount}")
        self.transactions.append(deposit)

    def transfer(self, amount: float, target_account: "BankAccount") -> float:
        if not self.account_active:
            raise ImpossibleOperationException("La cuenta origen está inactiva.")
        
        if not target_account.account_active:
            raise ImpossibleOperationException("La cuenta destino está inactiva.")

        if target_account.is_temporarily_locked():
            raise ImpossibleOperationException("La cuenta destino está bloqueada temporalmente.")

        if self.is_temporarily_locked():
            raise ImpossibleOperationException("La cuenta origen está bloqueada temporalmente.")

        if self == target_account:
            raise ImpossibleOperationException("No puede transferir a la misma cuenta.")

        if amount <= 0:
            raise ValueError("Monto inválido")

        if amount > self.transfer_limit:
            raise ImpossibleOperationException(f"El monto supera el límite de transferencia (${self.transfer_limit})")

        try:
            self.withdraw(amount)
            target_account.deposit(amount)

        except InsufficientBalanceException:
            self.__transfers_without_balance +=1
            raise

        except Exception:
            self._balance += amount
            raise
        
        transfer = Transaction(type="Transferencia", amount=amount, origin_acc= self, destination_acc= target_account, description=f"Transferencia de ${amount} a la cuenta: {target_account}")
        self.transactions.append(transfer)

        return self._balance

    def show_history(self):
        for x in self.transactions:
            print(x)

    def __str__(self) -> str:
        return (f"Número de cuenta: {self.account_number}\n"
                f"Número de banco: {self.bank_number}\n"
                f"DNI: {self.client.dni}\n"
                f"Nombre del cliente: {self.client.name}\n"
                f"Saldo: {self._balance}")
    
    def is_temporarily_locked(self):
        if self.locked_until is not None and datetime.now() >= self.locked_until:
            self.locked_until = None
            self.account_active = True
            return False
        return self.locked_until is not None

    def set_withdrawals_without_balance(self, value: int):
        self.__withdrawals_without_balance = value

    def set_transfers_without_balance(self, value: int):
        self.__transfers_without_balance = value
    
    def to_dict(self):
        return {
            "account_type": type(self).__name__,
            "bank_number": self.bank_number,
            "account_number": self.account_number,
            "client_dni": self.client.dni,
            "client_name": self.client.name,
            "balance": self._balance,
            "interest_rate": self.interest_rate,
            "overdraft_limit": self.overdraft_limit,
            "account_active": self.account_active,
            "commission_value": self.commission_value,
            "creation_date": self.creation_date.isoformat(),
            "locked_until": self.locked_until.isoformat() if self.locked_until else None,
            "transactions": [t.to_dict() for t in self.transactions],
            "cards": [c.to_dict() for c in self.cards],
            "transfer_limit": self.transfer_limit,
            "withdrawals_without_balance": self.get_withdrawals_without_balance(),
            "transfers_without_balance": self.get_transfers_without_balance()
        }