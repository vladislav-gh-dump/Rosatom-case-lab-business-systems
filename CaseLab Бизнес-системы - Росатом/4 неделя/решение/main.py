import random as rn

def matrix_employees(count_employees):
    matrix = [[[0 for _ in range(2)] for _ in range(count_employees)] for _ in range(count_employees)]
    rand_num = rn.randint(0, count_employees)
    for i in range(count_employees):
        for j in range(count_employees):
            if (i > j):
                matrix[i][j][0] = matrix[j][i][1]
                matrix[i][j][1] = matrix[j][i][0]

            if (j > i):
                matrix[i][j][0] = rn.randint(0, 1)
                matrix[i][j][1] = 1

            if (i == rand_num): matrix[i][j] = [0, 1]
            if (j == rand_num): matrix[i][j] = [1, 0]
        matrix[i][i] = [1, 1]
    return matrix

def draw_matrix(matrix, column, row):
    string = " # "
    for i in range(len(row)): string += f"|   {i+1:<2}  |"
    string += "|#######|"
    string += "\n" + ("-" * 56)
    print(string)

    for i in range(len(matrix)):
        string = f" {i+1} "
        for j in range(len(matrix[i])):
            if (i == j):
                string += "|#######|"
            else:
                slot = "|"
                for k in range(len(matrix[i][j])):
                    slot += f" {matrix[i][j][k]} /"
                slot = slot[:-1] + "|"
                string += slot
        string += f"|   {row[i]:<2}  |"
        string += "\n" + ("-"*56)
        print(string)
    string = " # "

    for c in column: string += f"|   {c:<2}  |"
    print(string + "|#######|")

matrix = matrix_employees(5)

column = []
sum_col = []
for i in range(5):
    sum1 = 0
    sum2 = 0
    for j in range(5):
        if (i != j):
            sum2 += matrix[j][i][0]
    column.append(sum2)
    sum_col.append([sum1, sum2])

row = []
sum_row = []
for i in range(5):
    sum1 = 0
    sum2 = 0
    for j in range(5):
        if (i != j):
            sum1 += matrix[i][j][0]
    row.append(sum1)
    sum_row.append([sum1, sum2])

draw_matrix(matrix, column, row)


if (max(column) * min(row) == 0):
    print(f"\nновенький: {row.index(min(row))+1}")
else:
    print("\nновенького нет")