# Задание: вычислить несобственный интеграл, используя выделение особенности и разложение
# подынтегральной функции в степенной ряд.
# функция: sin(x) / x, интеграл от 0 от 2
from sympy import integrate, Symbol, lambdify, sin


def calculate_h(a, b, n):
    return (b - a) / n


def trapezoids(f, a, b, n):
    h = calculate_h(a, b, n)
    x = a + 1 * h
    sum = 0
    for i in range(1, n):
        sum += f(x)
        x += h
    return h/2 * (f(a) + 2*sum + f(b))


def runge(f, a, b, n0, eps, solve_integral):
    c = 1/3
    n = n0
    In = solve_integral(f, a, b, n)
    I2n = solve_integral(f, a, b, 2*n)
    while abs(I2n - In) >= c * eps:
        n += 1
        In = solve_integral(f, a, b, n)
        I2n = solve_integral(f, a, b, 2 * n)
    return n


# погрешность
EPS = 0.0001

# функция
x = Symbol('x')
expr = sin(x) / x

# точный интеграл
a = 0
b = 2
integral = integrate(expr, (x, a, b)).evalf()
print('Exact integral: ', integral)
print('---------------------------------------------------------')

# f(x) = (x − x∗)^(−p) · ψ(x)
xi = sin(x)
x_star = 0
k = x ** (-1)
xi_row = xi.series(x, x0=x_star, n=12).removeO()
print('xi(x) = ', xi_row)
g = xi.series(x, x0=x_star, n=6).removeO()
phi = (xi_row - g)
g, phi = (g * k).simplify(), (phi * k).simplify()
print('phi(x) = ', phi)
print('g(x) = ', g)
print('f(x) = g(x) + phi(x) = ', g + phi)
print('---------------------------------------------------------')

# число разбиений по методу Рунге (подготовка)
g_func = lambdify(x, g)
phi_func = lambdify(x, phi)
n0 = 5

# число разбиений по методу Рунге для метода трапеций
n_g = runge(g_func, a, b, n0, EPS, trapezoids)
n_f = runge(phi_func, a, b, n0, EPS, trapezoids)

# интеграл методом средних прямоугольников
trapezoids_integral_g = trapezoids(g_func, a, b, n_g)
trapezoids_integral_f = trapezoids(phi_func, a, b, n_f)
trapezoids_integral = trapezoids_integral_g + trapezoids_integral_f
print('Trapezoids integral f(x): ', trapezoids_integral)
print('Error value: ', abs(trapezoids_integral - integral))
print('---------------------------------------------------------')
