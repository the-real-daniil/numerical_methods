def f_star(a, b, c, d, m):
    return a ** 0.5 - m * b / (c + d)


def f_delta(a, b, c, d, m, d_a, d_b, d_d, d_c, d_m):
    first = d_a / 2 / a ** 0.5
    numerator = (c + d) * (m * d_b + b * d_m) + m * b * (d_c + d_d)
    denominator = (c + d) * (c + d)
    second = numerator / denominator
    return first + second


def f_sigma(f_star, f_delta):
    return f_delta / f_star * 100


if __name__ == '__main__':
    a = 139.82
    d_a = 0.02
    b = 1.756
    d_b = 0.0005
    c = 5.2
    d_c = 0.04
    d = 0.94
    d_d = 0.01
    m = 1.0435
    d_m = 0.0002

    f_star_val = f_star(a, b, c, d, m)
    f_delta_val = f_delta(a, b, c, d, m, d_a, d_b, d_d, d_c, d_m)
    f_sigma_val = f_sigma(f_star_val, f_delta_val)

    print('F* = ', f_star_val)
    print('dF = ', f_delta_val)
    print('sigmaF = ', f_sigma_val)
