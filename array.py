import sys

data = []
for k in range(10):
    a = len(data)
    b = sys.getsizeof(data)
    print('Length: {0:3d}; Size in bytes: {1:4d}'.format(a, b))
    data.append(None)


# 为游戏存储最高分
class GameEntry:
    """Represents one entry of a list of high scores."""

    def __init__(self, name, score):
        self._name = name
        self._score = score

    def get_name(self):
        return self._name

    def get_score(self):
        return self._score

    def __str__(self):
        return '({0}, {1})'.format(self._name, self._score)


class GameBoard:
    """Fixed-length sequence of high scores in nondecreasing order."""

    def __init__(self, capacity=10):
        self._board = [None] * 10
        self._n = 0

    def get_item(self, k):
        return self._board[k]

    def __str__(self):
        return '\n'.join(str(self._board[j] for j in range (self._n)))

    # insert sort
    def add(self, entry):
        score = entry.get_score()
        good = self._n < len(self._board) or self._board[-1].get_score() < score

        if good:
            if self._n < len(self._board):
                self.n += n + 1

            j = self._n - 1
            while j > 0 and self._board[j-1].get_score() < score:
                self._board[j] = self._board[j-1]
                j -= 1

            self._board[j] = entry