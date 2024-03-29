import numpy as np
import matplotlib.pyplot as plt


def f(t, u):
    res = np.sin(0.6 * t) ** 2 * np.exp(-t * t + 2.5 * t - 1.5) - (2 * t - 4) * u
    return res


def u(t):
    res = np.exp(-t * t + 5 / 2 * t - 3 / 2) * (
                -1 / 3 + 25 / 123 * np.cos(6 * t / 5) - 20 / 123 * np.sin(6 * t / 5)) - np.exp(-t * t + 4 * t - 3) * (
                      -31 / 3 + 25 / 123 * np.cos(6 / 5) - 20 / 123 * np.sin(6 / 5))
    return res


Y = []
X = []

# 3 порядок
p1 = 3
a1 = [[0, 0], [0.5, 0], [-1, 2]]
c1 = [0, 0.5, 1]
b1 = [1/6, 4/6, 1/6]


# 4 порядок
p2 = 4
a2 = [[0, 0, 0], [0.5, 0, 0], [0, 0.5, 0], [0, 0, 1]]
c2 = [0, 0.5, 0.5, 1]
b2 = [1/6, 2/6, 2/6, 1/6]


def calc_interp(t, tau, coeffs, y, k1):
    rigth_calls = 0
    k = [k1]
    for i, coeff in enumerate(coeffs[:-1]):
        right_part = y+np.sum(np.array(coeff[1])*np.array(k))*tau
        print('right_part', right_part)
        k_i = f(t+coeff[0]*tau, right_part)
        print('k_i', k_i)
        rigth_calls += 1
        k.append(k_i)

        # print(k_i)
    k = np.array(k)
    b = np.array(coeffs[-1])
    y_new = y + tau * np.sum(k*b)
    return y_new, rigth_calls


def calc_interp_loop(t, tau, a, b, c, y):
    k = []
    for i in range(len(a)):
        temp = 0
        for j in range(i):
            temp += k[j]*a[i][j]
        right = y+tau*temp
        k_i = f(t+c[i]*tau, right)
        k.append(k_i)

    temp = 0
    for i in range(len(b)):
        temp += k[i]*b[i]
    y_new = tau*temp+y

    return y_new, 0


def main():
    t_0 = 1
    T = 6
    y_0 = 10
    eps = 1e-4
    tau_0 = 0.05
    eps_M = 1e-4

    t = t_0
    y = y_0
    tau = tau_0
    e_max = 0
    errors = []

    kf = 0

    while True:

        if np.abs(T - t) <= eps_M:
            break

        if kf == 0:
            v = y
            t1 = t

        w, temp_2 = calc_interp_loop(t, tau, a1, b1, c1, y)
        y, temp_2 = calc_interp_loop(t, tau, a2, b2, c2, y)

        E = np.abs(y - w) / max(1, np.abs(y))
        tauH = tau * min(0.1, 0.9 * np.power((eps / E), 1.0 / (p1 + 1)))
        if E <= eps:
            Y.append(y)
            X.append(t)
            error = np.abs(y - u(t))
            errors.append(error)
            # print('tau', tau)
            if e_max < error:
                e_max = error
                # print('e_max', e_max)
                # print('t', t)

            t += tau
            print('точний ровзязок', u(t))
            print('наближенний розвязок', y)
            kf = 0
        else:
            y = v
            t = t1
            tau = tauH
            kf = 1

    print('Максимальна похиюка:', e_max)
    for i, x in enumerate(X):
        print('t:{}, y:{}, u:{}, [y-u(t)]:{}'.format(x, Y[i], u(x), errors[i]))


def plot_roots():
    x = np.array(X)
    root = u(x)
    plt.plot(x, Y)
    plt.plot(x, root)
    # plt.savefig('graph.png')
    plt.show()


if __name__ == "__main__":
    main()
    plot_roots()
