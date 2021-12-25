# решить задачу  для диф. ур-я с нач. усл-ми

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


def runge_kutt(f_arr, y0, x, h, coeffs):
    K1 = lambda x_i, y_i, z_i, u_i, func: \
        h * func(
            x_i,
            y_i,
            z_i,
            u_i,
            
        )

    K2 = lambda x_i, y_i, z_i, u_i, func: \
        h * func(
            x_i + coeffs['a2'] * h,
            y_i + coeffs['b21'] * K1(x_i, y_i, z_i, u_i, f_arr[0]),
            z_i + coeffs['b21'] * K1(x_i, y_i, z_i, u_i, f_arr[1]),
            u_i + coeffs['b21'] * K1(x_i, y_i, z_i, u_i, f_arr[2]),
            
        )

    K3 = lambda x_i, y_i, z_i, u_i, func: \
        h * func(
            x_i + coeffs['a3'] * h,
            y_i + coeffs['b31'] * K1(x_i, y_i, z_i, u_i, f_arr[0]) + coeffs['b32'] * K2(x_i, y_i, z_i, u_i, f_arr[0]),
            z_i + coeffs['b31'] * K1(x_i, y_i, z_i, u_i, f_arr[1]) + coeffs['b32'] * K2(x_i, y_i, z_i, u_i, f_arr[1]),
            u_i + coeffs['b31'] * K1(x_i, y_i, z_i, u_i, f_arr[2]) + coeffs['b32'] * K2(x_i, y_i, z_i, u_i, f_arr[2]),
        )
    res = {
        'y': [y0[0]],
        'z': [y0[1]],
        'u': [y0[2]],
    }
    keys = {
        0: 'y',
        1: 'z',
        2: 'u',
    }
    for i in range(n + 1):
        for j, f in enumerate(f_arr):
            k1 = K1(x[i], res['y'][i-1], res['z'][i-1], res['u'][i-1], f)
            k2 = K2(x[i], res['y'][i-1], res['z'][i-1], res['u'][i-1], f)
            k3 = K3(x[i], res['y'][i-1], res['z'][i-1], res['u'][i-1], f)
            res[keys[j]].append(res[keys[j]][i] + coeffs['p1']*k1 + coeffs['p2']*k2 + coeffs['p3']*k3)

    return np.array(res['y'])


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
u = Symbol('u')
z = Symbol('z')
sets = [
    z,
    u,
    (-x * (4*x - 3)*u + 2*x*z - 2*y) / x*x*(2*x - 1),
]
y0 = [
    3,
    -3,
    4,
]
f_arr = [lambdify([x, y, z, u], set) for set in sets]
a = 1
b = 3.5
x0 = 1
n = 10
p2 = -3/8
p3 = 1/8
h = calculate_h(a, b, n)
x_arr = calculate_x(a, b, n, x0)

# находим точное решение
y_exact = lambdify(x, -1/x)

# метод Рунге Кутта
coeffs = find_coeffs(p2, p3)
y_runge_kutt = runge_kutt(f_arr, y0, x_arr, h, coeffs)

table = {
    'i': np.arange(0, n + 2),
    'x[i]': x_arr,
    'точное': [y_exact(x) for x in x_arr],
    'м. Рунге Кутта': y_runge_kutt,
}

df = pd.DataFrame(data=table)

print(df)
# print("Погрешность метода Рунге-Кутта: ", difference_rate(x_arr, y_runge_kutt, y_exact))
