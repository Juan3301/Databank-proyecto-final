from models.roles.autenticatable_employee import AutenticatableEmployee
class Administrative(AutenticatableEmployee):
    def __init__(self, name: str, dni: str, experience: int, password: str):
        super().__init__(name, dni, "Administrativo", 20000, experience, password)

    def obtain_bonus(self):
        bonus = self.get_salary() * 0.15
        self.set_salary(self.get_salary() + bonus)
        return bonus
    
    def can_see_reports(self) ->bool:
        return True
    
    def can_see_information(self) -> bool:
        return True
    
    def can_create_user(self) -> bool:
        return True
    
    def can_delete_user(self) ->bool:
        return True
    
    def percentage_increase(self) -> float:
        return 0.08
    