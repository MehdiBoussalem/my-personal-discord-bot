class MyPokemon:
    def __init__(self, name, level, type, hp, attack, defense, sp_atk, sp_def, speed, moves, id, sprite_front,
                 sprite_back):
        self.sprite_back = sprite_back
        self.sprite_front = sprite_front
        self.name = name
        self.level = level
        self.type = type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_atk = sp_atk
        self.sp_def = sp_def
        self.speed = speed
        self.moves = moves
        self.id = id

    def __str__(self):
        return f"{self.name} - {self.level} - {self.type} - {self.hp} - {self.attack} - {self.defense} - {self.sp_atk} - {self.sp_def} - {self.speed} - {self.moves} - {self.id}"

    def getName(self):
        return self.name

    def getLevel(self):
        return self.level

    def getType(self):
        return self.type

    def getHp(self):
        return self.hp

    def getAttack(self):
        return self.attack

    def getDefense(self):
        return self.defense

    def getSpAtk(self):
        return self.sp_atk

    def getSpDef(self):
        return self.sp_def

    def getSpeed(self):
        return self.speed

    def setName(self, name):
        self.name = name

    def setLevel(self, level):
        self.level = level

    def setType(self, type):
        self.type = type

    def setHp(self, hp):
        self.hp = hp

    def setAttack(self, attack):
        self.attack = attack

    def setDefense(self, defense):
        self.defense = defense

    def setSpAtk(self, sp_atk):
        self.sp_atk = sp_atk

    def setSpDef(self, sp_def):
        self.sp_def = sp_def

    def setSpeed(self, speed):
        self.speed = speed
