from sympy import Symbol, pprint, sympify


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


x_arr = [-3, 2, 5]
y_arr = [30, 5, 14]
f = lagrange(x_arr, y_arr).simplify()
pprint(f)

