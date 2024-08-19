import matplotlib.pyplot as plt
import numpy as np


def deriv(P):
    dPdt = 0.7*P*(1 - P/750) - 20

    return dPdt

init_P = 30
P_init_arr = np.array([])
P_res_arr = []
P_arr_temp = np.array([])
error_arr = np.array([])

t_arr = []
inp_dt = np.array([1/8, 0.25, 0.5, 1])
for i in range(len(inp_dt)):
    t_arr.append(np.arange(1, 60, inp_dt[i]))
    P_init_arr = np.append(P_init_arr, (init_P + inp_dt[i]*deriv(init_P)))

temp_P = 0
# print("Day {day}, # of fish: {n_of_fish}".format(day=1, n_of_fish=float(P_init_arr[0])))

for i in range(len(inp_dt)):
    P_arr_temp = np.copy([P_init_arr[i]])
    for j in range(len(t_arr[i])-1):
        temp_P = P_arr_temp[j] + inp_dt[i]*deriv(P_arr_temp[j])
        P_arr_temp = np.append(P_arr_temp, temp_P)

        # print("Day {day}, # of fish: {n_of_fish}".format(day=(i+2), n_of_fish=temp_P))
    P_res_arr.append(P_arr_temp)
    P_arr_temp = np.array([])

plt.plot(t_arr[0], P_res_arr[0], 'k-', linewidth=1.5, label='Dt = {dt}'.format(dt=inp_dt[0]))
plt.plot(t_arr[1], P_res_arr[1], 'g--', linewidth=1.5, label='Dt = {dt}'.format(dt=inp_dt[1]))
plt.plot(t_arr[2], P_res_arr[2], 'b.-', linewidth=1.5, label='Dt = {dt}'.format(dt=inp_dt[2]))
plt.plot(t_arr[3], P_res_arr[3], 'o-', linewidth=1.5, label='Dt = {dt}'.format(dt=inp_dt[3]))
plt.axvline(x = 13, color = 'r', label = 't = 13 days', linewidth=2)
plt.xlim(0,25)
plt.legend()
plt.xlabel('t, days')
plt.ylabel('P(t), fish')
plt.title('dP/dt = 0.7P·(1 - P/750) - 20, P(0) = 30')
plt.grid(which='both')

plt.show()