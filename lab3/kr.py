from sympy import Symbol

x = Symbol('x')
y = Symbol('y')

a11 = (x*x*x + y*y*x - 26*x - 2*x*y*y - 10*y) / 2 / (x*x - y*y)
a21 = (-x*x*y - y*y*y - 26*y + 2*x*x*y + 10*x) / 2 / (x*x - y*y)

values = {x: -6.071, y: 0.952}
print('a11 = ', a11.subs(values).evalf())
print('a21 = ', a21.subs(values).evalf())

x1 = 0.971
y1 = 0.712
norm = ((x**2 + y**2)**(1/2)).subs({x: x1, y: y1}).evalf()
print("Норма = ", norm)
