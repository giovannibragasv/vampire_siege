from src.settings import VAMPIRE_SPEED, VAMPIRE_HP, VAMPIRE_DAMAGE
from src.entities.enemy import Enemy


class Vampire(Enemy):
    COLOR = (18, 18, 46)

    def __init__(self, cx, cy):
        super().__init__(cx, cy, VAMPIRE_HP, VAMPIRE_SPEED, VAMPIRE_DAMAGE, self.COLOR)
