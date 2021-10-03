from sympy import log, symbols, diff, lambdify
from math import factorial
from sympy.plotting import plot

x = symbols('x')
f = diff(log(x, 10), x, 3)
# plot(f, (x, 1, 100))


def omega(x, arr_x):
    res = 1
    for k in range(len(arr_x)):
        res *= (x - arr_x[k])
    return res


def interpolation_error(x, arr_x, n, maxx):
    return maxx / factorial(n) * abs(omega(x, arr_x))


arr_x = [1, 10, 100]
maxx = lambdify(x, f)(1)   # максимум 3-ей производной функции lg(x) на моем отрезке от 1 до 100
n = len(arr_x)
x = 50
print(maxx)
print('Погрешность интерполяции = ', interpolation_error(x, arr_x, n, maxx))
print(98000/3/log(10).evalf())

