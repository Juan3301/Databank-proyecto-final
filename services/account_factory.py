from datetime import datetime
from models.accounts.savings_account import SavingsAccount
from models.accounts.checking_account import CheckingAccount
from models.accounts.young_account import YoungAccount
from models.accounts.business_account import BussinessAccount

class AccountFactory:

    @staticmethod
    def from_dict(data, clients):
        client = clients[data["client_dni"]]

        match data["account_type"]:
            case "SavingsAccount":
                account = SavingsAccount(
                    data["bank_number"],
                    client,
                    data["account_number"]
                )

            case "CheckingAccount":
                account = CheckingAccount(
                    data["bank_number"],
                    client,
                    data["account_number"]
                )

            case "YoungAccount":
                account = YoungAccount(
                    data["bank_number"],
                    client,
                    data["account_number"]
                )

            case "BussinessAccount":
                account = BussinessAccount(
                    data["bank_number"],
                    client,
                    data["nit"],
                    [clients[dni] for dni in data["authorized_users"]],
                    data["account_number"]
                )

            case _:
                raise ValueError("Tipo de cuenta desconocido")

        account._balance = data["balance"]
        account.interest_rate = data["interest_rate"]
        account.overdraft_limit = data["overdraft_limit"]
        account.account_active = data["account_active"]
        account.commission_value = data["commission_value"]
        account.transfer_limit = data["transfer_limit"]

        if "daily_withdrawal_limit" in data:  
            account.daily_withdrawal_limit = data["daily_withdrawal_limit"]

        account.set_withdrawals_without_balance(data["withdrawals_without_balance"])
        account.set_transfers_without_balance(data["transfers_without_balance"])

        account.creation_date = datetime.fromisoformat(data["creation_date"])

        if data["locked_until"]:
            account.locked_until = datetime.fromisoformat(data["locked_until"])

        return account
