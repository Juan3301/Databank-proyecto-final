from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.bank import Bank

class ReportObjects:
    def __init__(self, bank: "Bank"):
        self.bank = bank

    def generate_employee_report(self):
        report = []
        for employee in self.bank.employees:
          report.append({
              "Nombre": employee.name,
              "Dni": employee.get_dni(),
              "Rol": employee.get_position(),
              "Salario": employee.get_salary(),
              "Experiencia": employee.experience,
              "Está bloqueado": employee.is_blocked
          })
        return report
  
    def generate_security_report(self): 
        failed_logins = 0

        for log in self.bank.logs:
            if log.action == "login" and not log.status:
                failed_logins += 1

        report = []

        report.append(f"Total de logs: {len(self.bank.logs)}")
        report.append(f"Intentos de inicio de sesión fallidos: {failed_logins}")
        report.append(f"Saldo total del banco: ${self.bank.total_assets:,.2f}")

        if failed_logins > 100:
            report.append("Alerta crítica: Se recomienda bloquear cuentas afectadas.")
        elif failed_logins > 50:
            report.append("Alerta alta: Se recomienda bloqueo temporal.")
        elif failed_logins > 20:
            report.append("Alerta: Número alarmante de intentos fallidos.")
        elif failed_logins > 10:
            report.append("Alerta: Demasiados intentos fallidos.")
        elif failed_logins > 3:
            report.append("Alerta: Múltiples intentos fallidos detectados.")
        else:
            report.append("Sin alertas de seguridad.")

        return report
      
    def generate_credit_report(self):
          print("Generando reporte de créditos...")
          print("\n===== REPORTE DE CRÉDITOS =====\n")
          report = []
          for client in self.bank.clients:
            for credit in client.credits:
                report.append({
                    "Cliente": client.name,
                    "Monto": credit.amount,
                    "Estado": credit.status,
                    "Tasa de interés": credit.interest_rate,
                    "Meses": credit.months
                })
    
          print("Reporte de créditos generado exitosamente.")
          return report

    def generate_clients_report(self):
        report = []

        for client in self.bank.clients:
            report.append(str(client))

        return report


    def generate_accounts_report(self):
        report = []

        for account in self.bank.accounts:
            report.append(str(account))

        return report

    def generate_transactions_report(self):
        report = []

        for transaction in self.bank.global_transactions:
            report.append(str(transaction))

        return report

    def generate_financial_report(self):
        total_balance = 0

        for account in self.bank.accounts:
            total_balance += account.get_balance()

        return {
            "total_accounts": len(self.bank.accounts),
            "total_clients": len(self.bank.clients),
            "total_money": total_balance
        }
    
