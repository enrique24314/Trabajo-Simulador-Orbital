import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

G = 6.67430e-11 
M = 5.972e24     
R = 800e3        

r0 = 6771e3      
v0 = 7.67e3      
y0 = [r0, 0, 0, v0] 

dt = 10  

def ecuaciones_newton(t, y):
    r = np.sqrt(y[0]**2 + y[1]**2)
    ax = -G * M * y[0] / r**3
    ay = -G * M * y[1] / r**3
    return np.array([y[2], y[3], ax, ay])

def rk4_step(y, t, dt):
    k1 = dt * ecuaciones_newton(t, y)
    k2 = dt * ecuaciones_newton(t + dt / 2, y + k1 / 2)
    k3 = dt * ecuaciones_newton(t + dt / 2, y + k2 / 2)
    k4 = dt * ecuaciones_newton(t + dt, y + k3)
    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-2e7, 2e7)
ax.set_ylim(-2e7, 2e7)
ax.set_title("Simulación Orbital en Tiempo Real")
ax.set_xlabel("Posición en X (m)")
ax.set_ylabel("Posición en Y (m)")
ax.grid(True)

cuerpo = plt.Circle((0, 0), R, color='blue', label="Tierra")
ax.add_patch(cuerpo)

orbita_x, orbita_y = [], []
satelite, = ax.plot([], [], 'ro', label="Satélite")
orbita, = ax.plot([], [], 'r-', label="Órbita")

def init():
    satelite.set_data([], [])
    orbita.set_data([], [])
    return satelite, orbita

def update(frame):
    global y0
    y0 = rk4_step(y0, frame * dt, dt) 

    satelite.set_data([y0[0]], [y0[1]])

    orbita_x.append(y0[0])
    orbita_y.append(y0[1])
    orbita.set_data(orbita_x, orbita_y)

    return satelite, orbita

frames = iter(int, 1)  # Generador infinito
animacion = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=20)

plt.legend()
plt.show()
