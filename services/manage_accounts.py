from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.bank import Bank

from models.accounts.savings_account import SavingsAccount
from models.accounts.bank_account import BankAccount
from models.accounts.checking_account import CheckingAccount
from models.accounts.business_account import BussinessAccount
from models.accounts.young_account import YoungAccount
from models.accounts.client import Client
from models.roles.employee import Employee
from models.exceptions.impossible_operation_exception import ImpossibleOperationException

class ManageAccounts:
    def __init__(self, bank: "Bank"):
        self.bank = bank
    
    def create_account(self, employee: "Employee", client: "Client", account_type: str):
        self.bank.validate_permission(employee, "Crear_Cliente")

        account_types = {
            "Ahorros": SavingsAccount,
            "Corriente": CheckingAccount,
            "Empresarial": BussinessAccount,
            "Juvenil": YoungAccount
        }

        if account_type not in account_types:
            raise ValueError("Tipo de cuenta inválido")

        account_class = account_types[account_type]

        account = account_class(
            bank_number = self.bank.bank_number,
            client = client
        )

        self.bank.accounts.append(account)

        return account

    def delete_account(self, employee: "Employee", account: BankAccount):
        self.bank.validate_permission(employee, "Borrar_Cuenta")

        if account in self.bank.accounts:
            self.bank.accounts.remove(account)
            return True

        return False
    
    def change_account_status(self, employee: "Employee", account: BankAccount):
        self.bank.validate_permission(employee, "Borrar_Cuenta")

        account.account_active = not account.account_active

        return account.account_active
    
    def close_account(self, employee: "Employee", account: "BankAccount"):
        self.bank.validate_permission(employee, "Borrar_Cuenta")
        if account.get_balance() != 0:
            raise ImpossibleOperationException("No se puede cerrar una cuenta con saldo pendiente.")
        account.account_active = False
        self.bank.accounts.remove(account)
        self.bank.register_log("Cierre_de_cuenta", employee, True, "Cierre de cuenta por no uso")
        return True
    
    def apply_monthly_fee(self, employee: "Employee", account: "BankAccount", fee: float):
        self.bank.validate_permission(employee, "Borrar_Cuenta")
        if not account.account_active:
            raise ImpossibleOperationException("La cuenta no está activa.")
        if fee <= 0:
            raise ValueError("La comisión debe ser mayor a 0.")
        account.withdraw(fee)
        self.bank.register_log("Cuota de manejo", employee, True, "Cobro de cuota de manejo")
        return account.get_balance()