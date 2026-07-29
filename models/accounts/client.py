from datetime import datetime
class Client:
    def __init__(self, name: str, dni: int, age: int, profession: str):
        self.name = name
        self.dni = dni
        self.age = age
        self.profession = profession
        self.credits = []
        self.is_blacklisted = False
        self.blacklist_reason = ""
        self.registration_date: datetime | None = None

    def add_credit(self, credit):
        self.credits.append(credit)

    def __str__(self) -> str:
        return f"Cliente: {self.name}, Dni: {self.dni}"

    def to_dict(self):
        return {
            "name": self.name,
            "dni": self.dni,
            "age": self.age,
            "profession": self.profession,
            "is_blacklisted": self.is_blacklisted,
            "blacklist_reason": self.blacklist_reason,
            "registration_date": self.registration_date.isoformat() if self.registration_date else None,
            "credits": [credit.to_dict() for credit in self.credits]
        }

    @classmethod
    def from_dict(cls, data):
        client = cls(
            name=data["name"],
            dni=data["dni"],
            age=data["age"],
            profession=data["profession"]
        )

        client.is_blacklisted = data["is_blacklisted"]
        client.blacklist_reason = data["blacklist_reason"]
        client.registration_date = (
        datetime.fromisoformat(data["registration_date"])
        if data.get("registration_date") else None
        )

        return client