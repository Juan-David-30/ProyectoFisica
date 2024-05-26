import math
import numpy as np
import matplotlib.pyplot as plt

def colision_momento_lineal_2d(m1, x1, y1, vx1, vy1, m2, x2, y2, vx2, vy2):
  """
  Simula una colisión bidimensional con momento lineal.

  Argumentos:
    m1: La masa del primer objeto.
    x1, y1: La posición inicial del primer objeto en el plano 2D.
    vx1, vy1: La velocidad inicial del primer objeto en el plano 2D.
    m2: La masa del segundo objeto.
    x2, y2: La posición inicial del segundo objeto en el plano 2D.
    vx2, vy2: La velocidad inicial del segundo objeto en el plano 2D.

  Retorno:
    Un tuple con las posiciones y velocidades finales de los dos objetos.
  """

  # Momento lineal total inicial
  px_total_i = m1 * vx1 + m2 * vx2
  py_total_i = m1 * vy1 + m2 * vy2

  # Ecuaciones para las velocidades finales en colisiones 2D
  vx1f = ((m1 - m2) * vx1 + 2 * m2 * vx2) / (m1 + m2)
  vy1f = ((m1 - m2) * vy1 + 2 * m2 * vy2) / (m1 + m2)
  vx2f = ((m2 - m1) * vx2 + 2 * m1 * vx1) / (m1 + m2)
  vy2f = ((m2 - m1) * vy2 + 2 * m1 * vy1) / (m1 + m2)

  # Calcular posiciones finales
  x1f = x1 + vx1f * dt
  y1f = y1 + vy1f * dt
  x2f = x2 + vx2f * dt
  y2f = y2 + vy2f * dt

  return x1f, y1f, vx1f, vy1f, x2f, y2f, vx2f, vy2f

# Definir las variables
m1 = 10
x1 = 0
y1 = 0
vx1 = 5
vy1 = 0
m2 = 20
x2 = 10
y2 = 0
vx2 = 1
vy2 = 0
dt = 0.01

# Simular la colisión
x1f, y1f, vx1f, vy1f, x2f, y2f, vx2f, vy2f = colision_momento_lineal_2d(m1, x1, y1, vx1, vy1, m2, x2, y2, vx2, vy2)

# Visualizar la simulación
t = np.arange(0, 10, dt)
x1_t = np.zeros(len(t))
y1_t = np.zeros(len(t))
x2_t = np.zeros(len(t))
y2_t = np.zeros(len(t))

x1_t[0] = x1
y1_t[0] = y1
x2_t[0] = x2
y2_t[0] = y2

for i in range(1, len(t)):
  x1_t[i] = x1_t[i - 1] + vx1f * dt
  y1_t[i] = y1_t[i - 1] + vy1f * dt
  x2_t[i] = x2_t[i - 1] + vx2f * dt
  y2_t[i] = y2_t[i - 1] + vy2f * dt

plt.plot(x1_t, y1_t, label="Objeto 1")
plt.plot(x2_t, y2_t, label="Objeto 2")
plt.legend()
plt.show()
