import uuid
from models.roles.employee import Employee
from datetime import datetime

class Log:
    def __init__(self, employee: Employee, action: str, status: bool, details: str = ""):
        self.id = uuid.uuid4().hex[:8]
        self.date = datetime.now()
        self.employee = employee
        self.action = action
        self.status = status 
        self.details = details

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "employee_dni": self.employee.get_dni(),
            "action": self.action,
            "status": self.status,
            "details": self.details
        }
    
    @classmethod
    def from_dict(cls, data, employees):
        employee = next(
            (e for e in employees if str(e.get_dni()) == str(data["employee_dni"])),
            None
        )

        if employee is None:
            raise ValueError(
                f"No existe el empleado con DNI {data['employee_dni']}"
            )

        log = cls(
            employee=employee,
            action=data["action"],
            status=data["status"],
            details=data.get("details", "")
        )

        log.id = data["id"]
        log.date = datetime.fromisoformat(data["date"])

        return log
    
    def __str__(self) -> str:
         return (
            f"ID: {self.id} \n"
            f"Fecha: {self.date} \n"
            f"Empleado: {self.employee.name} \n"
            f"Acción: {self.action} \n"
            f"Estado: {self.status} \n"
            f"Detalles: {self.details} \n"
            )