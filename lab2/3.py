import numpy as np

def create_table(y_arr):
    table = np.zeros(len(y_arr))
    for i in range(len(y_arr)):
        print('i: ', i)
        for j in range(len(y_arr) - i):
            print('j: ', j)
            if i == 0:
                table[i][j] = y_arr[j]
            else:
                table[i][j] = y_arr[j + 1] - y_arr[j]
    return table


def print_m(M):
    for i in range(len(M)):
        for j in range(len(M[i])):
            print(M[i][j], ' ')


x_arr = [8, 11, 14, 17, 20, 23, 26, 29]
y_arr = [3, 7, 11, 17, 20, 20, 21, 22]


print_m(create_table(y_arr))
