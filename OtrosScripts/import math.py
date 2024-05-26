import math
import numpy as np
import matplotlib.pyplot as plt

def colision_momento_lineal_2d(m1, x1, y1, vx1, vy1, m2, x2, y2, vx2, vy2, tipo_colision):
  """
  Simula una colisión bidimensional con momento lineal.

  Argumentos:
    m1: La masa del primer objeto.
    x1, y1: La posición inicial del primer objeto en el plano 2D.
    vx1, vy1: La velocidad inicial del primer objeto en el plano 2D.
    m2: La masa del segundo objeto.
    x2, y2: La posición inicial del segundo objeto en el plano 2D.
    vx2, vy2: La velocidad inicial del segundo objeto en el plano 2D.
    tipo_colision: El tipo de colisión ("Elástica" o "Inelástica").

  Retorno:
    Un tuple con las posiciones y velocidades finales de los dos objetos.
  """

  # Momento lineal total inicial
  px_total_i = m1 * vx1 + m2 * vx2
  py_total_i = m1 * vy1 + m2 * vy2

  # Si la colisión es elástica, se conserva la energía cinética
  if tipo_colision == "Elástica":
    # Ecuaciones para las velocidades finales en colisiones elásticas 2D
    vx1f = ((m1 - m2) * vx1 + 2 * m2 * vx2) / (m1 + m2)
    vy1f = ((m1 - m2) * vy1 + 2 * m2 * vy2) / (m1 + m2)
    vx2f = ((m2 - m1) * vx2 + 2 * m1 * vx1) / (m1 + m2)
    vy2f = ((m2 - m1) * vy2 + 2 * m1 * vy1) / (m1 + m2)

  # Si la colisión es inelástica, se conserva el momento lineal total
  elif tipo_colision == "Inelástica":
    # Ecuaciones para las velocidades finales en colisiones inelásticas 2D
    vx_final = px_total_i / (m1 + m2)
    vy_final = py_total_i / (m1 + m2)
    vx1f = vx_final
    vy1f = vy_final
    vx2f = vx_final
    vy2f = vy_final

  else:
    raise ValueError("Tipo de colisión no válida.")

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
tipo_colision = "Elástica"
dt = 0.01

# Simular la colisión
x1f, y1f, vx1f, vy1f, x2f, y2f, vx2f, vy2f = colision_momento_lineal_2d(m1, x1, y1, vx1, vy1, m2, x2, y2, vx2, vy2, tipo_colision)

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
  x1_t[i], y1_t[i], vx1f, vy1f, x2_t[i], y2_t[i], vx2f, vy2f = colision_momento_lineal_2d(m1, x1_t[i-1], y1_t[i-1], vx1f, vy1f, m2, x2_t[i-1], y2_t[i-1], vx2f, vy2f, tipo_colision)

# Graficar las posiciones
plt.plot(x1_t, y1_t, label="Objeto 1")
plt.plot(x2_t, y2_t, label="Objeto 2")
plt.legend()
plt.xlabel("Tiempo (s)")
plt.ylabel("Posición (m)")
plt.show()
