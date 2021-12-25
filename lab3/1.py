# методом Ньютона решить нелинейное уравнение ln(x) − 1/x^2 = 0

from sympy.solvers import solve
from sympy import Symbol, diff
from sympy.utilities.lambdify import lambdify
import numpy as np
import matplotlib.pyplot as plt

# погрешность
EPS = 0.5

# задаем символьно функцию
x = Symbol('x')
expr = 2*x*x*x - 5*x*x - 14*x + 8
a = 2
b = 5

# рисуем график
x_range = np.linspace(0.1, a, b)
y_range = lambdify(x, expr)(x_range)
plt.plot(x_range, y_range)
plt.show()

# находим точные корни
root = solve(expr, x)[1].evalf()
print('Exact root: ', root)


# находит корни методом Ньютона с погрешностью EPS
def solve_by_newton_method(expr, a, b):
    counter = 0
    f = lambdify(x, expr)
    df = lambdify(x, diff(expr))
    x0 = 2.5
    if df(a) * f(x0) > 0:
        x0 = a
    else:
        x0 = b
    x1 = x0 - f(x0)/df(x0)
    while abs(x1 - x0) >= EPS:
        counter += 1
        x0 = x1
        x1 = x0 - f(x0) / df(x0)
    return x1, counter


newton_root, count = solve_by_newton_method(expr, a, b)
print('Newton root: ', newton_root)
print('Error value: ', abs(root - newton_root))
print('Iterations count: ', count)
