# решить уравнение 2*lg(x) - x/2 = -1 методом секущих

from sympy.solvers import solve
from sympy import Symbol, log
from sympy.utilities.lambdify import lambdify
from random import uniform
import numpy as np
import matplotlib.pyplot as plt

# погрешность
EPS = 0.001

# задаем символьно функцию
x = Symbol('x')
expr = 2*log(x, 10) - x/2 + 1

# рисуем график
x_range = np.linspace(0.1, 1, 100)
y_range = lambdify(x, expr)(x_range)
plt.plot(x_range, y_range)
plt.show()

# находим точные корни
root = solve(expr, x)[0].evalf()
print('Exact root: ', root)


# находит корни методом Ньютона с погрешностью EPS
def solve_by_secant_method(expr, a, b):
    counter = 0
    f = lambdify(x, expr)
    x0 = uniform(a, b)
    x1 = uniform(a, b)
    x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
    while abs(x2 - x1) >= EPS:
        counter += 1
        x0 = x1
        x1 = x2
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))

    return x2, counter


secant_root, count = solve_by_secant_method(expr, 0.1, 0.5)
print('Secant root: ', secant_root)
print('Error value: ', abs(root - secant_root))
print('Iterations count: ', count)
