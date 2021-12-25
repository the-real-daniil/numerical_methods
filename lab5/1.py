# решить ОДУ 1-го порядка

from sympy.solvers import solve
from sympy import Symbol, symbols
from sympy.utilities.lambdify import lambdify
import numpy as np
import pandas as pd


def calculate_h(a, b, n):
    return (b - a) / n


def calculate_x(a, b, n, x0):
    x = [x0]
    h = calculate_h(a, b, n)
    for i in range(n + 1):
        x.append(x0 + i * h)
    return x


def explicit_euler(f, y0, x, h):
    y = [y0]
    for i in range(n + 1):
        y.append(y[i] + h * f(x[i], y[i]))
    return y


def implicit_euler(f, y0, x, h):
    y = [y0]
    for i in range(n + 1):
        y_wave = y[i] + h * f(x[i], y[i])
        y.append(y[i] + h * f(x[i + 1], y_wave))
    return y


def hoyne(f, y0, x, h):
    y = [y0]
    for i in range(n + 1):
        y_wave = y[i] + h * f(x[i], y[i])
        y.append(y[i] + (h/2) * (f(x[i], y[i]) + f(x[i + 1], y_wave)))
    return y


def runge_kutt(f, y0, x, h, coeffs):
    k1, k2, k3 = 0, 0, 0
    y = [y0]
    for i in range(n + 1):
        k1 = h * f(x[i], y[i])
        k2 = h * f(x[i] + coeffs['a2'] * h, y[i] + coeffs['b21'] * k1)
        k3 = h * f(x[i] + coeffs['a3'] * h, y[i] + coeffs['b31'] * k1 + coeffs['b32'] * k2)
        y.append(y[i] + coeffs['p1'] * k1 + coeffs['p2'] * k2 + coeffs['p3'] * k3)
    return y


def difference_rate(x, y, y_ex):
    norm = 0
    for i in range(len(y)):
        norm += (y_ex(x[i]) - y[i])**2
    return norm**(1/2)


def find_coeffs(p2, p3):
    res = {'p2': p2, 'p3': p3}
    p1, a2, a3, b21, b31, b32 = symbols('p1, a2, a3, b21, b31, b32')

    sets = [
        p3 * a3 + p2 * a2 - 1/2,
        p1 + p2 + p3 - 1,
        a2 - b21,
        a3 - b31 - b32,
        a3 * (a3 - a2) - b32 * a2 * (2 - 3 * a2),
        p3 * b32 * a2 - 1/6,
    ]
    names = [p1, a2, a3, b21, b31, b32]

    k = solve(sets, names)[0]
    for i in range(len(k)):
        res[str(names[i])] = k[i]

    return res


# задаем символьно функцию
x = Symbol('x')
y = Symbol('y')
expr = (3 + 2*x*y) / (x*x)
f = lambdify([x, y], expr)
a = 1
b = 1.5
y0 = -1
x0 = 1
n = 10
p2 = 2/3
p3 = 1/3
h = calculate_h(a, b, n)
x_arr = calculate_x(a, b, n, x0)

# находим точное решение
y_exact = lambdify(x, -1/x)

# явный метод  Эйлера
y_explicit_euler = explicit_euler(f, y0, x_arr, h)

# неявный метод  Эйлера
y_implicit_euler = implicit_euler(f, y0, x_arr, h)

# метод Хойне
y_hoyne = hoyne(f, y0, x_arr, h)

# метод Рунге Кутта
coeffs = find_coeffs(p2, p3)
y_runge_kutt = runge_kutt(f, y0, x_arr, h, coeffs)


table = {
    'i': np.arange(0, n + 2),
    'x[i]': x_arr,
    'точное': [y_exact(x) for x in x_arr],
    'явный м. Эйлера': y_explicit_euler,
    'н./я. м. Эйлера': y_implicit_euler,
    'м. Хойна': y_hoyne,
    'м. Рунге Кутта': y_runge_kutt,
}

df = pd.DataFrame(data=table)

print(df)
print("Погрешность явного метода Эйлера: ", difference_rate(x_arr, y_explicit_euler, y_exact))
print("Погрешность неявного метода Эйлера: ", difference_rate(x_arr, y_implicit_euler, y_exact))
print("Погрешность метода Хойна: ", difference_rate(x_arr, y_hoyne, y_exact))
print("Погрешность метода Рунге-Кутта: ", difference_rate(x_arr, y_runge_kutt, y_exact))
