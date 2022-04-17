class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x:2},{self.y:2})'

    def goto(self, direction):
        if direction == 'E':
            self.x = self.x + 1
            self.y = self.y
        elif direction == 'NE':
            self.x = self.x + 1
            self.y = self.y + 1
        elif direction == 'N':
            self.x = self.x
            self.y = self.y + 1

    def get_slope(self, other):
        if self.x == other.x:
            return 100000000
        return (self.y - other.y) / (self.x - other.x)

    def get_coefficient(self, other):
        return other.y - self.y, self.x - other.x

    def get_decision_variable(self, other):
        m = self.get_slope(other)
        a, b = self.get_coefficient(other)

        if m < 1:
            return 2 * a + b, 2 * a, 2 * (a + b)
        elif m >= 1:
            return a + 2 * b, 2 * b, 2 * (a + b)


def do_conversion(point1, point2, d, option_1, option_2, direction_1, direction_2):

    print(f'starting point: {point1}')
    print(f'ending point : {point2}')

    itr = '   row'
    i = point1.y + 1
    j = point2.y
    if m < 1:
        i = point1.x + 1
        j = point2.x
        itr = 'column'

    print(f'{itr}|   d|  pixel|  co-ordinate')
    print(f'{i - 1:6}|   -|      -|      {point1}')

    temp_point = point1
    while i <= j:
        temp_d = d
        if d <= 0:
            direction = direction_1
            d += option_1
        else:
            direction = direction_2
            d += option_2

        temp_point.goto(direction)

        print(f'{i:6}| {temp_d:3}| {direction: >6}|      {temp_point}')
        i += 1


if __name__ == '__main__':
    x, y = input('Enter first point(x, y):').split()
    p1 = Point(int(x), int(y))
    x, y = input('Enter second point(x, y):').split()
    p2 = Point(int(x), int(y))

    m = p1.get_slope(p2)

    if m < 1:
        d_start, delta_E, delta_NE = p1.get_decision_variable(p2)
        do_conversion(p1, p2, d_start, delta_E, delta_NE, 'E', 'NE')
    elif m >= 1:
        d_start, delta_N, delta_NE = p1.get_decision_variable(p2)
        do_conversion(p1, p2, d_start, delta_NE, delta_N, 'NE', 'N')