import numpy as np


def f(t: float, y: list) -> list:
    res1 = -y[0]*y[1] + np.sin(t)/t
    res2 = -y[1]*y[1] + 2.5*t/(1+t*t)
    res = [res1, res2]
    return res


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


def calc_interp_loop(t, tau, a, b, c, y: list):
    k = []
    for i in range(len(a)):
        temp = [0, 0]
        for j in range(i):
            temp[0] += k[j][0]*a[i][j]
            temp[1] += k[j][1]*a[i][j]
        # right = y+tau*temp
        right_0 = y[0]+tau*temp[0]
        right_1 = y[1]+tau*temp[1]
        rights = [right_0, right_1]
        # k_i = f(t+c[i]*tau, right)
        k_i = f(t+c[i]*tau, rights)
        k.append(k_i)

    temp = [0, 0]
    for i in range(len(b)):
        temp[0] += k[i][0]*b[i]
        temp[1] += k[i][1]*b[i]

    y_new_0 = tau*temp[0]+y[0]
    y_new_1 = tau*temp[1]+y[1]
    y_new = [y_new_0, y_new_1]

    return y_new


def main():
    t_0 = 1
    T = 6
    y_0 = [0, 0.4122]
    eps = 1e-4
    tau_0 = 0.05
    eps_M = 1e-4

    t = t_0
    y = y_0
    tau = tau_0

    kf = 0

    while True:

        if np.abs(T - t) <= eps_M:
            break

        if kf == 0:
            v = y
            t1 = t

        w = calc_interp_loop(t, tau, a1, b1, c1, y)
        y = calc_interp_loop(t, tau, a2, b2, c2, y)

        t += tau

        up = max([np.abs(y[i]-w[i]) for i in range(len(y))])
        down = max(1, max(y))

        E = up/down
        tauH = tau * min(0.1, 0.9 * np.power((eps / E), 1.0 / (p1 + 1)))
        if E <= eps:
            t += tau
            kf = 0
        else:
            y = v
            t = t1
            tau = tauH
            kf = 1


if __name__ == "__main__":
    main()
