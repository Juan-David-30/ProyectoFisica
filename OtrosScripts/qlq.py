import numpy as np

def metodo_jacobi(A, b, tolerancia=1e-10, max_iteraciones=1000):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método de Jacobi.
    
    Parámetros:
    - A: Matriz de coeficientes (debe ser cuadrada y diagonalmente dominante).
    - b: Vector de términos independientes.
    - tolerancia: Criterio de convergencia (diferencia entre iteraciones consecutivas).
    - max_iteraciones: Número máximo de iteraciones permitidas.
    
    Retorna:
    - x: Vector solución aproximado.
    - iteraciones: Número de iteraciones realizadas.
    """
    n = len(b)
    x = np.zeros(n)  # Inicializar el vector solución con ceros
    x_nuevo = np.zeros(n)

    # Verificar si la matriz A es diagonalmente dominante
    if not all(abs(A[i, i]) > sum(abs(A[i, j]) for j in range(n) if j != i) for i in range(n)):
        raise ValueError("La matriz A no es diagonalmente dominante. El método de Jacobi puede no converger.")

    for k in range(max_iteraciones):
        for i in range(n):
            suma = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x_nuevo[i] = (b[i] - suma) / A[i, i]

        # Calcular la norma del error
        error = np.linalg.norm(x_nuevo - x, ord=np.inf)
        
        # Actualizar el vector solución
        x = x_nuevo.copy()

        # Verificar el criterio de convergencia
        if error < tolerancia:
            print(f"Convergencia alcanzada en {k + 1} iteraciones.")
            return x, k + 1

    raise ValueError("El método no convergió después de {} iteraciones.".format(max_iteraciones))

# Ejemplo de uso
if __name__ == "__main__":
    # Definir la matriz A y el vector b
    A = np.array([[4, 1, 2],
                  [3, 5, 1],
                  [1, 1, 3]], dtype=float)
    b = np.array([4, 7, 3], dtype=float)

    # Resolver el sistema usando el método de Jacobi
    try:
        solucion, iteraciones = metodo_jacobi(A, b)
        print("Solución encontrada:", solucion)
        print("Número de iteraciones:", iteraciones)
    except ValueError as e:
        print(e)
        
