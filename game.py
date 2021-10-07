import random


class Dots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y
        except:
            pass


class Ship:
    def __init__(self, size, is_vertical, point):
        self.size = size
        self.lives = size
        self.is_vertical = is_vertical
        self.point = point
        # self.deployed = []

    def deploy(self, size, is_vertical, point):
        deployed = []  # Список ячеек, занятых короблями
        deployed_x = point.x
        deployed_y = point.y

        self.is_vertical = is_vertical
        for dot in range(size):
            if size > 1:
                if self.is_vertical:
                    deployed_x += 1
                else:
                    deployed_y += 1
            deployed.append(Dots(deployed_x, deployed_y))
        return deployed


class Field:
    def __init__(self, size):
        self.size = size
        self.cell = [['0']*size for i in range(size)]
        self.deployed = []
        self.ships = []
        self.ship_quantity = 7

    def is_in_field(self, point):
        if point.x in range(self.size) and point.y in range(self.size):
            return True
        else:
            return False

    def is_empty(self, point):
        for deployed_dot in self.deployed:
            if deployed_dot == point:
                return False
            else:
                return True
        return True

    def check_borders(self, dots):
        border = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in dots:
            if self.is_empty(dot):
                return False
            for delta_x, delta_y in border:
                delta_dot = dot.x + delta_x, dot.y + delta_y
                empty = self.is_empty(delta_dot)
                print(f'Check emptyness: {empty}')
                if not empty:
                    print('kontur')
                    return False
        return True

    def add_deployed(self, ship_dots):
        all_dots_in_field = False
        for deployed_cell in ship_dots:
            if self.is_in_field(deployed_cell):
                all_dots_in_field = True
                if self.check_borders(ship_dots):
                    return False
            else:
                return False
        for deployed_cell in ship_dots:
            print(f'row: {deployed_cell.x+1} column: {deployed_cell.y+1}')
            if all_dots_in_field:
                self.cell[deployed_cell.x][deployed_cell.y] = '■'
                self.deployed.append(deployed_cell)
        return True

    def shot(self, cell):
        for ship in self.ships:
            if cell in self.deployed:
                ship.lives -= 1
                self.cell[cell.x][cell.y] = 'X'
                if ship.lives == 0:
                    self.ship_quantity -= 1
                    print('Корабль уничтожен!')
                else:
                    print('Корабль ранен')
            else:
                self.cell[cell.x][cell.y] = 'T'
                print('Мимо')

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.cell):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        return res


class Player:
    def __init__(self, oponent_field, is_human):
        self.oponent_field = oponent_field
        self.is_human = is_human

    def AI_turn(self, oponent_field):
        self.oponent_field = oponent_field
        self.make_turn(False)

    def human_turn(self, oponent_field):
        self.oponent_field = oponent_field
        self.make_turn(True)

    def make_turn(self, is_human):
        if is_human:
            cord_x = input('Введите колонку: ')
            cord_y = input('Введите строку: ')
        else:
            cord_x = random.randrange(0, self.oponent_field.size - 1)
            cord_y = random.randrange(0, self.oponent_field.size - 1)
        return Dots(cord_x, cord_y)


class Game:
    def __init__(self, size=6):
        self.size = size
        self.player_field = Field(size)
        self.AI_field = Field(size)

    def random_place(self):
        sizes = [3, 2, 2, 1, 1, 1, 1]
        field = Field(size=self.size)
        for ship_size in sizes:
            result = False
            attempts = 0
            while not result:
                attempts += 1
                print(f'Attempt: {attempts} whith size {ship_size}')
                if attempts > 10:
                    return None
                ship = Ship(ship_size, random.randrange(0, 2),
                            Dots(random.randrange(0, self.size), random.randrange(0, self.size)))
                ship_dots = ship.deploy(ship_size, random.randrange(0, 2),
                                        Dots(random.randrange(0, self.size), random.randrange(0, self.size)))
                # ship_dots = ship.deploy(ship_size, 0, Dots(0, 0))
                result = field.add_deployed(ship_dots)
                print(f'Result: {result}')
            print(f'****************** end attempt ******************\n')
        print(f'End field\n\n')
        return field

    def game_process(self):
        player = Player(self.AI_field, True)
        player_field = self.random_place()
        AI_player = Player(self.player_field, False)
        AI_player_field = self.random_place()
        while True:
            print('Ход игрока: ')
            print(player_field)
            print("\n", "*"*26)
            print(AI_player_field)
            player.human_turn(AI_player_field)
            print('Ход компьютера: ')
            AI_player.AI_turn(player_field)


game = Game()
game.game_process()
