import numpy as np
from sympy import Symbol, pprint, sympify, lambdify
import matplotlib.pyplot as plt


def create_table(y_arr):
    n = len(y_arr)
    table = np.zeros((n, n), 'int')

    for k in range(n):
        for i in range(n - k):
            if k == 0:
                table[i][k] = y_arr[i]
            else:
                table[i][k] = table[i + 1][k - 1] - table[i][k - 1]

    return table


def newton_polynomial_backward(table, x_arr, h):
    x = Symbol('x')
    n = len(table) - 1
    expr = sympify(table[n][0])
    fact = 1
    t = (x - x_arr[n]) / h
    tt = t
    i = 2

    while i != n + 2:
        expr += table[n - i + 1][i - 1] * tt / fact
        tt *= (t + i - 1)
        fact *= i
        i += 1

    return expr


x_arr = np.array([8, 11, 14, 17, 20, 23, 26, 29])
y_arr = np.array([3, 7, 11, 17, 20, 20, 21, 22])
h = 3

if __name__ == '__main__':
    table = create_table(y_arr)
    print(table)
    polynomial = newton_polynomial_backward(table, x_arr, h).simplify()
    pprint(polynomial)

    # интерполирующая функция
    x = Symbol('x')
    func = lambdify(x, polynomial)
    x_range = np.linspace(8, 29, 100)
    y_range = func(x_range)

    # точка x со звездочкой
    x_star = 22
    y_star = polynomial.subs(x, x_star)
    print(y_star)

    plt.plot(x_arr, y_arr, 'ro', x_range, y_range, x_star, y_star, 'b*')
    plt.show()
