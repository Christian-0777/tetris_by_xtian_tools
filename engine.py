"""Display-independent falling-block rules."""
import random

WIDTH, HEIGHT = 10, 20
SHAPES = dict(I=('....', '####', '....', '....'), O=('##', '##'),
              T=('.#.', '###', '...'), S=('.##', '##.', '...'),
              Z=('##.', '.##', '...'), J=('#..', '###', '...'),
              L=('..#', '###', '...'))


def cells(shape):
    return [(x, y) for y, row in enumerate(shape) for x, c in enumerate(row) if c == '#']


class Game:
    def __init__(self, challenge=False, rng=None):
        self.rng = rng or random.Random()
        self.challenge = challenge
        self.board = [[None] * WIDTH for _ in range(HEIGHT)]
        if challenge:
            for row in self.board[-4:]:
                row[:] = [self.rng.choice(('X', 'X', None)) for _ in row]
                row[self.rng.randrange(WIDTH)] = None
        self.bag = []
        self.score = self.lines = 0
        self.state = 'playing'
        self.next = self.draw()
        self.spawn()

    @property
    def level(self):
        return self.lines // 10

    def draw(self):
        if not self.bag:
            self.bag = list(SHAPES)
            self.rng.shuffle(self.bag)
        return self.bag.pop()

    def spawn(self):
        self.kind, self.next = self.next, self.draw()
        self.shape = SHAPES[self.kind]
        self.x, self.y = (WIDTH - len(self.shape)) // 2, 0
        if not self.fits(self.shape, self.x, self.y):
            self.state = 'game over'

    def fits(self, shape, x, y):
        return all(0 <= x+i < WIDTH and 0 <= y+j < HEIGHT and not self.board[y+j][x+i]
                   for i, j in cells(shape))

    def move(self, dx, dy):
        if self.fits(self.shape, self.x+dx, self.y+dy):
            self.x += dx
            self.y += dy
            return True
        return False

    def rotate(self, clockwise=True):
        s = self.shape
        rotated = tuple(zip(*s[::-1])) if clockwise else tuple(zip(*s))[::-1]
        for shift in (0, -1, 1, -2, 2):
            if self.fits(rotated, self.x+shift, self.y):
                self.shape, self.x = rotated, self.x+shift
                break

    def landing(self):
        y = self.y
        while self.fits(self.shape, self.x, y+1):
            y += 1
        return y

    def step(self, soft=False):
        if self.move(0, 1):
            self.score += int(soft)
        else:
            self.lock()

    def drop(self):
        end = self.landing()
        self.score += 2 * (end-self.y)
        self.y = end
        self.lock()

    def lock(self):
        for i, j in cells(self.shape):
            self.board[self.y+j][self.x+i] = self.kind
        remaining = [row for row in self.board if not all(row)]
        n = HEIGHT-len(remaining)
        self.board = [[None]*WIDTH for _ in range(n)] + remaining
        self.score += (0, 40, 100, 300, 1200)[n] * (1+self.level)
        self.lines += n
        if self.challenge and self.lines >= 25:
            self.state = 'course clear'
        else:
            self.spawn()
