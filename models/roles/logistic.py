from models.roles.autenticatable_employee import AutenticatableEmployee
class Logistic(AutenticatableEmployee):
    def __init__(self, name: str, dni: str, experience: int, password: str):
        super().__init__(name, dni, "Logística", 15000, experience, password)

    def obtain_bonus(self):
        bonus = self.get_salary() * 0.3
        self.set_salary(self.get_salary() + bonus)
        return bonus
    
    def percentage_increase(self) -> float:
        return 0.02
    