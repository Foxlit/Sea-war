import random


class ShotChecking(Exception):
    pass


class ShotRepeating(ShotChecking):
    def __str__(self):
        return 'Сюда уже стреляли'


class InvalidInput:
    def __str__(self):
        return 'Ошибка ввода'


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
    def __init__(self, size, hidden=False):
        self.size = size
        self.cell = [['0']*size for i in range(size)]
        self.deployed = []
        self.ships = []
        self.ship_dots_quantity = 0
        self.hidden = hidden

    def is_in_field(self, point):
        if point.x in range(self.size) and point.y in range(self.size):
            return True
        else:
            return False

    def is_empty(self, point):
        for deployed_dot in self.deployed:
            if deployed_dot == Dots(point.x, point.y):
                return False
            else:
                return True
        return True

    def borders_are_empty(self, dots):
        border = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in dots:
            # if self.is_empty(dot):
            #     return False
            for delta_x, delta_y in border:
                delta_dot = Dots(dot.x + delta_x, dot.y + delta_y)
                dot_is_empty = self.is_empty(delta_dot)
                # print(f'Check border emptyness: {dot_is_empty} in ({delta_dot.x};{delta_dot.y})')
                if not dot_is_empty:
                    return False
        return True

    def add_deployed(self, ship_dots):
        all_dots_in_field = False
        for deployed_cell in ship_dots:
            if self.is_in_field(deployed_cell):
                all_dots_in_field = True
            else:
                return False

        if not self.borders_are_empty(ship_dots):
            return False

        for deployed_cell in ship_dots:
            # print(f'row: {deployed_cell.x+1} column: {deployed_cell.y+1}')
            if all_dots_in_field:
                if self.cell[deployed_cell.x][deployed_cell.y] == '■':
                    return False
                else:
                    self.cell[deployed_cell.x][deployed_cell.y] = '■'
                    self.deployed.append(deployed_cell)
                    self.ship_dots_quantity += 1
        return True

    def shot(self, cell):
        for i in self.deployed:
            if self.cell[cell.x][cell.y] == 'T' or self.cell[cell.x][cell.y] == 'X':
                return 'no shot'
            if cell in self.deployed:

                self.cell[cell.x][cell.y] = 'X'
                print('Попадание')
                self.ship_dots_quantity -= 1
                return self.ship_dots_quantity
            else:
                self.cell[cell.x][cell.y] = 'T'
                print('Мимо')
                return self.ship_dots_quantity

    def __str__(self):
        val = ""
        val += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.cell):
            val += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hidden:
            val = val.replace("■", "0")
        return val


class Player:
    def __init__(self, oponent_field, is_human):
        self.oponent_field = oponent_field
        self.is_human = is_human

    def AI_turn(self, oponent_field):
        self.oponent_field = oponent_field
        return self.make_turn(False, oponent_field)

    def human_turn(self, oponent_field):
        self.oponent_field = oponent_field
        return self.make_turn(True, oponent_field)

    def make_turn(self, is_human, current_field):
        if is_human:
            while True:
                try:
                    cord_x = int(input('Введите строку: '))-1
                    cord_y = int(input('Введите колонку: '))-1
                    if cord_x > current_field.size-1 or cord_y > current_field.size-1:
                        print(f'Ошибка ввода! Координаты вне поля')
                        continue
                    break
                except ValueError as e:
                    print(f'Ошибка ввода! Введите число')
        else:
            cord_x = random.randrange(0, self.oponent_field.size - 1)
            cord_y = random.randrange(0, self.oponent_field.size - 1)

        return current_field.shot(Dots(cord_x, cord_y))


class Game:
    def __init__(self, size=6):
        self.size = size
        self.player_field = Field(size)
        self.AI_field = Field(size, True)

    def random_place(self, is_hidden=False):
        sizes = [3, 2, 2, 1, 1, 1, 1]
        field = Field(hidden=is_hidden, size=self.size)
        for ship_size in sizes:
            result = False
            attempts = 0
            while not result:
                attempts += 1
                # print(f'Attempt: {attempts} whith size {ship_size}')
                if attempts > 5000:
                    return None
                ship = Ship(ship_size, random.randrange(0, 2),
                            Dots(random.randrange(0, self.size), random.randrange(0, self.size)))
                ship_dots = ship.deploy(ship_size, random.randrange(0, 2),
                                        Dots(random.randrange(0, self.size), random.randrange(0, self.size)))
                # ship_dots = ship.deploy(ship_size, 0, Dots(0, 0))
                result = field.add_deployed(ship_dots)
        #         print(f'Result: {result}')
        #     print(f'****************** end attempt ******************\n')
        # print(f'End field\n\n')
        return field

    def game_process(self):
        player = Player(self.AI_field, True)
        player_field = self.random_place()
        AI_player = Player(self.player_field, False)
        AI_player_field = self.random_place(True)
        while True:

            print(player_field)
            print("\n", "*"*26)
            print(AI_player_field)

            print('Ход игрока: ')
            shot_is_done = False
            while not shot_is_done:
                AI_dots_left = player.human_turn(AI_player_field)
                if AI_dots_left == 'no shot':
                    print(f'Сюда уже стреляли')
                    continue
                else:
                    break

            if AI_dots_left == 0:
                print('Победил игрок')
                break

            print('Ход компьютера: ')

            shot_is_done = False
            attempts = 0
            while not shot_is_done:
                if attempts > 5000:
                    print("Не удалось выполнить выстрел")
                    break
                pl_dots_left = AI_player.AI_turn(player_field)
                if pl_dots_left == 'no shot':
                    attempts += 1
                    continue
                else:
                    break
            if pl_dots_left == 0:
                print('Победил компьютер')
                break

            # print(f'AI Dots left {AI_dots_left}')
            # print(f'Pl Dots left {pl_dots_left}')


game = Game()
game.game_process()
