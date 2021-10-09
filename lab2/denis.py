import sympy as sym
import matplotlib.pyplot as plt
import numpy as np
from math import pi


# task 1
def lagrange(xi, xj1):
    x = sym.Symbol('x')
    return (x - xj1) / (xi - xj1)


# task 2
def omega(x_st, arr):
    expr5 = 1
    for k in range(3):
        expr5 = expr5 * (x_st - arr[k])
    return abs(expr5)


# task 5
def make_matr(x, y, dy):
    matr = [([0] * (len(x))) for i in range(len(x))]
    for i in range(3):
        for j in range(3):
            if (i == 0):
                if (j == 0):
                    matr[i][j] = dy[0]
                else:
                    matr[i][j] = y[j] - y[j - 1]
            elif (i == 1):
                if (j == 0):
                    matr[i][j] = matr[i - 1][j + 1] - matr[i - 1][j]
                elif (j == 1):
                    matr[i][j] = (matr[i - 1][j + 1] - matr[i - 1][j]) / (x[j + 1] - x[j - 1])
                else:
                    matr[i][j] = 0
            else:
                if (j == 0):
                    matr[i][j] = (matr[i - 1][j + 1] - matr[i - 1][j]) / (x[i] - x[i - 2])
                else:
                    matr[i][j] = 0
    return matr


# task 1
expr1 = 0
list_x = [-2, -1, 1]
list_y = [5, 0, 2]
for i in range(3):
    expr2 = 1
    for j in range(3):
        if i == j:
            continue
        else:
            expr2 = expr2 * lagrange(list_x[i], list_x[j])
    expr1 = expr1 + expr2 * list_y[i]
expr1 = sym.simplify(expr1)
expr1 = sym.expand(expr1)
sym.pprint(expr1)

# task 2
arr_x = [0, pi / 6, pi / 3]
xst = pi / 4
x = sym.Symbol('x')
func = sym.tan(x)
n = 3
func = sym.diff(func, x, 3)
expr = abs(func.subs(x, pi / 3))
print('answer: ', expr * omega(xst, arr_x) / sym.factorial(n))

# task 3
array_x = [7, 8, 9, 10, 11, 12]
array_y = [99.73, 99.34, 100.42, 101.14, 101.16, 101.18]
array_yy = [[-0.39, 1.08, 0.72, 0.02, 0.02], [0, 1.47, -0.36, -0.7, 0], [0, 0, -1.83, -0.34, 0.7],
            [0, 0, 0, 1.49, 1.04], [0, 0, 0, 0, -0.45]]
x = sym.Symbol('x')
func = array_y[4] + 0.02 * (x - 12) + 0 + (0.7 * (x - 12) * (x - 11) * (x - 10) / 2 / 3) + (
        1.04 * (x - 12) * (x - 11) * (x - 10) * (x - 9) / 2 / 3 / 4) + (
               -0.45 * (x - 12) * (x - 11) * (x - 10) * (x - 9) * (x - 8) / 2 / 3 / 4 / 5)
func_diff = sym.diff(func, x)

# task 5
array_diff_x = [0, 0, 0, 0, 0]
for i in range(5):
    array_diff_x[i] = func_diff.subs(x, array_x[i])
    print('x[', i, ']: ', array_diff_x[i])
Hermite = [[7, 8, 9], [99.73, 99.34, 100.42], [-2.2, 0, 0]]
Hermite_sub = make_matr(Hermite[0], Hermite[1], Hermite[2])
for i in range(3):
    for j in range(3):
        print('Hermite_sub[', i, '][', j, '] - ', Hermite_sub[i][j])

plt.plot([array_x[0], array_x[1], array_x[2]], [array_y[0], array_y[1], array_y[2]], 'ro')
x = np.arange(7, 10, 1)
y = array_y[4] + array_yy[0][4] * (x - 12) + 0 + (array_yy[2][4] * (x - 12) * (x - 11) * (x - 10) / 2 / 3) + (
        array_yy[3][4] * (x - 12) * (x - 11) * (x - 10) * (x - 9) / 2 / 3 / 4) + (
            array_yy[4][4] * (x - 12) * (x - 11) * (x - 10) * (x - 9) * (x - 8) / 2 / 3 / 4 / 5)
plt.plot(x, y)

Herm = 99.73
p = 1
x_symb = sym.Symbol('x')

for i in range(3):
    if (i == 0):
        p *= Hermite_sub[i][0] * (x_symb - Hermite[0][i])
    else:
        p *= Hermite_sub[i][0] * (x_symb - Hermite[0][i - 1]) / (Hermite_sub[i - 1][0])
    Herm += p

for i in range(3):
    print('Herm[', i, '] - ', Herm.subs(x_symb, Hermite[0][i]))
plt.plot([7, 8, 9],
         [Herm.subs(x_symb, Hermite[0][0]), Herm.subs(x_symb, Hermite[0][1]), Herm.subs(x_symb, Hermite[0][2])])
plt.show()
