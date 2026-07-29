from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.bank import Bank
    
from models.roles.autenticatable_employee import AutenticatableEmployee
from models.roles.employee import Employee
from models.roles.director import Director
from models.roles.administrative import Administrative
from models.roles.analist import Analist
from models.roles.logistic import Logistic
from models.exceptions.impossible_operation_exception import ImpossibleOperationException
from services.auditlog import AuditLog

class ManageEmployees:
    def __init__(self, bank: "Bank"):
        self.bank = bank
    
    def add_employee(self, employee: "Employee", target: "Employee"):
        self.bank.validate_permission(employee, "Crear_Empleado")
        self.bank.employees.append(target)
        audit = AuditLog("CREATE", employee.name, target.name, target.get_dni())
        self.bank.register_log_e(audit)
        print ("\nEmpleado añadido exitosamente.")
        return target

    def delete_employee(self, employee: "Employee", target: "Employee"):
        self.bank.validate_permission(employee, "Eliminar_Empleado")
        if target in self.bank.employees: 
            self.bank.employees.remove(target) 
            audit = AuditLog("DELETE", employee.name, target.name, target.get_dni(), details="")
            print("\nEmpleado removido exitosamente.")
            return True 
        return False

    def change_role(self, employee: "AutenticatableEmployee", target: "AutenticatableEmployee", new_role: str, department: str):
        self.bank.validate_permission(employee, "Crear_Empleado")

        if target not in self.bank.employees:
            raise ImpossibleOperationException("El empleado objetivo no pertenece a este banco.")

        if new_role == "Analista":
            new_employee : Employee = Analist(target.name, target.get_dni(), target.experience, target.get_password())
            print("\nCambio a analista realizado exitosamente.")
        
        elif new_role == "Logistica":
            new_employee = Logistic(target.name, target.get_dni(), target.experience, target.get_password())
            print("\nCambio a logistica realizado exitosamente.")
        
        elif new_role == "Administrativo":
            new_employee = Administrative(target.name, target.get_dni(), target.experience, target.get_password())
            print("\nCambio a administrativo realizado exitosamente.")
        
        elif new_role == "Director":
            new_employee = Director(target.name, target.get_dni(), department, target.experience, target.get_password())
            print("\nCambio a director realizado exitosamente.")
        
        else:
            raise ImpossibleOperationException("Rol inválido.")

        self.bank.employees[self.bank.employees.index(target)] = new_employee
        return new_employee

    def approve_salary_increase(self, employee: "Employee", target, amount: float):
        if not employee.can_modify_salary(target, amount):
            raise PermissionError("No es posible modificar el salario.")

        target.set_salary(target.get_salary() + amount)

        return target.get_salary()


    def apply_salary_increase(self, employee: "Employee", target: "Employee"):
        if not employee.can_raise_salary(target):
            raise PermissionError("No es posible aumentar el salario.")
        
        target.raise_salary()

        return target.get_salary()

    def evaluate_promotion(self, director: "Director", employee: "Employee"):
        if not director.can_create_user():
            raise ImpossibleOperationException("Permiso denegado.")
        
        if employee.can_request_promotion():
            return {
                "eligible": True,
                "reason": "El empleado cumple los requisitos mínimos para solicitar promoción."
            }
        
        return {
            "eligible": False,
            "reason": "El empleado no cumple todos los requisitos para ser promovido."
        }
    
    def approve_promotion(self, director: "Director", employee: "Employee"):
        if not director.can_create_user():
            raise ImpossibleOperationException("Permiso denegado.")

        employee.experience += 1

        return True
    
    def update_experience(self, employee: "Employee", points: int):
        employee.experience += points

        return employee.experience
