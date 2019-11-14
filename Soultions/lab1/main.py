import numpy as np
import matplotlib.pyplot as plt

def f(t, u):
  res = np.sin(0.6*t)**2*np.exp(-t*t+2.5*t-1.5)-(2*t-2)*u
  return res


def u(t):
  res = np.exp(-t*t+5/2*t-3/2)*(-1/3+25/123*np.cos(6*t/5) - 20/123*np.sin(6*t/5)) - np.exp(-t*t+4*t-3)*(-31/3 + 25/123*np.cos(6/5)-20/123*np.sin(6/5))
  return res


Y = []
X = []

# 3 порядок
p1 = 3
c2_1 = 1/2
a21_1 = 1/2

c_3_1 = 1
a_31_1 = -1
a_32_1 = 2

c_4_1 = 1

b1_1, b2_1, b3_1 = 1/6, 4/6, 1/6

# 4 порядок 
p2 = 4
c2_2 = 1/2
a21_2 = 1/2

c_3_2 = 1/2
a_31_2 = 0
a_32_2 = 1/2

c_4_2 = 1
c_4_3 = 0
c_4_4 = 0
c_4_5 = 1

b1_2, b2_2, b3_2, b4_2 = 1/6, 2/6, 2/6, 1/6

def main():
  t_0 = 1
  T = 6
  y_0 = 10
  eps = 1e-4
  tau_0 = 0.5
  eps_M = 1e-4

  t = t_0
  y = y_0
  tau = tau_0
  e_max = 0

  print("t=", t, "y=", y, 'u(t)=', y_0, '|y-u(t)|=', y - u(t))

  right_call = 0

  kf = 0

  while True:

    if np.abs(T-t) <= eps_M:
      break

    if kf == 0:
      v = y
      t1 = t


    k1 = f(t, y)
    right_call += 1
    k2_1 = f(t + c2_1 * tau, y + tau * a21_1 * k1)
    right_call += 1
    k3_1 = f(t + c_3_1 * tau, y + tau * a_31_1 * k1)
    right_call += 1

    k2_2 = f(t + c2_2 * tau, y + tau * a21_2 * k1)
    right_call += 1
    k3_2 = f(t + c_3_2 * tau, y + tau * a_31_2 * k1)
    right_call += 1
    k4_2 = f(t + c_3_2 * tau, y + tau * a_31_2 * k1)
    right_call += 1

    w = y + tau*(b1_1*k1+b2_1*k2_1+b3_1*k3_1)
    y = y + tau*(b1_2*k1+b2_2*k2_2+b3_2*k3_2+b4_2*k4_2)

    # print('w', 'y')
    # print(w, y)
    

    E = np.abs(y-w)/max(1, np.abs(y))
    # print('E', E)
    tauH = tau * min(0.1, 0.9*np.power((eps/E), 1.0/(p2+1)))
    # print('E', E, 'eps', eps)
    if E <= eps:
      Y.append(y)
      X.append(t)
      error = np.abs(y - u(t))
      # print('t', t)
      if e_max < error:
        e_max = error
        print('e_max', e_max)
        print('t=', t)

      t += tau
      # print('точний ровзязок', u(t))
      # print('наближенний розвязок', y)
      kf = 0
    else:
      y = v
      t = t1
      tau = tauH
      kf = 1


  print('Максимальна похиюка:', e_max)
  print('Кількість звертань до правої частини:', right_call)

def plot_roots():
  x = np.array(X)
  root = u(x)
  plt.plot(x, Y)
  plt.plot(x, root)
  plt.savefig('graph.png')


if __name__ == "__main__":
  main()
  plot_roots()
