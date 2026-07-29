from datetime import datetime

class AuditLog:
    def __init__(self, action_type, operator_name, target_name, target_dni, details=""):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.action_type = action_type
        self.operator_name = operator_name
        self.target_name = target_name
        self.target_dni = target_dni
        self.details = details 

    def to_string(self):
        if self.action_type == "CREATE":
            return f"[{self.timestamp}] CREACIÓN: El operador {self.operator_name} creó al empleado {self.target_name} (DNI: {self.target_dni})."
        
        elif self.action_type == "DELETE":
            return f"[{self.timestamp}] DESPIDO: El operador {self.operator_name} eliminó al empleado {self.target_name} (DNI: {self.target_dni}). Motivo: {self.details}"
        
        elif self.action_type == "UPDATE":
            return (
                f"[{self.timestamp}] ACTUALIZACIÓN: "
                f"El operador {self.operator_name} actualizó al empleado "
                f"{self.target_name} (DNI: {self.target_dni}). "
                f"{self.details}"
            )

        elif self.action_type == "REJECT":
            return (
                f"[{self.timestamp}] RECHAZO: "
                f"El operador {self.operator_name} rechazó la solicitud de "
                f"{self.target_name} (DNI: {self.target_dni}). "
                f"{self.details}"
            )

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "action_type": self.action_type,
            "operator_name": self.operator_name,
            "target_name": self.target_name,
            "target_dni": self.target_dni,
            "details": self.details
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(
            action_type=data["action_type"],
            operator_name=data["operator_name"],
            target_name=data["target_name"],
            target_dni=data["target_dni"],
            details=data.get("details", "")
        )

        obj.timestamp = data["timestamp"]
        return obj