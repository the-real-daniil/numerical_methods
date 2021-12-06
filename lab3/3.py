# решить уравнение e^x - 6*x = 3 методом простой итерации

from sympy.solvers import solve
from sympy import Symbol, diff
from sympy.functions import exp
from sympy.utilities.lambdify import lambdify
from random import uniform
import numpy as np
import matplotlib.pyplot as plt


def solve_by_simple_iteration(a, b, expr):
    counter = 0
    x0 = uniform(a, b)
    phi = lambdify(x, expr)
    d_phi = lambdify(x, diff(expr))
    q = abs(d_phi(b))
    x1 = phi(x0)
    while abs(x1 - x0) >= ((1 - q) * EPS / q):
        x0 = x1
        x1 = phi(x0)
        counter += 1
    return x1, counter


# погрешность
EPS = 0.0001
# левая граница
a = -1
# правая граница
b = 0

# задаем символьно функцию
x = Symbol('x')
expr = exp(x) - 6*x - 3

# итерационная форма
phi = (3 - exp(x)) / (-6)

# рисуем график
x_range = np.linspace(a, b, 100)
y_range = lambdify(x, expr)(x_range)
plt.plot(x_range, y_range)
plt.show()

# находим точные корни
root = solve(expr, x)[0].evalf()
print('Exact root: ', root)

# находим приближенные корни
simple_iteration_root, count = solve_by_simple_iteration(a, b, phi)
print('Simple iteration root: ', simple_iteration_root)
print('Error value: ', abs(root - simple_iteration_root))
print('Iterations count: ', count)
