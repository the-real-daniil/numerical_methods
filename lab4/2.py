# Задание: вычислить интеграл по ф-ле средних прямоугольников и формуле трапеций
# с точностью EPS = 0.0001
from sympy import integrate, Symbol, sqrt, lambdify


def calculate_h(a, b, n):
    return (b - a) / n


def middle_rectangles(f, a, b, n):
    h = calculate_h(a, b, n)
    x = a
    x_next = a + 1 * h
    sum = 0
    for i in range(0, n):
        sum += f((x + x_next) / 2)
        x = x_next
        x_next += h
    return h * sum


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
# expr = sin(9 * x) / sqrt(x ** 3 - 1)
expr = 1 / sqrt(3 * x * x - 1)

# точный интеграл
a = 1.4
b = 2.1
integral = integrate(expr, (x, a, b)).evalf()
print('Exact integral: ', integral)
print('---------------------------------------------------------')

# число разбиений по методу Рунге (подготовка)
func = lambdify(x, expr)
n0 = 10

#  число разбиений по методу Рунге для метода средних прямоугольников
# n = runge(func, a, b, n0, EPS, middle_rectangles)
n = 5
print('n = ', n)

# интеграл методом средних прямоугольников
middle_rectangles_integral = middle_rectangles(func, a, b, n)
print('Middle rectangles integral: ', middle_rectangles_integral)
print('Error value: ', abs(middle_rectangles_integral - integral))
print('---------------------------------------------------------')

# число разбиений по методу Рунге для метода трапеций
n = runge(func, a, b, n0, EPS, trapezoids)
print('n = ', n)

# интеграл методом средних прямоугольников
trapezoids_integral = trapezoids(func, a, b, n)
print('Trapezoids integral: ', trapezoids_integral)
print('Error value: ', abs(trapezoids_integral - integral))
print('---------------------------------------------------------')
