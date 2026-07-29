from models.roles.autenticatable_employee import AutenticatableEmployee
class Analist(AutenticatableEmployee):
    def __init__(self, name: str, dni: str, experience: int, password: str):
        super().__init__(name, dni, "Analista", 30000, experience, password)
    
    def obtain_bonus(self) -> float:
        bonus = self.get_salary() * 0.2
        self.set_salary(self.get_salary() + bonus)
        return bonus
    
    def can_see_reports(self) -> bool:
        return True
    
    def percentage_increase(self) -> float:
        return 0.08