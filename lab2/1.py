from sympy import Symbol, pprint, sympify, lambdify
import matplotlib.pyplot as plt
import numpy as np


def lagrange(arr_x, arr_y):
    x = Symbol('x')
    expr = sympify('0')
    for i in range(len(arr_y)):
        product = sympify('1')
        for j in range(len(arr_x)):
            if j != i:
                product *= (x - arr_x[j]) / (arr_x[i] - arr_x[j])
        expr += arr_y[i] * product
    return expr


x_arr = np.array([-3, 2, 5])
y_arr = np.array([30, 5, 14])
f = lagrange(x_arr, y_arr).simplify()
pprint(f)

x = Symbol('x')
x_range = np.linspace(-3, 5, 100)
func = lambdify(x, f)
y = func(x_range)

plt.plot(x_range, y, x_arr, y_arr)
plt.show()