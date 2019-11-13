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

c_4 = 1

b1, b2, b3 = 1/6, 4/6, 1/6


def main():
  t_0 = 1
  T = 6
  y_0 = 10
  eps = 1e-5
  tau_0 = 0.5
  eps_M = 1e-4
  kf = 0

  t = t_0
  y = y_0
  tau = tau_0
  e_max = 0

  print("t=", t, "y=", y, 'u(t)=', y_0, '|y-u(t)|=', y - u(t))

  right_call = 0

  while True:

    v = y
    t1 = t
    kf = 0

    if np.abs(T-t) <= eps_M:
      break

    if kf==0:
      k1 = f(t, y)
      right_call += 1

    k2 = f(t + c2 * tau, y + tau * a21 * k1)
    right_call += 1
    k3 = f(t + c_3 * tau, y + tau * a_31 * k1)
    right_call += 1

    w = y + tau * k3
    y = y + tau*(b1*k1+b2*k2+b3*k3)

    E = np.abs(y-w)/max(1, np.abs(y))
    tauH = tau * min(0.1, 0.9*np.power((eps/E), 1.0/(p+1)))

    if E <= eps:
      error = np.abs(y - u(t))
      if e_max < error:
        e_max = error
      t += tau
      kf = 0
    else:
      y = v
      t = t1
      tau = tauH
      kf = 1

  print('Максимальна похиюка:', e_max)
  print('Кількість звертань до правої частини:', right_call)


if __name__ == "__main__":
  main()
