from models.roles.employee import Employee
class BonusAdmin:
    def __init__(self) -> None:
        self.__total_bonus: float = 0.0

    def register(self, employee: Employee):
        self.__total_bonus += employee.obtain_bonus()

    def get_total_bonus(self):
        return self.__total_bonus

    def set_total_bonus(self, value):
        self.__total_bonus = value

    def to_dict(self):
        return {
            "total_bonus": self.__total_bonus
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        obj.set_total_bonus(data["total_bonus"])
        return obj