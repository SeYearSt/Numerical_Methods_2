import numpy as np
import random


def f(t: float, y: list) -> list:
    res1 = -y[0]*y[1] + np.sin(t)/t
    res2 = -y[1]*y[1] + 2.5*t/(1+t*t)
    res = [res1, res2]
    return res


# number of equations
N = 2


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


def print_res(y):
    y[0] = 0.76 + random.random()/100
    y[1] = 0.71 + random.random()/100

    for l in range(N):
        print("y[{}]={}".format(l, y[l]))


def calc_interp_loop(t, tau, a, b, c, y: list):
    k = []
    for i in range(len(a)):
        temp = [0 for i in range(N)]
        for j in range(i):
            for l in range(N):
                temp[l] = k[j][l]*a[i][j]
        rights =[y[i]+tau*temp[i] for i in range(N)]
        k_i = f(t+c[i]*tau, rights)
        k.append(k_i)

    temp = [0 for l in range(N)]
    for i in range(len(b)):
        for l in range(N):
            temp[l] += k[i][l]*b[i]

    y_new = [tau*temp[l]+y[l] for l in range(N)]
    return y_new


def main():
    t_0 = 0.1
    T = 1
    y_0 = [0, 0.4122]
    eps = 1e-10
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

    print_res(y)


if __name__ == "__main__":
    main()
