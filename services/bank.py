import json
from datetime import datetime, timedelta
from models.accounts.bank_account import BankAccount
from models.accounts.client import Client
from models.accounts.transaction import Transaction
from models.roles.employee import Employee
from models.exceptions.impossible_operation_exception import ImpossibleOperationException
from models.Log.log import Log
from models.accounts.credit import Credit
from models.accounts.card import Card
from services.account_factory import AccountFactory
from services.bonus_admin import BonusAdmin
from services.analize import Analize
from services.autenticate import AutenticateObjects
from services.list_objects import ListObjects
from services.manage_accounts import ManageAccounts
from services.manage_credits import ManageCredits
from services.manage_employees import ManageEmployees
from services.manage_cards import ManageCards
from services.notificate import Notificate
from services.report import ReportObjects
from services.search import SearchObjects
from services.auditlog import AuditLog
from services.promotion_request import PromotionRequest
from services.salary_inc_req import SalaryIncreaseRequest
from services.employee_factory import EmployeeFactory

class Bank:
    def __init__(self, name: str, number: int, clients: list[Client], employees: list[Employee], global_transactions: list[Transaction], logs: list[Log], bonus_admin: BonusAdmin, password: str):
        self.name = name
        self.bank_number = number
        self.__password = password
        self.clients = clients
        self.employees: list["Employee"] = employees
        self.accounts: list[BankAccount] = []
        self.global_transactions = global_transactions
        self.logs = logs
        self.bonus_admin = bonus_admin
        self.interest_rate = 0.06
        self.audit_history: list[AuditLog]= []
        self.promotion_requests: list [PromotionRequest] = []
        self.salary_requests: list [SalaryIncreaseRequest] = []
        self.audit_logs : list = []

        self.analize = Analize(self)
        self.autenticate = AutenticateObjects(self)
        self.list_objects = ListObjects(self)
        self.manage_accounts = ManageAccounts(self)
        self.manage_credits = ManageCredits(self)
        self.manage_employees = ManageEmployees(self)
        self.manage_cards = ManageCards(self)
        self.notificate = Notificate(self)
        self.report = ReportObjects(self)
        self.search = SearchObjects(self)

    def get_password(self):
        return self.__password

    def set_password(self, new):
        self.__password = new

    @property
    def total_assets(self) -> float:
        return sum(account.get_balance() for account in self.accounts)

    def validate_permission(self, employee: "Employee", action: str):
        permissions = {
            "Crear_Empleado": employee.can_create_user(),
            "Eliminar_Empleado": employee.can_delete_user(),
            "Ver_informacion": employee.can_see_information(),
            "Ver_reportes": employee.can_see_reports(),
            "Cambiar_rol": employee.can_change_role,
            "Crear_Cliente": employee.can_create_user(),
            "Borrar_Cuenta": employee.can_delete_user(),
        }

        if action not in permissions:
            raise ImpossibleOperationException("Operación inválida")
        
        if not permissions[action]:
            raise PermissionError(
                f"{employee.name} no tiene permiso para {action}"
            )
        
        return True

    def create_client(self, employee: "Employee", client_data):
        self.validate_permission(employee, "Crear_Empleado")

        client = Client (
            client_data["name"],
            client_data["dni"],
            client_data["age"],
            client_data["profession"]
        )

        self.clients.append(client)
        return client

    def register_transaction(self, transaction: "Transaction"):
        self.global_transactions.append(transaction)

    def get_account_history(self, account: BankAccount):
        return account.transactions

    def get_client_history(self, client: "Client"):
        transactions = []

        for account in self.accounts:
            if account.client == client:
                for transaction in account.transactions:
                    transactions.append(transaction)

        return transactions

    def get_global_transactions(self, employee: "Employee"):
        self.validate_permission(employee, "Ver_informacion")
        return self.global_transactions

    def register_global_bonus(self):
        for employee in self.employees:
            self.bonus_admin.register(employee)

    def get_total_bonus(self):
        return self.bonus_admin.get_total_bonus()

    def sort_accounts_by_number(self):
        self.accounts.sort(key=lambda account: account.account_number)

        return self.accounts

    def sort_accounts_by_balance(self):
        self.accounts.sort(key=lambda account: account.get_balance())

        return self.accounts

    def register_log(self, action: str, employee: "Employee", status: bool, details: str):
        log = Log(employee, action, status, details)
        self.logs.append(log)
        
        return log

    def get_logs(self):
        return self.logs


    def export_accounts_json(self):
        data = []

        for account in self.accounts:
            data.append({
                "Número de cuenta": account.account_number,
                "Número de banco": account.bank_number,
                "Cliente": account.client.name,
                "Saldo": account.get_balance()
            })
        with open("accounts.json", "w") as file:
            json.dump(
                data,
                file,
                indent=4
            )
      
    def validate_transfer_limit(self, amount: float, limit: float):
        if amount <= 0:
            raise ValueError("El monto debe ser mayor a 0.")
        return amount <= limit  
  
    def temporary_account_lock(self, account: "BankAccount", minutes: int):
        if minutes <= 0:
            raise ValueError("Los minutos deben ser mayor a 0.")
        account.account_active = False
        account.locked_until = datetime.now() + timedelta(minutes=minutes)
        return account.locked_until
  

    def blacklist_client(self, employee: "Employee", client: "Client", reason: str):
        self.validate_permission(employee, "Eliminar_Empleado")
        if not hasattr(client, "is_blacklisted"):
            client.is_blacklisted = False
        client.is_blacklisted = True
        client.blacklist_reason = reason
        self.register_log("Cliente en lista negra", employee, True, f"Cliente {client.name} (DNI: {client.dni}) bloqueado. Motivo: {reason}")
        return True
    
    def register_log_e(self, log_entry):
        self.audit_history.append(log_entry)
    
    def to_dict(self):
        return {
            "bank_name": self.name,
            "bank_number": self.bank_number,
            "password": self.get_password(),
            "interest_rate": self.interest_rate,

            "clients": [client.to_dict() for client in self.clients],

            "employees": [
                employee.to_dict()
                for employee in self.employees
            ],

            "accounts": [
                account.to_dict()
                for account in self.accounts
            ],

            "transactions": [
                transaction.to_dict()
                for transaction in self.global_transactions
            ],

            "logs": [
                log.to_dict()
                for log in self.logs
            ],

            "bonus_admin": self.bonus_admin.to_dict(),

            "promotion_requests": [
                request.to_dict()
                for request in self.promotion_requests
            ],

            "salary_requests": [
                request.to_dict()
                for request in self.salary_requests
            ],

            "audit_history": [
                log.to_dict()
                for log in self.audit_history
            ],

            "audit_logs": [
                log.to_dict()
                for log in self.audit_logs
            ]
        }

    def export_data_json(self):
        data = self.to_dict()

        with open(f"{self.name}_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return True

    def import_data_json(self, filepath: str):

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.name = data["bank_name"]
        self.bank_number = data["bank_number"]
        self.interest_rate = data["interest_rate"]
        self.bonus_admin = BonusAdmin.from_dict(data["bonus_admin"])
        self.set_password (data["password"])

        self.clients = [
            Client.from_dict(c)
            for c in data["clients"]
        ]

        clients = {
            c.dni: c
            for c in self.clients
        }

        for client_data in data["clients"]:
            client = clients[client_data["dni"]]

            for credit_data in client_data["credits"]:
                Credit.from_dict(
                    credit_data,
                    client
                )


        self.employees = [
            EmployeeFactory.from_dict(e)
            for e in data["employees"]
        ]

        employees = {
            e.get_dni(): e
            for e in self.employees
        }

        self.accounts = [
            AccountFactory.from_dict(a, clients)
            for a in data["accounts"]
        ]

        accounts = {
            a.account_number: a
            for a in self.accounts
        }

        self.global_transactions = [
            Transaction.from_dict(t, accounts)
            for t in data["transactions"]
        ]

        for transaction in self.global_transactions:

            if transaction.origin_account:
                transaction.origin_account.transactions.append(transaction)

            if (
                    transaction.destination_account
                    and transaction.destination_account is not transaction.origin_account
                ):
                    transaction.destination_account.transactions.append(transaction)

        for account, account_data in zip(self.accounts, data["accounts"]):

            account.cards = [
                Card.from_dict(card_data, accounts)
                for card_data in account_data["cards"]
            ]

        self.logs = [
            Log.from_dict(log, employees)
            for log in data["logs"]
        ]

        self.promotion_requests = [
            PromotionRequest.from_dict(req, employees)
            for req in data["promotion_requests"]
        ]

        self.salary_requests = [
            SalaryIncreaseRequest.from_dict(req, employees)
            for req in data["salary_requests"]
        ]

        self.audit_logs = [
            AuditLog.from_dict(a)
            for a in data.get("audit_logs", [])
        ]

        self.audit_history = [
            AuditLog.from_dict(a)
            for a in data.get("audit_history", [])
        ]

        return True


        