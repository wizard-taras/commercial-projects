import matplotlib.pyplot as plt
import numpy as np


def derivP(P, G):
    dPdt = 0.7*P*(1 - P/100) - 0.04*P*G

    return dPdt

def derivG(P, G):
    dGdt = 0.008*P*G - 0.25*G

    return dGdt

init_P = 20
init_G = 5

P_init_arr = np.array([])
G_init_arr = np.array([])
P_temp_arr = np.array([])
G_temp_arr = np.array([])
deriv_P_temp_arr = np.array([])
deriv_G_temp_arr = np.array([])

X_arr = [[], []]
F_arr = [[], []]

t_arr = []
inp_dt = np.array([1, 1/2, 1/4, 1/8, 1/16])
for i in range(len(inp_dt)):
    t_arr.append(np.arange(1, 100, inp_dt[i]))
    P_init_arr = np.append(P_init_arr, (init_P + inp_dt[i]*derivP(init_P, init_G)))
    G_init_arr = np.append(G_init_arr, (init_G + inp_dt[i]*derivG(init_P, init_G)))

temp_P = 0
temp_G = 0

for i in range(len(inp_dt)):
    P_temp_arr = np.copy([P_init_arr[i]])
    G_temp_arr = np.copy([G_init_arr[i]])

    deriv_P_temp_arr = np.array([derivP(init_P, init_G)])
    deriv_G_temp_arr = np.array([derivG(init_P, init_G)])
    for j in range(len(t_arr[i])-1):
        deriv_P_temp = derivP(P_temp_arr[j], G_temp_arr[j])
        deriv_G_temp = derivG(P_temp_arr[j], G_temp_arr[j])

        deriv_P_temp_arr = np.append(deriv_P_temp_arr, deriv_P_temp)
        deriv_G_temp_arr = np.append(deriv_G_temp_arr, deriv_G_temp)

        temp_P = P_temp_arr[j] + inp_dt[i]*deriv_P_temp
        P_temp_arr = np.append(P_temp_arr, temp_P)
        temp_G = G_temp_arr[j] + inp_dt[i]*deriv_G_temp
        G_temp_arr = np.append(G_temp_arr, temp_G)

    X_arr[0].append(P_temp_arr)
    X_arr[1].append(G_temp_arr)

    F_arr[0].append(deriv_P_temp_arr)
    F_arr[1].append(deriv_G_temp_arr)

    P_temp_arr = np.array([])
    G_temp_arr = np.array([])
    deriv_P_temp_arr = np.array([])
    deriv_G_temp_arr = np.array([])

# Main plot, P(t) & G(t) vs t
main_plot = plt.figure(1)
plt.plot(t_arr[0], X_arr[0][0], 'k-', linewidth=1.5, label='P(t), Dt = {dt}'.format(dt=inp_dt[0]))
plt.plot(t_arr[0], X_arr[1][0], 'k--', linewidth=1.5, label='G(t), Dt = {dt}'.format(dt=inp_dt[0]))
plt.plot(t_arr[1], X_arr[0][1], 'g-', linewidth=1.5, label='P(t), Dt = {dt}'.format(dt=inp_dt[1]))
plt.plot(t_arr[1], X_arr[1][1], 'g--', linewidth=1.5, label='G(t), Dt = {dt}'.format(dt=inp_dt[1]))
plt.plot(t_arr[2], X_arr[0][2], 'b-', linewidth=1.5, label='P(t), Dt = {dt}'.format(dt=inp_dt[2]))
plt.plot(t_arr[2], X_arr[1][2], 'b--', linewidth=1.5, label='G(t), Dt = {dt}'.format(dt=inp_dt[2]))
plt.plot(t_arr[3], X_arr[0][3], 'm-', linewidth=1.5, label='P(t), Dt = {dt}'.format(dt=inp_dt[3]))
plt.plot(t_arr[3], X_arr[1][3], 'm--', linewidth=1.5, label='G(t), Dt = {dt}'.format(dt=inp_dt[3]))
plt.plot(t_arr[4], X_arr[0][4], 'r-', linewidth=1.5, label='P(t), Dt = {dt}'.format(dt=inp_dt[4]))
plt.plot(t_arr[4], X_arr[1][4], 'r--', linewidth=1.5, label='G(t), Dt = {dt}'.format(dt=inp_dt[4]))
# plt.axvline(x = 13, color = 'r', label = 't = 13 days', linewidth=2)
# plt.xlim(0,25)
plt.legend()
plt.xlabel('t, days')
plt.ylabel('P(t), G(t), fish')
plt.title('')
plt.grid(which='both')

# dP/dt & dG/dt vs t plot
deriv_plot = plt.figure(2)
plt.plot(t_arr[0], F_arr[0][0], 'k-', linewidth=1.5, label='dP/dt, Dt = {dt}'.format(dt=inp_dt[0]))
plt.plot(t_arr[0], F_arr[1][0], 'k--', linewidth=1.5, label='dG/dt, Dt = {dt}'.format(dt=inp_dt[0]))
plt.plot(t_arr[1], F_arr[0][1], 'g-', linewidth=1.5, label='dP/dt, Dt = {dt}'.format(dt=inp_dt[1]))
plt.plot(t_arr[1], F_arr[1][1], 'g--', linewidth=1.5, label='dG/dt, Dt = {dt}'.format(dt=inp_dt[1]))
plt.plot(t_arr[2], F_arr[0][2], 'b-', linewidth=1.5, label='dP/dt, Dt = {dt}'.format(dt=inp_dt[2]))
plt.plot(t_arr[2], F_arr[1][2], 'b--', linewidth=1.5, label='dG/dt, Dt = {dt}'.format(dt=inp_dt[2]))
plt.plot(t_arr[3], F_arr[0][3], 'm-', linewidth=1.5, label='dP/dt, Dt = {dt}'.format(dt=inp_dt[3]))
plt.plot(t_arr[3], F_arr[1][3], 'm--', linewidth=1.5, label='dG/dt, Dt = {dt}'.format(dt=inp_dt[3]))
plt.plot(t_arr[4], F_arr[0][4], 'r-', linewidth=1.5, label='dP/dt, Dt = {dt}'.format(dt=inp_dt[4]))
plt.plot(t_arr[4], F_arr[1][4], 'r--', linewidth=1.5, label='dG/dt, Dt = {dt}'.format(dt=inp_dt[4]))
plt.legend()
plt.xlabel('t, days')
plt.ylabel('dP/dt, dG/dt, per day')
plt.title('')
plt.grid(which='both')

# Phase plane (P(t) vs G(t)) plot
phase_plane_plot = plt.figure(3)
plt.plot(X_arr[0][0], X_arr[1][0], 'k-', linewidth=1.5, label='Dt = {dt}'.format(dt=inp_dt[0]))
plt.plot(X_arr[0][1], X_arr[1][1], 'k--', linewidth=1.5, label='Dt = {dt}'.format(dt=inp_dt[1]))
plt.plot(X_arr[0][2], X_arr[1][2], 'g-', linewidth=1.5, label='Dt = {dt}'.format(dt=inp_dt[2]))
plt.plot(X_arr[0][3], X_arr[1][3], 'g--', linewidth=1.5, label='Dt = {dt}'.format(dt=inp_dt[3]))
plt.legend()
plt.xlim(0,70)
plt.ylim(0,20)
plt.xlabel('P(t)')
plt.ylabel('G(t)')
plt.title('Phase plane')
plt.grid(which='both')
plt.show()


# Error estimation
error = 1e6
error_limit = 1 # Insert the desired error limit (precision)
error_arr = []
i = 0
t_arr = []
t_eq_arr = []
stepsize = 1
stepsize_prev = stepsize
stepsize_arr = []

P_temp_arr = np.array([])
G_temp_arr = np.array([])
X_arr = [[], []]
P_init_arr = np.array([])
G_init_arr = np.array([])
P_init_arr = np.append(P_init_arr, (init_P + stepsize*derivP(init_P, init_G)))
G_init_arr = np.append(G_init_arr, (init_G + stepsize*derivG(init_P, init_G)))

while error > error_limit:
    stepsize_arr.append(stepsize)
    P_temp_arr = np.copy([P_init_arr])
    G_temp_arr = np.copy([G_init_arr])
    t_arr.append(np.arange(1, 100, stepsize))

    for j in range(len(t_arr[i])-1):
        deriv_P_temp = derivP(P_temp_arr[j], G_temp_arr[j])
        deriv_G_temp = derivG(P_temp_arr[j], G_temp_arr[j])

        temp_P = P_temp_arr[j] + stepsize*deriv_P_temp
        P_temp_arr = np.append(P_temp_arr, temp_P)
        temp_G = G_temp_arr[j] + stepsize*deriv_G_temp
        G_temp_arr = np.append(G_temp_arr, temp_G)

    X_arr[0].append(P_temp_arr)
    X_arr[1].append(G_temp_arr)

    P_temp_arr = np.array([])
    G_temp_arr = np.array([])

    t_eq = np.nonzero(X_arr[0][i] >= 32)
    
    print("Stepsize: {dt}\n".format(dt=stepsize))
    print(t_eq)
    print("\n")
    t_eq_arr.append(t_eq)

    # Estimating error of the Euler's method:
    if len(X_arr[0]) >= 2:
        error = X_arr[0][i][int((6/stepsize) - 1)] - X_arr[0][i-1][int((6/stepsize_prev) - 1)] # 6 because on this day dP/dt has the biggest value
        if error < 0:
            error = 1e6
            stepsize_prev = stepsize
            stepsize = stepsize/2
            continue
        error_arr.append(error)

    i += 1
    stepsize_prev = stepsize
    stepsize = stepsize/2

    P_init_arr = np.array([])
    G_init_arr = np.array([])
    P_init_arr = np.append(P_init_arr, (init_P + stepsize*derivP(init_P, init_G)))
    G_init_arr = np.append(G_init_arr, (init_G + stepsize*derivG(init_P, init_G)))