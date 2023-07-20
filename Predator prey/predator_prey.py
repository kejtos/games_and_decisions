import numpy as np
from numpy import random
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import ConnectionPatch

t = np.linspace(0, 10, num=10000)

a = 1.5
b = 1.5
c = 1
d = 2

vars_0 = [1, 2]
params = [a, b, c, d]

def predator_prey(vars, t, params):
    x = vars[0]
    y = vars[1]
    a = params[0]
    b = params[1]
    c = params[2]
    d = params[3]

    dxdt  =    a*x - b*x*y
    dydt  =  c*x*y - d*y

    return [dxdt, dydt]


y = odeint(predator_prey, vars_0, t, args=(params,))

f,ax = plt.subplots(1)
line1, = ax.plot(t, y[:,0], 'b-')
line2, = ax.plot(t, y[:,1], 'r-')
plt.show()


fig,axs = plt.subplots(2,2, gridspec_kw=dict(width_ratios=[1, 3], wspace=0))
axs[0,1].set_yticklabels([])
axs[0,1].set_yticks([])
axs[0,0].set_xticklabels([])
axs[0,0].set_xticks([])
axs[1,0].set_xticklabels([])
axs[1,0].set_xticks([])
axs[1,1].set_yticklabels([])
axs[1,1].set_yticks([])
axs[0,0].set_yticklabels([])
axs[0,0].set_yticks([])
axs[1,0].set_yticklabels([])
axs[1,0].set_yticks([])

axs[0,1].set_xlim(0,10)
axs[0,1].set_ylim(0,5)

axs[1,1].set_xlim(0,10)
axs[1,1].set_ylim(0,5)

l1, = axs[0,1].plot([], [], 'b-')
l2, = axs[1,1].plot([], [], 'r-')

img_rab = plt.imread('rabbit.png')
img_fox = plt.imread('fox.png')

n = 20
sigma = 0.001
l_rab = random.permutation(np.linspace(0.0, 0.25, n) + random.uniform(-sigma, sigma, n))
b =  random.permutation(np.linspace(0.52, 0.8, n) + random.uniform(-sigma, sigma, n))
l_fox =  random.permutation(np.linspace(0.0, 0.25, n) + random.uniform(-sigma, sigma, n))
b_fox =  random.permutation(np.linspace(0.15, 0.4, n) + random.uniform(-sigma, sigma, n))
size = 0.05

ax_rab = np.array([])
for i in range(n):
    ax_rab = np.append(ax_rab, fig.add_axes([l_rab[i], b[i], size, size], anchor='NE', zorder=1))
    ax_rab[i].imshow(img_rab)
    ax_rab[i].axis('off')

ax_fox = np.array([])
for i in range(n,2*n):
    ax_fox = np.append(ax_fox, fig.add_axes([l_fox[i-n], b_fox[i-n], size, size], anchor='NE', zorder=1))
    ax_fox[i-n].imshow(img_fox)
    ax_fox[i-n].axis('off')

axs[0,0].axis('off')
axs[1,0].axis('off')

# plt.show()

xlist = []
ylist1 = []
ylist2 = []
con = ConnectionPatch((0, 1), (0, 2), "data", "data", axesA=axs[0,1], axesB=axs[1,1], color="C0", ls="dotted")
fig.add_artist(con)

gran = 10
min_rab = np.min(y[:,0])
max_rab = np.max(y[:,0])
min_fox = np.min(y[:,1])
max_fox = np.max(y[:,1])
range_rab = max_rab-min_rab
range_fox = max_fox-min_fox
int_rab = range_rab/n
int_fox = range_fox/n

n_pic = np.arange(n)
rab = min_rab + int_rab*n_pic
fox = min_fox + int_fox*n_pic

def animate(i):
    l1.set_data(t[:i*gran],y[:i*gran,0])
    l2.set_data(t[:i*gran],y[:i*gran,1])
    con.xy1 = t[i*gran], y[i*gran,0]
    con.xy2 = t[i*gran], y[i*gran,1]
    ix1 = np.max(np.where(rab < y[i*gran,0])[0])

    for j in range(min(ix1+3,20)):
        ax_rab[j].set_visible(True)
    for k in range(min(ix1+3,20),n):
        ax_rab[k].set_visible(False)

    ix2 = np.max(np.where(fox < y[i*gran,1])[0])

    for l in range(min(ix2+3,n)):
        ax_fox[l].set_visible(True)
    for m in range(min(ix2+3,n),n):
        ax_fox[m].set_visible(False)

    return l1,l2,con,

ani = FuncAnimation(fig, animate, repeat=False, blit=False, interval=1, frames=len(t)//gran)
ani.save('predator-pray.gif', PillowWriter(fps=30))
