from datetime import datetime
from models.roles.director import Director
from models.roles.administrative import Administrative
from models.roles.analist import Analist
from models.roles.logistic import Logistic

class EmployeeFactory:
    @staticmethod
    def from_dict(data):
        employee_type = data["employee_type"]

        if employee_type == "Director":
            employee = Director(
                name=data["name"],
                dni=data["dni"],
                department=data["department"],
                experience=data["experience"],
                password=data["password"]
            )

        elif employee_type == "Administrative":
            employee = Administrative(
                name=data["name"],
                dni=data["dni"],
                experience=data["experience"],
                password=data["password"]
            )

        elif employee_type == "Analist":
            employee = Analist(
                name=data["name"],
                dni=data["dni"],
                experience=data["experience"],
                password=data["password"]
            )

        elif employee_type == "Logistic":
            employee = Logistic(
                name=data["name"],
                dni=data["dni"],
                experience=data["experience"],
                password=data["password"]
            )

        else:
            raise ValueError(f"Tipo de empleado desconocido: {employee_type}")

        employee.set_salary(data["salary"])
        employee.is_blocked = data["is_blocked"]
        employee.failed_attempts = data["failed_attempts"]
        employee.can_change_role = data["can_change_role"]

        if data["locked_until"] is not None:
            employee.locked_until = datetime.fromisoformat(data["locked_until"]) # type: ignore

        if "register_date" in data:
            employee.register_date = datetime.fromisoformat(data["register_date"])

        return employee