class PromotionRequest:
    def __init__(self, employee, reasons):
        self.employee = employee
        self.reasons = reasons

    def to_dict(self):
        return {
            "employee_dni": self.employee.get_dni(),
            "reasons": self.reasons
        }

    @classmethod
    def from_dict(cls, data, employees):
        employee = employees.get(str(data["employee_dni"]))
        if employee is None:
            raise ValueError(f"No existe el empleado con DNI {data['employee_dni']}")
        return cls(employee=employee, reasons=data["reasons"])