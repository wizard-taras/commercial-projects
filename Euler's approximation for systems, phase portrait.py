import matplotlib.pyplot as plt
import numpy as np


def derivP(P, G):
    dPdt = 0.7*P*(1 - P/100) - 0.04*P*G

    return dPdt

def derivG(P, G):
    dGdt = 0.008*P*G - 0.25*G

    return dGdt

init_P = [1, 20, 70, 120]
init_G = [55, 5, 10, 1]

P_init_arr = np.array([])
G_init_arr = np.array([])
P_temp_arr = np.array([])
G_temp_arr = np.array([])
deriv_P_temp_arr = np.array([])
deriv_G_temp_arr = np.array([])

X_arr = [[], []]
F_arr = [[], []]

inp_dt = 1/8
t_arr = np.arange(1, 100, inp_dt)
for i in range(len(init_P)):
    P_init_arr = np.append(P_init_arr, (init_P[i] + inp_dt*derivP(init_P[i], init_G[i])))
    G_init_arr = np.append(G_init_arr, (init_G[i] + inp_dt*derivG(init_P[i], init_G[i])))

temp_P = 0
temp_G = 0

for i in range(len(init_P)):
    P_temp_arr = np.copy([P_init_arr[i]])
    G_temp_arr = np.copy([G_init_arr[i]])

    deriv_P_temp_arr = np.array([derivP(init_P[i], init_G[i])])
    deriv_G_temp_arr = np.array([derivG(init_P[i], init_G[i])])
    for j in range(len(t_arr)-1):
        deriv_P_temp = derivP(P_temp_arr[j], G_temp_arr[j])
        deriv_G_temp = derivG(P_temp_arr[j], G_temp_arr[j])

        deriv_P_temp_arr = np.append(deriv_P_temp_arr, deriv_P_temp)
        deriv_G_temp_arr = np.append(deriv_G_temp_arr, deriv_G_temp)

        temp_P = P_temp_arr[j] + inp_dt*deriv_P_temp
        P_temp_arr = np.append(P_temp_arr, temp_P)
        temp_G = G_temp_arr[j] + inp_dt*deriv_G_temp
        G_temp_arr = np.append(G_temp_arr, temp_G)

    X_arr[0].append(P_temp_arr)
    X_arr[1].append(G_temp_arr)

    F_arr[0].append(deriv_P_temp_arr)
    F_arr[1].append(deriv_G_temp_arr)

    P_temp_arr = np.array([])
    G_temp_arr = np.array([])
    deriv_P_temp_arr = np.array([])
    deriv_G_temp_arr = np.array([])

plt.plot(X_arr[0][0], X_arr[1][0], 'k-', linewidth=1.5, label='P(0)={P0}, G(0)={G0}'.format(P0=init_P[0], G0=init_G[0]))
plt.plot(X_arr[0][1], X_arr[1][1], 'k--', linewidth=1.5, label='P(0)={P0}, G(0)={G0}'.format(P0=init_P[1], G0=init_G[1]))
plt.plot(X_arr[0][2], X_arr[1][2], 'g-', linewidth=1.5, label='P(0)={P0}, G(0)={G0}'.format(P0=init_P[2], G0=init_G[2]))
plt.plot(X_arr[0][3], X_arr[1][3], 'g--', linewidth=1.5, label='P(0)={P0}, G(0)={G0}'.format(P0=init_P[3], G0=init_G[3]))
plt.legend()
# plt.xlim(0,70)
plt.ylim(0,20)
plt.xlabel('P(t)')
plt.ylabel('G(t)')
plt.title('Phase plane')
plt.grid(which='both')
plt.show()