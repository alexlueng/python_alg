matrix = [[1, 2, 3], [4, 5, 6]]

matrix_T = [list(i) for i in zip(*matrix)]

print(matrix_T)