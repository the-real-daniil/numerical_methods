from newton import *
from sympy import diff

def values(x_arr, func):
    n = len(x_arr)
    res = np.zeros(n)
    for i in range(n):
        res[i] = func.subs(Symbol('x'), x_arr[i])
    return res


def divided_difference(x1, x2, f1, f2):
    print('x1 = ', x1)
    print('x2 = ', x2)
    print('f1 = ', f1)
    print('f2 = ', f2)
    return (f2 - f1) / (x2 - x1)


def make_hermite_polynomial(matrix):
    x = Symbol('x')
    n = len(matrix)
    expr = sympify('0')
    k = 1
    for i in range(n):
        expr += matrix[0][i + 1] * k
        k *= (x - matrix[i][0])
    return expr


def make_hermite_matrix(x, y, dy):
    n = len(x) + 1
    res = np.zeros((n, n + 1))
    for j in range(n + 1):
        for i in range(n):
            if j > 1 and i > n - j:
                break
            if j == 0:
                if i == 0:
                    res[i][j] = x[0]
                else:
                    res[i][j] = x[i - 1]
            elif j == 1:
                if i == 0:
                    res[i][j] = y[0]
                else:
                    res[i][j] = y[i - 1]
            else:
                print('i, j = ', i, j)
                if j == 2 and i == 0:
                    res[i][j] = dy[0]
                else:
                    res[i][j] = divided_difference(res[i][0], res[i + j - 1][0], res[i][j - 1], res[i + 1][j - 1])
    return res


table = create_table(y_arr)
newton_polynomial = newton_polynomial_backward(table, x_arr, h).simplify()

pprint(newton_polynomial)
func_values = values(x_arr, newton_polynomial)
diff_values = values(x_arr, diff(newton_polynomial))

my_chunk = np.concatenate((x_arr[0:3], func_values[0:3], diff_values[0:3]), axis=0).reshape(3, 3)
print(my_chunk)

hermite_matrix = make_hermite_matrix(my_chunk[0], my_chunk[1], my_chunk[2])
print(hermite_matrix)

hermite_polynomial = make_hermite_polynomial(hermite_matrix)
pprint(hermite_polynomial)

x = Symbol('x')

# интерполирующая функция Лагранжа
func_1 = lambdify(x, newton_polynomial)
x_range = np.linspace(8, 14, 100)
y_range_1 = func_1(x_range)

# интерполирующая функция Эрмита
func_2 = lambdify(x, hermite_polynomial)
x_range = np.linspace(8, 14, 100)
y_range_2 = func_2(x_range)

plt.plot(x_arr, y_arr, 'ro', x_range, y_range_1, 'y', x_range, y_range_2, 'g')
plt.show()
