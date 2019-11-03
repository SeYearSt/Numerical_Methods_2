import numpy as np


def f(t, u):
  res = np.sin(0.6*t)**2*np.exp(-t*t+2.5*t-1.5)-(2*t-2)*u
  return res


def u(t):
  return 0


p = 3

c2 = 1/2
a21 = 1/2

c_3 = 1
a_31 = -1
a_32 = 2

b1, b2, b3 = 1/6, 4/6, 1/6


def main():
  t_0 = 1
  T = 6
  y_0 = 10
  eps = 1e-5
  tau_0 = 0.5
  eps_M = 1e-6

  t = t_0
  y = y_0
  tau = tau_0
  e_max = 0

  print("t=", t, "y=", y, 'u(t)=', y_0, '|y-u(t)|=', y - u(t))

  v = y
  t1 = t

  pr = 1

  while True:

    if np.abs(T-t) <= eps_M:
      print('Максимальна похиюка:', e_max)
      break

 # maybe pr=1

    if pr:

      if t+tau > T:
        tau = T-t

      v = y
      t1 = t

    kf = 0

    if kf == 0:
      w = y
      y = v
      tau = tau/2
      kf = 1

    if kf == 1:
      t += tau
      kf = 2

      if kf in [1, 2]:
       k1 = f(t, y)

    k2 = f(t + c2 * tau, y + tau * a21 * k1)
    k3 = f(t + c_3 * tau, y + tau * a_31 * k1)
    y = y + tau*(b1*k1+b2*k2+b3*k3)

    if kf == 2:
      E = np.abs(y-w)/((2**p-1)*np.max(1, np.abs(y)))
      tau_H = 2*tau*min(5, np.max(0.1, 0.9*(eps/E)^(1/(p+1))))

      if E <= eps:
        t = t+tau
        y += (y-w)/(2**p-1)
        tau = tau_H

        diff = np.abs(y-u(t))

        print('t =', t, 'u(t)=', u(t), '|y-u(t)|=', diff)

        if e_max < diff:
          e_max = diff

      else:
        y = v
        t = t1
        tau = tau_H
        pr = 0


if __name__ == "__main__":
  main()


