import matplotlib.pyplot as plt
import numpy as np



def deriv(P):
    dPdt = 0.7*P*(1 - P/750) - 20

    return dPdt

init_P = 30
P_init = 0
P_res_arr = []
P_arr_temp = np.array([])
P_init_arr = np.array([])
error = 1e6
error_limit = 1 # Insert the desired error limit (precision)
error_arr = []
i = 0

t_arr = []
t_eq_arr = []
stepsize = 1
stepsize_prev = stepsize
stepsize_arr = []
P_init_arr = np.append(P_init_arr, (init_P + stepsize*deriv(init_P)))

temp_P = 0

while error > error_limit:
    stepsize_arr.append(stepsize)
    P_arr_temp = np.copy([P_init_arr])
    t_arr.append(np.arange(1, 60, stepsize))

    for j in range(len(t_arr[i])-1):
        temp_P = P_arr_temp[j] + stepsize*deriv(P_arr_temp[j])
        P_arr_temp = np.append(P_arr_temp, temp_P)

    P_res_arr.append(P_arr_temp)
    P_arr_temp = np.array([])

    t_eq = np.nonzero(P_res_arr[i] >= 720)
    
    print("Stepsize: {dt}\n".format(dt=stepsize))
    print(t_eq)
    print("\n")
    t_eq_arr.append(t_eq)

    # Estimating error of the Euler's method:
    if len(P_res_arr) >= 2:
        error = P_res_arr[i][int((13/stepsize) - 1)] - P_res_arr[i-1][int((13/stepsize_prev) - 1)] # 13 because on this day dP/dt has the biggest value
        error_arr.append(error)

    i += 1
    stepsize_prev = stepsize
    stepsize = stepsize/2

    P_init_arr = np.array([])
    P_init_arr = np.append(P_init_arr, (init_P + stepsize*deriv(init_P)))


plt.plot(stepsize_arr[1:], error_arr, 'k.-', linewidth=1.5)
# plt.xlim(0,25)
plt.xlabel('dt, days')
plt.ylabel(r'$e_{\Delta t}$, fish')
plt.title(r'Error estimation $(e_{\Delta t} < 1)$')
plt.grid(which='both')

plt.show()